import os
from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from app.models import UserTopicProgress, UserAchievement, utc_now
from app.services.dashboard_service import (
    build_accuracy_trend_chart,
    build_achievements_gallery,
    build_daily_goal_metrics,
    build_recent_activities,
    build_syllabus_overview,
    to_naive_utc,
)
from app.services.history_service import get_user_history_paginated
from app.services.progress_service import get_user_attempt_stats, get_user_exam_stats

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))


@dashboard_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Główny pulpit ucznia
    # W jednym widoku agreguje: postęp w podstawie programowej, dzisiejszy cel,
    # zdobyte odznaki, historię ostatnich 5 aktywności oraz 7-dniowy wykres trendu celności.
    user = current_user
    now_naive = to_naive_utc(utc_now())
    progress_records = (
        UserTopicProgress.query
        .options(joinedload(UserTopicProgress.topic))
        .filter_by(user_id=user.id)
        .all()
    )
    progress_map = {p.topic_id: p for p in progress_records if p.topic}
    syllabus = build_syllabus_overview(progress_map, now_naive)
    stats = get_user_attempt_stats(user.id)
    user_achievements = (
        UserAchievement.query
        .options(joinedload(UserAchievement.achievement))
        .filter_by(user_id=user.id)
        .order_by(UserAchievement.unlocked_at.desc(), UserAchievement.achievement_id.desc())
        .all()
    )
    earned_badges = [ua.achievement for ua in user_achievements if ua.achievement]
    earned_badges_preview = earned_badges[:4]
    achievements_gallery, total_achievements_count = build_achievements_gallery(user_achievements)
    daily = build_daily_goal_metrics(stats['today_correct'])
    recent_activities = build_recent_activities(user.id, user_achievements)
    chart_labels, chart_values, accuracy_trend = build_accuracy_trend_chart(user.id)
    return render_template(
        'dashboard/dashboard.html',
        chart_labels=chart_labels,
        chart_values=chart_values,
        accuracy_trend=accuracy_trend,
        user=user,
        total=stats['total_attempts'],
        accuracy=stats['accuracy'],
        earned_badges=earned_badges,
        earned_badges_preview=earned_badges_preview,
        achievements_gallery=achievements_gallery,
        total_achievements_count=total_achievements_count,
        correct_count=stats['correct_attempts'],
        recent_activities=recent_activities,
        **syllabus,
        **daily,
    )
@dashboard_bp.route('/history')
@login_required
def history():
    type_filter = request.args.get('type', 'all')
    status_filter = request.args.get('status') or 'all'
    page = request.args.get('page', 1, type=int)
    per_page = 20
    task_stats = get_user_attempt_stats(current_user.id)
    exam_stats = get_user_exam_stats(current_user.id)
    pagination = get_user_history_paginated(
        user_id=current_user.id,
        type_filter=type_filter,
        status_filter=status_filter,
        page=page,
        per_page=per_page,
    )
    return render_template(
        'dashboard/history.html',
        attempts=pagination.items,
        pagination=pagination,
        current_type=type_filter,
        current_status=status_filter,
        total_tasks_count=task_stats["total_attempts"],
        correct_tasks_count=task_stats["correct_attempts"],
        task_accuracy=task_stats["accuracy"],
        total_exams_count=exam_stats["completed_count"],
        passed_exams_count=exam_stats["passed_count"],
        avg_exam_score=exam_stats["avg_percentage"],
    )


from app.blueprints.dashboard import settings_routes  # noqa: E402, F401
