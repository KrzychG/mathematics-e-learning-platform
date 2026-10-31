"""
Serwis Postępów Dydaktycznych i Grywalizacji
Realizuje adaptacyjny algorytm poziomu trudności 
3 poprawne odpowiedzi z rzędu w temacie -> awans
2 błędne odpowiedzi z rzędu -> spadek
Silnik przyznawania odznak 
Weryfikuje warunki serie, cele dzienne, dni aktywności, wyniki egzaminu i odblokowuje odznaki
Błyskawiczna agregacja statystyk ucznia skuteczność, dzisiejsze zadania, egzaminy pojedynczym zapytaniem SQL
"""

from app.services.timezone_service import get_today_start_utc, to_local_time, utc_now
from sqlalchemy import func, case, and_
from app import db
from app.models import UserTopicProgress, Attempt, Achievement, UserAchievement, ExamAttempt
from app.services.achievements_catalog import ACHIEVEMENTS_CATALOG

def sync_achievements_catalog(commit: bool = True) -> int:
    existing = {
        a.trigger_condition: a
        for a in Achievement.query.all()
        if a.trigger_condition
    }
    created = 0
    for item in ACHIEVEMENTS_CATALOG:
        cond = item["trigger_condition"]
        if cond not in existing:
            db.session.add(Achievement(**item))
            created += 1
    if commit:
        db.session.commit()
    return created


def get_user_exam_stats(user_id: int) -> dict:
    # Agregacja statystyk egzaminacyjnych w jednym strzale do bazy.
    # Unikamy wyciągania całych modeli ExamAttempt do Pythona
    perc_expr = case(
        (and_(ExamAttempt.is_completed.is_(True), ExamAttempt.total_tasks > 0), ExamAttempt.score * 100.0 / ExamAttempt.total_tasks),
        else_=None
    )
    row = db.session.query(
        func.count(ExamAttempt.id),
        func.coalesce(func.sum(case((ExamAttempt.is_completed.is_(True), 1), else_=0)), 0),
        func.coalesce(func.sum(case((and_(ExamAttempt.is_completed.is_(True), ExamAttempt.passed.is_(True)), 1), else_=0)), 0),
        func.coalesce(func.avg(perc_expr), 0),
        func.coalesce(func.max(perc_expr), 0),
        func.coalesce(func.max(case((ExamAttempt.is_completed.is_(True), ExamAttempt.score), else_=None)), 0),
    ).filter(ExamAttempt.user_id == user_id).first()
    total_exams = row[0] or 0
    completed_count = int(row[1] or 0)
    passed_count = int(row[2] or 0)
    avg_percentage = int(round(float(row[3] or 0))) if completed_count > 0 else 0
    best_percentage = int(round(float(row[4] or 0))) if completed_count > 0 else 0
    best_score = int(row[5] or 0)
    return {
        "total_exams": total_exams,
        "completed_count": completed_count,
        "passed_count": passed_count,
        "avg_percentage": avg_percentage,
        "best_percentage": best_percentage,
        "best_score": best_score,
    }


def get_user_attempt_stats(user_id: int) -> dict:
    # Szybkie podsumowanie aktywności ucznia
    # today_start jest w UTC pod indeks created_at, więc liczymy wszystko jednym zapytaniem SQL.
    today_start = get_today_start_utc()
    stats = db.session.query(
        func.count(Attempt.id),
        func.coalesce(func.sum(case((Attempt.is_correct.is_(True), 1), else_=0)), 0),
        func.coalesce(func.sum(case((and_(Attempt.created_at >= today_start, Attempt.is_correct.is_(True)), 1), else_=0)), 0),
        func.coalesce(func.sum(case((and_(Attempt.llm_hint_provided.isnot(None), Attempt.llm_hint_provided != ''), 1), else_=0)), 0)
    ).filter(Attempt.user_id == user_id).first()
    total = stats[0] or 0
    correct = int(stats[1] or 0)
    today_correct = int(stats[2] or 0)
    hints_used = int(stats[3] or 0)
    accuracy = int(round((correct / total * 100))) if total > 0 else 0
    return {
        "total_attempts": total,
        "correct_attempts": correct,
        "today_correct": today_correct,
        "hints_used": hints_used,
        "accuracy": accuracy,
    }
PRACTICE_CONDITIONS = {
    "first_task",
    "streak_3",
    "daily_goal_5",
    "daily_goal_10",
    "attempts_10",
    "correct_10",
    "correct_25",
    "correct_50",
    "correct_100",
    "accuracy_80",
    "active_days_3",
    "active_days_7",
    "level_3",
    "level_4",
    "level_5",
    "topics_5",
    "topics_10",
    "mastered_3",
}

EXAM_CONDITIONS = {
    "exam_passed",
    "exam_high_80",
}

def _check_and_award_achievements(
    user_id: int,
    hit_streak_3: bool,
    *,
    context: str | None = None,
    is_correct: bool | None = None,
    current_topic_difficulty: int | None = None,
    exam_attempt: ExamAttempt | None = None,
) -> list:
    # Weryfikacja i przyznawanie odznak
    # Żeby nie męczyć bazy, najpierw wyciągamy tylko te odznaki, których uczeń jeszcze nie zdobył.
    # Jeśli uczeń ma już wszystkie dostępne w danym kontekście, od razu uciekamy.
    unlocked_subquery = (
        db.session.query(UserAchievement.achievement_id)
        .filter(UserAchievement.user_id == user_id)
    )
    query = Achievement.query.filter(~Achievement.id.in_(unlocked_subquery))
    if context == "practice":
        query = query.filter(Achievement.trigger_condition.in_(PRACTICE_CONDITIONS))
    elif context == "exam":
        query = query.filter(Achievement.trigger_condition.in_(EXAM_CONDITIONS))
    locked_achievements = query.all()
    if not locked_achievements:
        return []
    needed_conditions = {badge.trigger_condition for badge in locked_achievements if badge.trigger_condition}
    total_attempts = 0
    correct_attempts = 0
    today_correct = 0
    # pobieramy z bazy tylko te metryki, które są faktycznie potrzebne
    # dla brakujących odznak pomijamy sprawdzanie dni aktywności, jeśli user ma już te odznaki.
    attempt_metric_conditions = {
        "first_task", "attempts_10", "correct_10", "correct_25",
        "correct_50", "correct_100", "daily_goal_5", "daily_goal_10", "accuracy_80",
    }
    if bool(needed_conditions & attempt_metric_conditions):
        stats = get_user_attempt_stats(user_id)
        total_attempts = stats["total_attempts"]
        correct_attempts = stats["correct_attempts"]
        today_correct = stats["today_correct"]
    active_days = 0
    if bool(needed_conditions & {"active_days_3", "active_days_7"}):
        attempt_dates = (
            db.session.query(Attempt.created_at)
            .filter(Attempt.user_id == user_id, Attempt.created_at.isnot(None))
            .all()
        )
        active_days = len({to_local_time(row[0]).date() for row in attempt_dates if row[0]})
    max_level = 1
    topics_started = 0
    mastered_topics = 0
    topic_metric_conditions = {
        "streak_3", "level_3", "level_4", "level_5",
        "topics_5", "topics_10", "mastered_3",
    }
    if bool(needed_conditions & topic_metric_conditions):
        progress_stats = db.session.query(
            func.coalesce(func.max(UserTopicProgress.current_difficulty), 1),
            func.count(UserTopicProgress.topic_id),
            func.coalesce(func.sum(case((UserTopicProgress.current_difficulty >= 5, 1), else_=0)), 0),
        ).filter(UserTopicProgress.user_id == user_id).first()
        if progress_stats:
            max_level = progress_stats[0] or 1
            topics_started = progress_stats[1] or 0
            mastered_topics = int(progress_stats[2] or 0)
    passed_exams = 0
    best_exam_pct = 0
    if exam_attempt is not None:
        if exam_attempt.is_completed:
            if exam_attempt.passed:
                passed_exams = 1
            best_exam_pct = exam_attempt.percentage
    elif context != "practice" and bool(needed_conditions & EXAM_CONDITIONS):
        exam_stats = get_user_exam_stats(user_id)
        passed_exams = exam_stats["passed_count"]
        best_exam_pct = exam_stats["best_percentage"]
    accuracy_pct = (correct_attempts / total_attempts * 100.0) if total_attempts > 0 else 0.0
    answered_correctly = True if is_correct is None else bool(is_correct)
    topic_level = max_level if current_topic_difficulty is None else current_topic_difficulty
    conditions_met = {
        "first_task": total_attempts >= 1,
        "streak_3": answered_correctly and (hit_streak_3 if context == "practice" else (hit_streak_3 or max_level > 1)),
        "daily_goal_5": answered_correctly and today_correct >= 5,
        "daily_goal_10": answered_correctly and today_correct >= 10,
        "attempts_10": total_attempts >= 10,
        "correct_10": answered_correctly and correct_attempts >= 10,
        "correct_25": answered_correctly and correct_attempts >= 25,
        "correct_50": answered_correctly and correct_attempts >= 50,
        "correct_100": answered_correctly and correct_attempts >= 100,
        "accuracy_80": answered_correctly and total_attempts >= 20 and accuracy_pct >= 80.0,
        "active_days_3": active_days >= 3,
        "active_days_7": active_days >= 7,
        "level_3": answered_correctly and topic_level >= 3,
        "level_4": answered_correctly and topic_level >= 4,
        "level_5": answered_correctly and topic_level >= 5,
        "topics_5": topics_started >= 5,
        "topics_10": topics_started >= 10,
        "mastered_3": answered_correctly and topic_level >= 5 and mastered_topics >= 3,
        "exam_passed": passed_exams >= 1,
        "exam_high_80": best_exam_pct >= 80,
    }
    new_badges = []
    for badge in locked_achievements:
        if conditions_met.get(badge.trigger_condition, False):
            ua = UserAchievement(
                user_id=user_id,
                achievement_id=badge.id,
                unlocked_at=utc_now()
            )
            db.session.add(ua)
            new_badges.append(badge)
    return new_badges
def update_and_get_difficulty(user_id: int, topic_id: int, is_correct: bool) -> dict:
    # Algorytm adaptacji trudności w danym temacie
    # - seria 3 dobrych odpowiedzi awansuje o poziom wyżej (max level 5)
    # - 2 potknięcia z rzędu cofają na niższy poziom (min level 1)
    # Przy zmianie poziomu zerujemy bieżącą passę, a flushujemy stan przed ewaluacją odznak,
    # żeby warunki poziomu widziały świeży poziom w tej samej transakcji.
    progress = UserTopicProgress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
    if not progress:
        progress = UserTopicProgress(user_id=user_id, topic_id=topic_id)
        db.session.add(progress)
    progress.consecutive_correct = progress.consecutive_correct or 0
    progress.consecutive_wrong = progress.consecutive_wrong or 0
    progress.current_difficulty = progress.current_difficulty or 1
    progress.last_activity = utc_now()
    level_changed = False
    action = None
    hit_streak_3 = False
    if is_correct:
        progress.consecutive_correct += 1
        progress.consecutive_wrong = 0
        if progress.consecutive_correct >= 3:
            hit_streak_3 = True
            progress.consecutive_correct = 0
            if progress.current_difficulty < 5:
                progress.current_difficulty += 1
                level_changed = True
                action = 'up'
    else:
        progress.consecutive_wrong += 1
        progress.consecutive_correct = 0
        if progress.consecutive_wrong >= 2 and progress.current_difficulty > 1:
            progress.current_difficulty -= 1
            progress.consecutive_wrong = 0
            level_changed = True
            action = 'down'
    try:
        db.session.flush()
        new_badges = _check_and_award_achievements(
            user_id,
            hit_streak_3,
            context="practice",
            is_correct=is_correct,
            current_topic_difficulty=progress.current_difficulty,
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return {
        "new_difficulty": progress.current_difficulty,
        "level_changed": level_changed,
        "action": action,
        "new_badges": new_badges
    }


def get_current_difficulty(user_id: int, topic_id: int) -> int:
    diff = db.session.query(UserTopicProgress.current_difficulty).filter_by(user_id=user_id, topic_id=topic_id).scalar()
    return diff if diff else 1
