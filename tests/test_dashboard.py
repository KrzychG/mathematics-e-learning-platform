import re
import json
from datetime import datetime, timezone, timedelta
from app import db
from app.models import Category, Topic, Task, Attempt, UserTopicProgress, Achievement, UserAchievement, ExamAttempt
from app.services.dashboard_service import to_naive_utc
from app.services.timezone_service import format_activity_time
from app.services.progress_service import (
    ACHIEVEMENTS_CATALOG, sync_achievements_catalog,
    _check_and_award_achievements
)


def test_dashboard_accuracy_and_knowledge_structure(student_client, student_user):
    h0 = student_client.get('/dashboard').data.decode('utf-8')
    assert 'Skuteczność Odpowiedzi' in h0 and json.loads(re.search(r'data-values=\'([^\']*)\'', h0).group(1)) == [0]*7

    cat = Category(name="Algebra i Funkcje")
    db.session.add(cat)
    db.session.flush()
    t1 = Topic(name="Działania arytmetyczne", category_id=cat.id)
    t2 = Topic(name="Funkcja kwadratowa", category_id=cat.id)
    db.session.add_all([t1, t2])
    db.session.flush()
    task = Task(topic_id=t1.id, question="2+3", correct_answer="5")
    db.session.add(task)
    db.session.flush()
    db.session.add_all([
        Attempt(user_id=student_user.id, task_id=task.id, user_answer='5', is_correct=True, created_at=datetime.now(timezone.utc)),
        UserTopicProgress(user_id=student_user.id, topic_id=t1.id, current_difficulty=3),
    ])
    db.session.commit()

    h1 = student_client.get('/dashboard').data.decode('utf-8')
    assert json.loads(re.search(r'data-values=\'([^\']*)\'', h1).group(1))[-1] == 100.0 and '+100.0%' in h1
    for s in ('Struktura Wiedzy', 'Algebra i Funkcje', 'Działania arytmetyczne', 'Poziom 3/5', 'Funkcja kwadratowa', 'Nierozpoczęte'):
        assert s in h1


def test_dashboard_timestamps_and_activities(student_client, student_user):
    assert to_naive_utc(None) == datetime.min
    naive = datetime(2026, 10, 28, 12, 0)
    assert to_naive_utc(naive) == to_naive_utc(datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc)) == naive
    assert format_activity_time(None) == "Brak daty" and "Dzisiaj" in format_activity_time(datetime.now(timezone.utc))

    t = Topic(name="Temat testowy")
    a1, a2 = Achievement(name="Zwycięzca", trigger_condition="win", icon_class="bi-trophy"), Achievement(name="Mistrz", trigger_condition="master", icon_class="bi-star")
    db.session.add_all([t, a1, a2])
    db.session.flush()
    task = Task(topic_id=t.id, question="1+1", correct_answer="2")
    db.session.add(task)
    db.session.flush()
    db.session.add_all([
        Attempt(user_id=student_user.id, task_id=task.id, is_correct=True, created_at=datetime(2026, 10, 27, 10, 0)),
        Attempt(user_id=student_user.id, task_id=task.id, is_correct=False, created_at=datetime.now(timezone.utc)),
        Attempt(user_id=student_user.id, task_id=task.id, is_correct=True, created_at=None),
        UserAchievement(user_id=student_user.id, achievement_id=a1.id, unlocked_at=datetime.now(timezone.utc)),
        UserAchievement(user_id=student_user.id, achievement_id=a2.id, unlocked_at=datetime(2026, 10, 26, 15, 30)),
    ])
    db.session.commit()

    html = student_client.get('/dashboard').data.decode('utf-8')
    for term in ('Zadanie zaliczone: Temat testowy', 'Błąd w obliczeniach: Temat testowy', 'Zdobyto osiągnięcie: Zwycięzca', 'Zdobyto osiągnięcie: Mistrz'):
        assert term in html


def test_daily_goal_and_recommendation(student_client, student_user):
    topic = Topic(name="Cel dzienny")
    db.session.add(topic)
    db.session.flush()
    task = Task(topic_id=topic.id, question="2*2", correct_answer="4")
    db.session.add(task)
    db.session.flush()

    now = datetime.now(timezone.utc)
    for _ in range(4):
        db.session.add(Attempt(user_id=student_user.id, task_id=task.id, user_answer='4', is_correct=True, created_at=now))
    db.session.commit()
    assert '4 / 5 zadań' in student_client.get('/dashboard').data.decode('utf-8')

    db.session.add(Attempt(user_id=student_user.id, task_id=task.id, user_answer='4', is_correct=True, created_at=now))
    db.session.commit()
    h2 = student_client.get('/dashboard').data.decode('utf-8')
    assert '5 / 5 zadań' in h2 and 'bi-check-circle-fill text-success' in h2 and 'id="randomTaskDashboardBtn"' in h2


def test_achievements_catalog_and_triggers(student_client, student_user, user_factory):
    assert len(ACHIEVEMENTS_CATALOG) == 20 and len({a['trigger_condition'] for a in ACHIEVEMENTS_CATALOG}) == 20
    assert sync_achievements_catalog() == 20 and sync_achievements_catalog() == 0 and Achievement.query.count() == 20

    user = user_factory(email='ach20@example.com', first_name='Kasia', password_hash='secret')
    cat = Category(name='Analiza')
    db.session.add(cat)
    db.session.flush()
    topics = [Topic(name=f'Temat Ach {i}', category_id=cat.id) for i in range(10)]
    db.session.add_all(topics)
    db.session.flush()
    task = Task(topic_id=topics[0].id, question='1+1', correct_answer='2')
    db.session.add(task)
    db.session.flush()

    now = datetime.now(timezone.utc)
    for _ in range(10):
        db.session.add(Attempt(user_id=user.id, task_id=task.id, user_answer='2', is_correct=True, created_at=now))
    for d in range(1, 7):
        db.session.add(Attempt(user_id=user.id, task_id=task.id, user_answer='2', is_correct=True, created_at=now - timedelta(days=d)))
    for _ in range(4):
        db.session.add(Attempt(user_id=user.id, task_id=task.id, user_answer='2', is_correct=True, created_at=now - timedelta(days=1)))
    for idx, t in enumerate(topics):
        db.session.add(UserTopicProgress(user_id=user.id, topic_id=t.id, current_difficulty=5 if idx < 3 else 2))
    db.session.add(ExamAttempt(user_id=user.id, title='E', score=17, total_tasks=20, passed=True, is_completed=True))
    db.session.commit()

    unlocked = {b.trigger_condition for b in _check_and_award_achievements(user.id, hit_streak_3=True)}
    for req in ('first_task', 'streak_3', 'daily_goal_5', 'daily_goal_10', 'attempts_10', 'correct_10', 'accuracy_80', 'level_5', 'exam_passed'):
        assert req in unlocked

    all_ach = Achievement.query.order_by(Achievement.id.asc()).all()
    base_time = datetime(2026, 11, 1, 10, 0, tzinfo=timezone.utc)
    for idx, ach in enumerate(all_ach[:6]):
        db.session.add(UserAchievement(user_id=student_user.id, achievement_id=ach.id, unlocked_at=base_time + timedelta(hours=idx)))
    db.session.commit()

    html = student_client.get('/dashboard').data.decode('utf-8')
    assert '6 / 20' in html and 'Wyświetl wszystkie (20)' in html and 'id="allAchievementsModal"' in html
