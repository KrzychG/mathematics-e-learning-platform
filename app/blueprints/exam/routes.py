import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, has_request_context
from flask_login import current_user, login_required

from app import db, limiter
from app.models import EXAM_PASS_RATIO, EXAM_REQUIRED_TASKS, ExamAttempt, Task, utc_now
from app.services.answer_service import answers_match, resolve_choice_letter
from app.services.progress_service import get_user_exam_stats, _check_and_award_achievements
from app.services.preset_task_service import (
    create_unique_exam_tasks,
    get_preset_exam_tasks,
    get_preset_explanations_map,
    get_or_create_exam_topic,
    normalize_question_key,
)
from app.utils import json_error, json_success, wants_json_response
from app.services.history_service import load_entities_by_ids, paginate_clamped

exam_bp = Blueprint('exam', __name__)

def _get_or_create_exam_tasks(required_count=EXAM_REQUIRED_TASKS) -> list[Task]:
    # Przygotowanie 20 unikalnych zadań do arkusza egzaminacyjnego:
    #Pobieramy zadania z bazy i deduplikujemy po znormalizowanym pytaniu.
    #Jeśli w bazie brakuje zadań do pełnego arkusza, doładowujemy zadania z preset_tasks.json.
    #W skrajnym przypadku algorytmicznie dopełniamy brakujące pozycje.
    # Losujemy próbkę dokładnie 20 pytań.
    candidate_tasks = (
        Task.query.filter(
            Task.options.isnot(None),
            Task.correct_answer.isnot(None)
        )
        .order_by(Task.id.desc())
        .limit(1000)
        .all()
    )
    unique_by_key: dict[str, Task] = {}
    for task in candidate_tasks:
        if not task.has_four_options:
            continue
        q_key = normalize_question_key(task.question)
        if not q_key:
            continue
        existing = unique_by_key.get(q_key)
        if existing is None or (task.explanation and not existing.explanation):
            unique_by_key[q_key] = task
    valid_tasks = list(unique_by_key.values())
    if len(valid_tasks) >= required_count:
        return random.sample(valid_tasks, required_count)
    fallback_topic = get_or_create_exam_topic()
    preset_items = get_preset_exam_tasks()
    preset_questions = [p["question"] for p in preset_items if "question" in p]
    existing_preset = {
        normalize_question_key(t.question): t
        for t in Task.query.filter(Task.question.in_(preset_questions)).all()
    }
    added_presets = create_unique_exam_tasks(
        preset_items,
        topic_id=fallback_topic.id,
        existing_by_key=existing_preset,
        seen_keys=set(unique_by_key.keys()),
    )
    for task in added_presets:
        unique_by_key[normalize_question_key(task.question)] = task
        valid_tasks.append(task)
    pad_idx = 1
    while len(valid_tasks) < required_count:
        pad_q = f"Zadanie próbne {pad_idx}: Oblicz wartość wyrażenia {pad_idx} + {pad_idx}."
        pad_key = normalize_question_key(pad_q)
        pad_idx += 1
        if pad_key in unique_by_key:
            continue
        pad_task = Task(
            topic_id=fallback_topic.id,
            question=pad_q,
            options={"A": str(2 * (pad_idx - 1)), "B": "0", "C": "-1", "D": "99"},
            correct_answer="A",
            difficulty=2
        )
        db.session.add(pad_task)
        unique_by_key[pad_key] = pad_task
        valid_tasks.append(pad_task)
    db.session.commit()
    return random.sample(valid_tasks, required_count)
def get_active_exam_attempt(user_id: int) -> ExamAttempt | None:
    return ExamAttempt.query.filter_by(
        user_id=user_id,
        is_completed=False
    ).order_by(ExamAttempt.created_at.desc()).first()
@exam_bp.route('/')
@exam_bp.route('/lobby')
@login_required
def exam_lobby():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    active_attempt = get_active_exam_attempt(current_user.id)
    stats = get_user_exam_stats(current_user.id)
    total_exams = stats["completed_count"]
    passed_exams = stats["passed_count"]
    best_score = stats["best_score"]
    avg_percentage = stats["avg_percentage"]
    completed_query = ExamAttempt.query.filter_by(
        user_id=current_user.id,
        is_completed=True
    ).order_by(ExamAttempt.completed_at.desc(), ExamAttempt.id.desc())
    attempts_pagination = paginate_clamped(completed_query, page=page, per_page=per_page)
    return render_template(
        'exam/lobby.html',
        active_attempt=active_attempt,
        attempts=attempts_pagination.items,
        attempts_pagination=attempts_pagination,
        total_exams=total_exams,
        passed_exams=passed_exams,
        best_score=best_score,
        avg_percentage=avg_percentage
    )


def _exam_redirect_response(
    redirect_url: str,
    *,
    is_ajax: bool = False,
    message: str | None = None,
    category: str = 'info',
):
    if is_ajax:
        return json_success(redirect_url=redirect_url)
    if message:
        flash(message, category)
    return redirect(redirect_url)


@exam_bp.route('/generating')
@login_required
def exam_generating():
    existing_active = get_active_exam_attempt(current_user.id)
    if existing_active:
        return _exam_redirect_response(
            url_for('exam.exam_session', attempt_id=existing_active.id),
            message='Kontynuujesz rozpoczęty wcześniej arkusz egzaminacyjny.',
        )
    return render_template('exam/generating.html')


@exam_bp.route('/start', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def start_exam():
    is_ajax = wants_json_response()
    existing_active = get_active_exam_attempt(current_user.id)
    if existing_active:
        return _exam_redirect_response(
            url_for('exam.exam_session', attempt_id=existing_active.id),
            is_ajax=is_ajax,
            message='Kontynuujesz rozpoczęty wcześniej arkusz egzaminacyjny.',
        )
    from app.services.llm_service import generate_exam_tasks
    tasks = generate_exam_tasks(required_count=EXAM_REQUIRED_TASKS)
    ai_generated = bool(tasks and len(tasks) >= EXAM_REQUIRED_TASKS)
    if not ai_generated:
        tasks = _get_or_create_exam_tasks(required_count=EXAM_REQUIRED_TASKS)
    new_attempt = ExamAttempt(
        user_id=current_user.id,
        title='Próbny Egzamin - Poziom Podstawowy',
        score=0,
        total_tasks=len(tasks),
        passed=False,
        is_completed=False,
        task_ids=[t.id for t in tasks],
        answers={},
        created_at=utc_now()
    )
    db.session.add(new_attempt)
    db.session.commit()
    start_msg = (
        f'Sztuczna inteligencja wygenerowała dla Ciebie unikalny arkusz {EXAM_REQUIRED_TASKS} zadań egzaminacyjnych! Powodzenia!'
        if ai_generated
        else f'Egzamin został rozpoczęty! Arkusz zawiera {EXAM_REQUIRED_TASKS} zadań zamkniętych bez limitu czasu. Powodzenia!'
    )
    return _exam_redirect_response(
        url_for('exam.exam_session', attempt_id=new_attempt.id),
        is_ajax=is_ajax,
        message=start_msg,
        category='success',
    )


def _authorize_exam_attempt(attempt: ExamAttempt, *, as_json: bool = False):
    if attempt.user_id != current_user.id and not current_user.is_admin:
        if as_json:
            return json_error("Brak uprawnień.", 403)
        abort(403)
    return None


def _sync_attempt_existing_tasks(attempt: ExamAttempt) -> tuple[dict[int, Task], list[Task]]:
    task_ids = attempt.task_ids or []
    task_map = load_entities_by_ids(Task.query, Task.id, task_ids)
    if attempt.prune_missing_task_ids(set(task_map.keys())):
        db.session.commit()
    ordered_tasks = [task_map[tid] for tid in (attempt.task_ids or []) if tid in task_map]
    return task_map, ordered_tasks


def _evaluate_attempt_answers(attempt: ExamAttempt) -> tuple[list[dict], int, int]:
    # Weryfikacja przesłanych odpowiedzi w arkuszu egzaminacyjnym
    # Przepuszcza każdą odpowiedź przez answers_match
    # i buduje szczegółowe podsumowanie każdego zadania
    task_map, _ = _sync_attempt_existing_tasks(attempt)
    task_ids = attempt.task_ids or []
    answers = attempt.answers or {}
    preset_explanations = get_preset_explanations_map()
    breakdown = []
    score = 0
    for idx, tid in enumerate(task_ids, start=1):
        task = task_map.get(tid)
        if not task:
            continue
        user_ans = (answers.get(str(tid)) or '').strip()
        is_correct = answers_match(user_ans, task.correct_answer, options=task.options_dict)
        if is_correct:
            score += 1
        correct_letter = resolve_choice_letter(
            task.correct_answer,
            options=task.options_dict,
            fallback=str(task.correct_answer).strip().upper(),
        )
        user_letter = resolve_choice_letter(
            user_ans,
            options=task.options_dict,
            fallback=(user_ans.strip().upper() if user_ans else ''),
        )
        breakdown.append({
            "number": idx,
            "task": task,
            "user_answer": user_letter or '',
            "user_text": task.options_dict.get(user_letter or '', ''),
            "correct_answer": correct_letter,
            "correct_text": task.options_dict.get(correct_letter, ''),
            "is_correct": is_correct,
            "is_unanswered": not bool(user_ans),
            "explanation": task.explanation or preset_explanations.get(task.question),
        })
    return breakdown, score, len(task_ids)


@exam_bp.route('/session/<int:attempt_id>')
@login_required
def exam_session(attempt_id):
    attempt = db.get_or_404(ExamAttempt, attempt_id)
    _authorize_exam_attempt(attempt)
    if attempt.is_completed:
        return redirect(url_for('exam.exam_result', attempt_id=attempt.id))
    _, ordered_tasks = _sync_attempt_existing_tasks(attempt)
    if not ordered_tasks:
        db.session.delete(attempt)
        db.session.commit()
        flash('Rozpoczęty arkusz nie zawiera już dostępnych zadań. Wygeneruj nowy egzamin.', 'warning')
        return redirect(url_for('exam.exam_lobby'))
    return render_template(
        'exam/session.html',
        attempt=attempt,
        tasks=ordered_tasks,
        answers=attempt.answers,
        hide_scratchpad=True
    )


@exam_bp.route('/session/<int:attempt_id>/save-answer', methods=['POST'])
@login_required
def save_answer(attempt_id):
    attempt = db.get_or_404(ExamAttempt, attempt_id)
    err_resp = _authorize_exam_attempt(attempt, as_json=True)
    if err_resp:
        return err_resp
    if attempt.is_completed:
        return json_error("Arkusz został już zakończony.", 400)
    data = request.get_json(silent=True) or request.form
    task_id_str = str(data.get('task_id', '')).strip()
    selected_option = str(data.get('selected_option', '')).strip().upper()
    valid_task = task_id_str.isdigit() and int(task_id_str) in (attempt.task_ids or [])
    if not valid_task or selected_option not in ('A', 'B', 'C', 'D'):
        return json_error("Nieprawidłowe dane odpowiedzi.", 400)
    if attempt.answers is None:
        attempt.answers = {}
    attempt.answers[task_id_str] = selected_option
    db.session.commit()
    return json_success(
        task_id=task_id_str,
        selected_option=selected_option,
        answered_count=len(attempt.answers),
    )


@exam_bp.route('/session/<int:attempt_id>/submit', methods=['POST'])
@login_required
def submit_exam(attempt_id):
    attempt = db.get_or_404(ExamAttempt, attempt_id)
    _authorize_exam_attempt(attempt)
    if attempt.is_completed:
        return redirect(url_for('exam.exam_result', attempt_id=attempt.id))
    _finish_and_grade_attempt(attempt)
    flash('Arkusz egzaminacyjny został pomyślnie oddany i sprawdzony!', 'success')
    return redirect(url_for('exam.exam_result', attempt_id=attempt.id))


@exam_bp.route('/result/<int:attempt_id>')
@login_required
def exam_result(attempt_id):
    attempt = db.get_or_404(ExamAttempt, attempt_id)
    _authorize_exam_attempt(attempt)
    if not attempt.is_completed:
        return redirect(url_for('exam.exam_session', attempt_id=attempt.id))
    results_breakdown, _, _ = _evaluate_attempt_answers(attempt)
    return render_template(
        'exam/result.html',
        attempt=attempt,
        breakdown=results_breakdown
    )
    _authorize_exam_attempt(attempt)
    if not attempt.is_completed:
        return redirect(url_for('exam.exam_session', attempt_id=attempt.id))
    results_breakdown, _, _ = _evaluate_attempt_answers(attempt)
    return render_template(
        'exam/result.html',
        attempt=attempt,
        breakdown=results_breakdown
    )
def _finish_and_grade_attempt(attempt: ExamAttempt) -> None:
    # Finalizacja i ocena egzaminu:
    # Podlicza punkty, weryfikuje próg zdawalności
    # i sprawdza odznaki w kontekście egzaminu
    if attempt.is_completed:
        return
    _, score, total = _evaluate_attempt_answers(attempt)
    attempt.score = score
    attempt.total_tasks = total
    attempt.passed = (score / total) >= EXAM_PASS_RATIO if total > 0 else False
    attempt.completed_at = utc_now()
    attempt.is_completed = True
    db.session.flush()
    new_badges = _check_and_award_achievements(
        attempt.user_id,
        hit_streak_3=False,
        context="exam",
        exam_attempt=attempt,
    )
    db.session.commit()
    if has_request_context():
        for badge in new_badges:
            flash(f'Zdobyto nowe osiągnięcie: {badge.name}!', 'success')
