from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app import db
from app.models import (
    Attempt,
    Category,
    ExamAttempt,
    Task,
    Topic,
    User,
    UserAchievement,
    UserTopicProgress,
)
from app.services.history_service import paginate_clamped
from app.services.progress_service import get_user_attempt_stats, get_user_exam_stats
from app.services.timezone_service import parse_local_date_range_to_utc
from app.services.user_service import count_active_admins

USER_SORT_OPTIONS = {
    'id_desc': 'ID: od najnowszych',
    'id_asc': 'ID: od najstarszych',
    'name_asc': 'Imię: A–Z',
    'name_desc': 'Imię: Z–A',
    'email_asc': 'E-mail: A–Z',
    'email_desc': 'E-mail: Z–A',
    'created_desc': 'Rejestracja: najnowsze',
    'created_asc': 'Rejestracja: najstarsze',
    'activity_desc': 'Aktywność: najnowsza',
    'activity_asc': 'Aktywność: najstarsza',
}

def _build_user_last_activity_query():
    # Wyznacza ostatnią aktywność ucznia jednym zapytaniem SQL
    # Aktywność pochodzi z dwóch różnych źródeł
    # Tworzymy podzapytania agregujące z max(created_at), łączymy je przez OUTER JOIN z tabelą users
    # i wybieramy najświeższą datę przez instrukcję CASE
    attempt_subq = (
        db.session.query(
            Attempt.user_id.label('user_id'),
            func.max(Attempt.created_at).label('max_attempt_at'),
        )
        .group_by(Attempt.user_id)
        .subquery()
    )
    exam_subq = (
        db.session.query(
            ExamAttempt.user_id.label('user_id'),
            func.max(ExamAttempt.created_at).label('max_exam_at'),
        )
        .group_by(ExamAttempt.user_id)
        .subquery()
    )
    max_attempt_col = attempt_subq.c.max_attempt_at
    max_exam_col = exam_subq.c.max_exam_at
    max_interaction = db.case(
        (max_attempt_col.is_(None), max_exam_col),
        (max_exam_col.is_(None), max_attempt_col),
        (max_attempt_col >= max_exam_col, max_attempt_col),
        else_=max_exam_col,
    )
    last_activity_case = db.case(
        (max_interaction.is_(None), User.created_at),
        (User.created_at.is_(None), max_interaction),
        (max_interaction >= User.created_at, max_interaction),
        else_=User.created_at,
    )
    last_activity_expr = db.type_coerce(last_activity_case, db.DateTime).label('last_activity')
    query = (
        db.session.query(User, last_activity_expr)
        .outerjoin(attempt_subq, attempt_subq.c.user_id == User.id)
        .outerjoin(exam_subq, exam_subq.c.user_id == User.id)
    )
    return query, last_activity_case


def _coerce_activity_datetime(raw_value, fallback):
    if isinstance(raw_value, str):
        try:
            return datetime.fromisoformat(raw_value)
        except ValueError:
            return fallback
    return raw_value or fallback


def _get_user_last_activity(user: User):
    query, _ = _build_user_last_activity_query()
    row = query.filter(User.id == user.id).first()
    return _coerce_activity_datetime(row[1], user.created_at) if row else user.created_at


def get_filtered_users_pagination(
    search_query: str = '',
    role_filter: str = 'all',
    status_filter: str = 'all',
    otp_filter: str = 'all',
    page: int = 1,
    per_page: int = 15,
    date_from: str = '',
    date_to: str = '',
    sort_by: str = 'id_desc',
):
    # Zbiorcze filtrowanie i sortowanie listy użytkowników w CMS
    # Obsługuje wyszukiwanie po emailu/imieniu, filtry ról, blokady konta, 2FA
    # oraz sortowanie dynamiczne
    query, last_activity_case = _build_user_last_activity_query()
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            db.or_(
                User.email.ilike(search_pattern),
                User.first_name.ilike(search_pattern),
            )
        )
    filter_mappings = [
        (role_filter, {'admin': User.is_admin.is_(True), 'student': User.is_admin.is_(False)}),
        (status_filter, {'active': User.is_active.is_(True), 'blocked': User.is_active.is_(False)}),
        (
            otp_filter,
            {
                'enabled': User.is_otp_enabled.is_(True),
                'disabled': db.or_(User.is_otp_enabled.is_(False), User.is_otp_enabled.is_(None)),
            },
        ),
    ]
    for val, mapping in filter_mappings:
        if val in mapping:
            query = query.filter(mapping[val])
    start_utc, end_utc_exclusive = parse_local_date_range_to_utc(date_from, date_to)
    if start_utc is not None:
        query = query.filter(User.created_at >= start_utc)
    if end_utc_exclusive is not None:
        query = query.filter(User.created_at < end_utc_exclusive)
    sort_mappings = {
        'id_desc': (User.id.desc(),),
        'id_asc': (User.id.asc(),),
        'name_asc': (func.lower(func.coalesce(User.first_name, User.email)).asc(), User.id.asc()),
        'name_desc': (func.lower(func.coalesce(User.first_name, User.email)).desc(), User.id.desc()),
        'email_asc': (func.lower(User.email).asc(), User.id.asc()),
        'email_desc': (func.lower(User.email).desc(), User.id.desc()),
        'created_desc': (User.created_at.desc(), User.id.desc()),
        'created_asc': (User.created_at.asc(), User.id.asc()),
        'activity_desc': (last_activity_case.desc(), User.id.desc()),
        'activity_asc': (last_activity_case.asc(), User.id.asc()),
    }
    order_clauses = sort_mappings.get(sort_by, sort_mappings['id_desc'])
    pagination = paginate_clamped(query.order_by(*order_clauses), page=page, per_page=per_page)
    users = []
    for row in pagination.items:
        user_obj, last_act = row[0], row[1]
        user_obj.last_activity = _coerce_activity_datetime(last_act, user_obj.created_at)
        users.append(user_obj)
    pagination.items = users
    return pagination


def get_admin_system_counts() -> dict:
    total_users, total_students, total_admins, active_admins, total_active_users = db.session.query(
        func.count(User.id),
        func.coalesce(func.sum(db.case((User.is_admin.is_(False), 1), else_=0)), 0),
        func.coalesce(func.sum(db.case((User.is_admin.is_(True), 1), else_=0)), 0),
        func.coalesce(func.sum(db.case((db.and_(User.is_admin.is_(True), User.is_active.is_(True)), 1), else_=0)), 0),
        func.coalesce(func.sum(db.case((User.is_active.is_(True), 1), else_=0)), 0),
    ).one()
    return {
        'total_users': int(total_users or 0),
        'total_students': int(total_students or 0),
        'total_admins': int(total_admins or 0),
        'active_admins': int(active_admins or 0),
        'total_active_users': int(total_active_users or 0),
        'total_tasks': Task.query.count(),
        'total_attempts': Attempt.query.count(),
        'total_categories': Category.query.count(),
        'total_topics': Topic.query.count(),
    }


def build_user_detail_context(
    user: User,
    tasks_page: int,
    exams_page: int,
    topics_page: int,
    badges_page: int,
) -> dict:
    stats = get_user_attempt_stats(user.id)
    exam_stats = get_user_exam_stats(user.id)
    attempts_pagination = paginate_clamped(
        Attempt.query
        .options(joinedload(Attempt.task).joinedload(Task.topic).joinedload(Topic.category))
        .filter_by(user_id=user.id)
        .order_by(Attempt.created_at.desc(), Attempt.id.desc()),
        page=tasks_page,
        per_page=15,
    )
    exams_pagination = paginate_clamped(
        ExamAttempt.query
        .filter_by(user_id=user.id)
        .order_by(ExamAttempt.created_at.desc(), ExamAttempt.id.desc()),
        page=exams_page,
        per_page=10,
    )
    topics_pagination = paginate_clamped(
        UserTopicProgress.query
        .options(joinedload(UserTopicProgress.topic).joinedload(Topic.category))
        .filter_by(user_id=user.id)
        .order_by(UserTopicProgress.last_activity.desc(), UserTopicProgress.topic_id.desc()),
        page=topics_page,
        per_page=15,
    )
    badges_pagination = paginate_clamped(
        UserAchievement.query
        .options(joinedload(UserAchievement.achievement))
        .filter_by(user_id=user.id)
        .order_by(UserAchievement.unlocked_at.desc(), UserAchievement.achievement_id.desc()),
        page=badges_page,
        per_page=12,
    )
    last_activity = _get_user_last_activity(user)
    active_admins = count_active_admins()
    return {
        'u': user,
        'active_admins': active_admins,
        'total_attempts': stats['total_attempts'],
        'correct_attempts': stats['correct_attempts'],
        'hints_used': stats['hints_used'],
        'task_accuracy': stats['accuracy'],
        'exam_attempts': exams_pagination.items,
        'total_exams': exam_stats['total_exams'],
        'completed_exams_count': exam_stats['completed_count'],
        'passed_exams_count': exam_stats['passed_count'],
        'avg_exam_score': exam_stats['avg_percentage'],
        'recent_attempts': attempts_pagination.items,
        'topic_progress_list': topics_pagination.items,
        'user_achievements': badges_pagination.items,
        'attempts_pagination': attempts_pagination,
        'exams_pagination': exams_pagination,
        'topics_pagination': topics_pagination,
        'badges_pagination': badges_pagination,
        'total_topics_started': topics_pagination.total,
        'total_achievements_count': badges_pagination.total,
        'last_activity': last_activity,
    }
