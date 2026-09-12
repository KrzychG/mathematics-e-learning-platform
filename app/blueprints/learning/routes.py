import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session, current_app
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from app import db, limiter
from app.models import Category, Topic, Task, Attempt, UserTopicProgress
from app.services.answer_service import answers_match
from app.services.llm_service import generate_math_task, generate_hint, are_tasks_too_similar
from app.services.preset_task_service import EXAM_TOPIC_NAME
from app.services.progress_service import update_and_get_difficulty, get_current_difficulty

learning_bp = Blueprint('learning', __name__)

def _pending_topic_task_key(topic_id: int) -> str:
    return f'pending_task_{topic_id}'


def _pick_random_topic(exclude_topic_id: int | None = None) -> Topic | None:
    topics = (
        Topic.query
        .options(joinedload(Topic.category))
        .filter(Topic.name != EXAM_TOPIC_NAME)
        .all()
    )
    if not topics:
        topics = Topic.query.options(joinedload(Topic.category)).all()
    if not topics:
        return None
    if exclude_topic_id is not None and len(topics) > 1:
        filtered = [t for t in topics if t.id != exclude_topic_id]
        if filtered:
            topics = filtered
    return random.choice(topics)


def _get_valid_pending_task(user_id: int, session_key: str, *, topic_id: int | None = None, load_topic: bool = False) -> Task | None:
    # Pobiera z sesji ID zadania, które uczeń aktualnie rozwiązuje
    # Zapobiega generowaniu nowego zadania przy przypadkowym odświeżeniu strony (F5).
    # Jeśli zadanie zostało już rozwiązane lub usunięte z bazy, czyścimy sesję.
    pending_task_id = session.get(session_key)
    if not pending_task_id:
        return None
    if load_topic:
        task = (
            Task.query
            .options(joinedload(Task.topic).joinedload(Topic.category))
            .filter_by(id=pending_task_id)
            .first()
        )
    else:
        task = db.session.get(Task, pending_task_id)
    topic_matches = (task.topic is not None) if topic_id is None else (task.topic_id == topic_id)
    is_valid = (
        task is not None
        and topic_matches
        and task.has_four_options
        and not Attempt.query.filter_by(user_id=user_id, task_id=task.id).first()
    )
    if not is_valid:
        session.pop(session_key, None)
        return None
    return task


def _get_active_random_task(user_id: int) -> Task | None:
    return _get_valid_pending_task(user_id, 'pending_random_task', load_topic=True)


@learning_bp.route('/learning')
@learning_bp.route('/learning/<int:topic_id>')
@login_required
@limiter.exempt
def learning_desk(topic_id=None):
    categories, uncategorized_topics = Category.get_syllabus_tree()
    user_progress = UserTopicProgress.query.filter_by(user_id=current_user.id).all()
    progress_map = {p.topic_id: p.mastery_percent for p in user_progress}
    active_topic = db.session.get(Topic, topic_id) if topic_id else None
    if topic_id and not active_topic:
        flash('Wybrany temat nie istnieje.', 'warning')
        return redirect(url_for('learning.learning_desk'))
    return render_template(
        'learning/learning_desk.html',
        categories=categories,
        uncategorized_topics=uncategorized_topics,
        progress_map=progress_map,
        active_topic=active_topic
    )


@learning_bp.route('/graph-explorer')
@login_required
@limiter.exempt
def graph_explorer():
    return render_template('learning/graph_explorer.html')


def _render_practice_page(
    *,
    topic: Topic | None,
    task_data: dict | None,
    difficulty: int | None,
    is_retry: bool = False,
    is_loading: bool = False,
    force_new: bool = False,
    random_mode: bool = False,
):
    return render_template(
        'learning/practice.html',
        topic=topic,
        task=task_data,
        difficulty=difficulty,
        is_retry=is_retry,
        is_loading=is_loading,
        force_new=force_new,
        random_mode=random_mode,
    )
def _resolve_existing_task(user_id: int, topic_id: int, force_new: bool = False) -> Task | None:
    session_key = _pending_topic_task_key(topic_id)
    if force_new:
        prev_id = session.pop(session_key, None)
        if prev_id:
            session[f'_prev_{session_key}'] = prev_id
        return None
    active_task = _get_valid_pending_task(user_id, session_key, topic_id=topic_id)
    if active_task:
        return active_task
    difficulty = get_current_difficulty(user_id, topic_id)
    user_attempted_task_ids = [
        a.task_id for a in Attempt.query.filter_by(user_id=user_id).all()
    ]
    user_attempted_questions = [
        t.question for t in Task.query.filter(Task.id.in_(user_attempted_task_ids), Task.topic_id == topic_id).all()
        if t.question
    ]
    candidates = Task.query.filter(
        Task.topic_id == topic_id,
        Task.difficulty == difficulty,
        Task.options.isnot(None),
        Task.options != 'null',
        ~Task.attempts.any(Attempt.user_id == user_id)
    ).order_by(Task.id.desc()).all()
    for candidate in candidates:
        if candidate.has_four_options:
            if user_attempted_questions and any(are_tasks_too_similar(candidate.question, uq) for uq in user_attempted_questions):
                continue
            session[session_key] = candidate.id
            return candidate
    return None
def _task_topic_meta(topic: Topic) -> dict:
    return {
        "topic_id": topic.id,
        "topic_name": topic.name,
        "category_name": topic.category_label,
        "theory_url": url_for('learning.learning_desk', topic_id=topic.id),
    }
def _try_generate_pending_task(
    topic_id: int,
    difficulty: int,
    session_key: str,
) -> tuple[dict | None, Exception | None]:
    try:
        exclude_task_id = session.pop(f'_prev_{session_key}', None)
        task_data = generate_math_task(
            topic_id=topic_id,
            difficulty_level=difficulty,
            exclude_task_id=exclude_task_id,
        )
        session[session_key] = task_data['task_id']
        return task_data, None
    except Exception as err:
        db.session.rollback()
        return None, err


def _generate_sync_task(topic_id: int, difficulty: int, session_key: str) -> dict | None:
    task_data, err = _try_generate_pending_task(topic_id, difficulty, session_key)
    if err is not None:
        flash(f'Nie udało się pobrać zadania: {str(err)}', 'danger')
        return None
    return task_data


@learning_bp.route('/practice/random')
@login_required
@limiter.limit("30 per minute; 150 per hour")
def random_practice():
    is_new = request.args.get('new', type=int) == 1
    force_new = request.args.get('force_new', type=int) == 1
    is_sync = request.args.get('sync', type=int) == 1
    reset_pending = is_new or force_new
    if reset_pending:
        prev_random_id = session.pop('pending_random_task', None)
        if prev_random_id:
            session['_prev_pending_random_task'] = prev_random_id
    topic = None
    task_data = None
    difficulty = None
    is_loading = False
    active_task = None if reset_pending else _get_active_random_task(current_user.id)
    if active_task:
        task_data = active_task.to_view_dict()
        topic = active_task.topic
        difficulty = active_task.difficulty
    else:
        topic = _pick_random_topic()
        if not topic:
            flash('Brak tematów w bazie danych, aby wylosować zadanie.', 'warning')
            return redirect(url_for('dashboard.dashboard'))
        if reset_pending and not is_sync:
            return redirect(url_for('learning.random_practice'))
        if is_sync:
            difficulty = get_current_difficulty(current_user.id, topic.id)
            task_data = _generate_sync_task(topic.id, difficulty, 'pending_random_task')
            if task_data is None:
                return redirect(url_for('dashboard.dashboard'))
        else:
            topic = None
            is_loading = True
    return _render_practice_page(
        topic=topic,
        task_data=task_data,
        difficulty=difficulty,
        is_loading=is_loading,
        random_mode=True,
    )
@learning_bp.route('/practice/<int:topic_id>')
@login_required
@limiter.limit("30 per minute; 150 per hour")
def practice(topic_id):
    topic = db.get_or_404(Topic, topic_id)
    retry_task_id = request.args.get('task_id', type=int)
    force_new = request.args.get('force_new', type=int) == 1
    random_mode = (request.args.get('mode') == 'random') and bool(retry_task_id)
    difficulty = get_current_difficulty(current_user.id, topic.id)
    task_data = None
    is_retry = False
    is_loading = False
    if retry_task_id:
        task = db.session.get(Task, retry_task_id)
        if not task or task.topic_id != topic.id:
            abort(404)
        task_data = task.to_view_dict()
        difficulty = task.difficulty
        is_retry = True
    else:
        existing_task = _resolve_existing_task(current_user.id, topic.id, force_new=force_new)
        if existing_task:
            task_data = existing_task.to_view_dict()
            difficulty = existing_task.difficulty
        elif request.args.get('sync', type=int) == 1:
            task_data = _generate_sync_task(topic.id, difficulty, _pending_topic_task_key(topic.id))
            if task_data is None:
                return redirect(url_for('learning.learning_desk', topic_id=topic.id))
        else:
            is_loading = True
    return _render_practice_page(
        topic=topic,
        task_data=task_data,
        difficulty=difficulty,
        is_retry=is_retry,
        is_loading=is_loading,
        force_new=force_new if is_loading else False,
        random_mode=random_mode,
    )


@learning_bp.route('/check-answer', methods=['POST'])
@login_required
@limiter.limit("20 per minute; 100 per hour")
def check_answer():
    # Główny endpoint sprawdzania odpowiedzi ucznia w trybie ćwiczeń
    # Walidacja formatu wejścia.
    # Porównanie odpowiedzi funkcją answers_match.
    #Przy błędzie generujemy wyjaśnienie/podpowiedź z analizą popełnionego błędu.
    #jeśli uczeń rozwiązał już to zadanie poprawnie w przeszłości, zapisujemy próbę,
    #ale nie podbijamy po raz kolejny poziomu trudności ani nie dublujemy odznak.
    # Aktualizacja adaptacyjnej trudności tematu i zwolnienie zadania oczekującego w sesji.
    task_id = request.form.get('task_id', type=int)
    if task_id is None or task_id <= 0:
        abort(400)
    user_answer = request.form.get('user_answer', '').strip()
    if len(user_answer) > 255:
        user_answer = user_answer[:255]
    random_mode = request.form.get('mode', '').strip() == 'random'
    task = db.get_or_404(Task, task_id)
    if task.options_dict:
        allowed_keys = {str(k).strip().upper() for k in task.options_dict.keys()}
        allowed_vals = {str(v).strip() for v in task.options_dict.values() if v is not None}
        if user_answer.upper() not in allowed_keys and user_answer not in allowed_vals:
            abort(400)
    is_correct = answers_match(user_answer, task.correct_answer, options=task.options_dict)
    hint = None
    if not is_correct:
        hint = generate_hint(task.question, task.correct_answer, user_answer, options=task.options_dict)
    new_attempt = Attempt(
        user_id=current_user.id,
        task_id=task.id,
        user_answer=user_answer,
        is_correct=is_correct,
        llm_hint_provided=hint
    )
    try:
        already_solved = Attempt.query.filter(
            Attempt.user_id == current_user.id,
            Attempt.task_id == task.id,
            Attempt.is_correct.is_(True)
        ).first() is not None
        db.session.add(new_attempt)
        if already_solved:
            db.session.commit()
            current_diff = get_current_difficulty(current_user.id, task.topic_id)
            progress_result = {
                "new_difficulty": current_diff,
                "level_changed": False,
                "action": None,
                "new_badges": []
            }
        else:
            progress_result = update_and_get_difficulty(current_user.id, task.topic_id, is_correct)
        topic_key = _pending_topic_task_key(task.topic_id)
        if not random_mode or session.get(topic_key) == task.id:
            session.pop(topic_key, None)
        if random_mode or session.get('pending_random_task') == task.id:
            session.pop('pending_random_task', None)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(
            f"Błąd transakcji podczas sprawdzania odpowiedzi (user_id={current_user.id}, task_id={task.id}): {e}",
            exc_info=True
        )
        flash('Wystąpił błąd podczas zapisywania odpowiedzi.', 'danger')
        return redirect(url_for('learning.learning_desk', topic_id=task.topic_id))
    return render_template(
        'dashboard/result.html',
        is_correct=is_correct,
        user_answer=user_answer,
        correct_answer=task.correct_answer,
        task_options=task.options_dict,
        hint=hint,
        task_content=task.question,
        level_changed=progress_result['level_changed'],
        action=progress_result['action'],
        new_difficulty=progress_result['new_difficulty'],
        topic_id=task.topic_id,
        topic_name=task.topic.name if task.topic else '',
        random_mode=random_mode,
        task_id=task.id,
        graph_spec=task.graph_spec,
        new_badges=progress_result.get('new_badges', [])
    )
from app.blueprints.learning import api_routes  # noqa: E402, F401
