"""
Serwis Pulpitu Ucznia i Wizualizacji Danych 
Przygotowuje dane analityczne dla widoku głównego ucznia 
Oblicza wykres skumulowanej skuteczności z ostatnich 7 dni z podziałem na dni w czasie lokalnym
Buduje oś czasu Ostatnia Aktywność
Przetwarza stan opanowania materiału wg 13 kategorii sylabusa maturalnego i rekomenduje powtórki
Oblicza progres realizacji celu dziennego
"""

from collections import Counter
from datetime import datetime, timedelta
from flask import url_for
from sqlalchemy import case, func
from sqlalchemy.orm import joinedload

from app import db
from app.models import (
    Achievement,
    Attempt,
    Category,
    Task,
    Topic,
    UNCATEGORIZED_CATEGORY_LABEL,
    UserAchievement,
    UserTopicProgress,
)
from app.services.progress_service import get_user_attempt_stats
from app.services.timezone_service import (
    format_activity_time,
    format_local_datetime,
    get_local_now,
    to_local_time,
    to_naive_utc,
    to_utc_iso,
)

CATEGORY_ICONS = {
    'liczby': 'bi-calculator',
    'wyrażenia': 'bi-code-slash',
    'równania': 'bi-distribute-horizontal',
    'układy': 'bi-grid-1x2',
    'funkcje': 'bi-graph-up',
    'ciągi': 'bi-123',
    'trygonometria': 'bi-triangle',
    'planimetria': 'bi-pentagon',
    'analityczna': 'bi-bounding-box-circles',
    'stereometria': 'bi-box',
    'kombinatoryka': 'bi-dice-5',
    'prawdopodobieństwa': 'bi-pie-chart',
    'statystyka': 'bi-pie-chart',
    'optymalizacja': 'bi-speedometer2',
    'pochodne': 'bi-speedometer2',
    'rachunek': 'bi-speedometer2',
}

def get_category_icon(category_name: str) -> str:
    name_lower = (category_name or '').lower()
    return next((icon for key, icon in CATEGORY_ICONS.items() if key in name_lower), 'bi-journal-bookmark')


def evaluate_topic_progress(topic: Topic, progress: UserTopicProgress | None, now_naive: datetime) -> dict:
    # Wyznacza status opanowania tematu w panelu ucznia
    # - 'mastered': wbity maksymalny 5. poziom
    # - 'needs-review': uczeń ma serię min. 2 błędów z rzędu albo nie powtarzał materiału od 2 tygodni
    # - 'in-progress': temat rozpoczęty, brak sygnałów o problemach
    # - 'not-started': brak jakichkolwiek prób w tym temacie
    if progress:
        lvl = int(progress.current_difficulty or 1)
        percent = progress.mastery_percent
        last_act_naive = to_naive_utc(progress.last_activity)
        days_since_act = (now_naive - last_act_naive).days if progress.last_activity else 999
        is_stale = days_since_act >= 14
        is_struggling = (progress.consecutive_wrong or 0) >= 2
        if lvl >= 5:
            status = 'mastered'
        elif is_struggling or is_stale:
            status = 'needs-review'
        else:
            status = 'in-progress'
    else:
        lvl = 0
        percent = 0
        status = 'not-started'
    return {
        'id': topic.id,
        'name': topic.name,
        'description': topic.description or '',
        'level': lvl,
        'percent': percent,
        'status': status,
    }


def process_category_group(cat: dict, progress_map: dict, now_naive: datetime) -> dict:
    cat_topics_data = [
        evaluate_topic_progress(t, progress_map.get(t.id), now_naive)
        for t in sorted(cat['topics'], key=lambda t: t.id)
    ]
    counts = Counter(t['status'] for t in cat_topics_data)
    cat_level_sum = sum(t['level'] for t in cat_topics_data)
    total_cat = len(cat_topics_data)
    cat_percent = int((cat_level_sum / (total_cat * 5.0)) * 100) if total_cat > 0 else 0
    return {
        'id': cat['id'],
        'name': cat['name'],
        'icon': get_category_icon(cat['name']),
        'topics': cat_topics_data,
        'total_count': total_cat,
        'completed_count': counts['mastered'],
        'in_progress_count': counts['in-progress'],
        'needs_review_count': counts['needs-review'],
        'not_started_count': counts['not-started'],
        'percent': cat_percent,
        'level_sum': cat_level_sum,
        'first_topic_id': cat_topics_data[0]['id'] if cat_topics_data else None,
    }


def build_syllabus_overview(progress_map: dict, now_naive: datetime) -> dict:
    # Agreguje całe drzewo podstawy programowej
    # i wylicza globalny procent opanowania materiału (suma poziomów / (liczba tematów * 5)).
    categories, uncategorized_topics = Category.get_syllabus_tree()
    all_cat_groups = [{'id': cat.id, 'name': cat.name, 'topics': list(cat.topics)} for cat in categories]
    if uncategorized_topics:
        all_cat_groups.append({'id': 0, 'name': UNCATEGORIZED_CATEGORY_LABEL, 'topics': uncategorized_topics})
    knowledge_categories = [process_category_group(cat, progress_map, now_naive) for cat in all_cat_groups]
    total_topics = sum(c['total_count'] for c in knowledge_categories)
    level_sum = sum(c['level_sum'] for c in knowledge_categories)
    overall_percent = int(round((level_sum / (total_topics * 5.0)) * 100)) if total_topics > 0 else 0
    return {
        'knowledge_categories': knowledge_categories,
        'total_topics_count': total_topics,
        'mastered_topics_count': sum(c['completed_count'] for c in knowledge_categories),
        'in_progress_topics_count': sum(c['in_progress_count'] for c in knowledge_categories),
        'needs_review_topics_count': sum(c['needs_review_count'] for c in knowledge_categories),
        'not_started_topics_count': sum(c['not_started_count'] for c in knowledge_categories),
        'overall_syllabus_percent': overall_percent,
    }
def build_daily_goal_metrics(today_correct_count: int, daily_goal: int = 5) -> dict:
    daily_progress = min(today_correct_count, daily_goal)
    daily_completed = today_correct_count >= daily_goal
    daily_percent = min(100, int((daily_progress / daily_goal) * 100))
    return {
        'daily_goal': daily_goal,
        'daily_progress': daily_progress,
        'daily_completed': daily_completed,
        'daily_percent': daily_percent,
    }


def build_recent_activities(user_id: int, user_achievements: list) -> list[dict]:
    recent_attempts = (
        Attempt.query
        .options(joinedload(Attempt.task).joinedload(Task.topic))
        .filter_by(user_id=user_id)
        .order_by(Attempt.created_at.desc(), Attempt.id.desc())
        .limit(5)
        .all()
    )
    def _make_activity(title, badge_text, badge_class, icon, timestamp, url=None, item_class=""):
        return {
            "title": title,
            "badge_text": badge_text,
            "badge_class": badge_class,
            "icon": icon,
            "item_class": item_class,
            "timestamp": timestamp or datetime.min,
            "time_str": format_activity_time(timestamp),
            "time_iso": to_utc_iso(timestamp),
            "url": url,
        }
    activities = []
    for att in recent_attempts:
        topic_name = att.task.topic.name if (att.task and att.task.topic) else "Zadanie matematyczne"
        topic_id = att.task.topic_id if att.task else None
        activities.append(_make_activity(
            title=f"Zadanie zaliczone: {topic_name}" if att.is_correct else f"Błąd w obliczeniach: {topic_name}",
            badge_text="Dobrze" if att.is_correct else "Błąd",
            badge_class="text-success" if att.is_correct else "text-danger",
            icon="bi-check-lg" if att.is_correct else "bi-x-lg",
            timestamp=att.created_at,
            url=url_for('learning.learning_desk', topic_id=topic_id) if topic_id else None,
        ))
    for ua in user_achievements:
        if ua.achievement:
            activities.append(_make_activity(
                title=f"Zdobyto osiągnięcie: {ua.achievement.name}",
                badge_text="Odznaka",
                badge_class="text-warning",
                icon="bi-award",
                item_class="border-secondary",
                timestamp=ua.unlocked_at,
            ))
    activities.sort(key=lambda x: to_naive_utc(x["timestamp"]), reverse=True)
    return activities[:5]


def build_accuracy_trend_chart(user_id: int) -> tuple[list[str], list[float], float]:
    # Wykres skumulowanej skuteczności z ostatnich 7 dni
    # Żeby nie przeliczać historii od nowa dla każdego słupka z osobna,
    # pobieramy stan bazowy sprzed 7 dni jednym zapytaniem, a potem
    # lecimy dzień po dniu do przodu i inkrementujemy licznik. Grupowanie dni
    # robimy w czasie lokalnym użytkownika.
    now_local = get_local_now()
    today = now_local.date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    earliest_day = days[0]
    earliest_local_midnight = datetime.combine(earliest_day, datetime.min.time(), tzinfo=now_local.tzinfo)
    cutoff_utc = to_naive_utc(earliest_local_midnight)
    base_stats = (
        db.session.query(
            func.count(Attempt.id),
            func.coalesce(func.sum(case((Attempt.is_correct.is_(True), 1), else_=0)), 0),
        )
        .filter(Attempt.user_id == user_id, Attempt.created_at < cutoff_utc)
        .first()
    )
    base_total = int(base_stats[0] or 0)
    base_correct = int(base_stats[1] or 0)
    recent_attempts = (
        Attempt.query
        .with_entities(Attempt.is_correct, Attempt.created_at)
        .filter(Attempt.user_id == user_id, Attempt.created_at >= cutoff_utc)
        .order_by(Attempt.created_at.asc())
        .all()
    )
    daily_counts = {d: [0, 0] for d in days}
    for is_correct, created_at in recent_attempts:
        if not created_at:
            continue
        att_date = to_local_time(created_at).date()
        if att_date in daily_counts:
            daily_counts[att_date][0] += 1
            if is_correct:
                daily_counts[att_date][1] += 1
        elif att_date < earliest_day:
            base_total += 1
            if is_correct:
                base_correct += 1
    chart_labels = []
    chart_values = []
    running_total = base_total
    running_correct = base_correct
    for d in days:
        chart_labels.append('Dziś' if d == today else 'Wczoraj' if d == today - timedelta(days=1) else d.strftime('%d.%m'))
        day_total, day_correct = daily_counts[d]
        running_total += day_total
        running_correct += day_correct
        chart_values.append(round((running_correct / running_total) * 100, 1) if running_total > 0 else 0.0)
    yesterday_acc = chart_values[-2] if len(chart_values) >= 2 else 0.0
    accuracy_trend = round(chart_values[-1] - yesterday_acc, 1)
    return chart_labels, chart_values, accuracy_trend


def build_achievements_gallery(user_achievements: list) -> tuple[list[dict], int]:
    all_achievements = Achievement.query.order_by(Achievement.id.asc()).all()
    unlocked_map = {ua.achievement_id: ua for ua in user_achievements if ua.achievement_id}
    gallery = []
    for ach in all_achievements:
        ua = unlocked_map.get(ach.id)
        gallery.append({
            "achievement": ach,
            "unlocked": ua is not None,
            "unlocked_at": ua.unlocked_at if ua else None,
        })
    return gallery, len(all_achievements)


def build_student_settings_stats(user) -> dict:
    attempt_stats = get_user_attempt_stats(user.id)
    return {
        'total_attempts': attempt_stats['total_attempts'],
        'accuracy': attempt_stats['accuracy'],
        'badges_count': UserAchievement.query.filter_by(user_id=user.id).count(),
        'member_since': format_local_datetime(user.created_at, '%d.%m.%Y') if user.created_at else '-',
    }
