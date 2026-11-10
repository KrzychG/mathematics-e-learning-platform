from datetime import datetime, timedelta, timezone
from app import db
from app.models import User, Task, Attempt, Topic, Category, UserTopicProgress, ExamAttempt, UNCATEGORIZED_CATEGORY_LABEL
from app.services.progress_service import update_and_get_difficulty
from app.services.admin_service import get_filtered_users_pagination, build_user_detail_context
from app.services.history_service import clamp_page_bounds, load_entities_by_ids
from app.services.user_service import count_active_admins


def test_difficulty_streak_and_replay_protection(app_with_user, client, login_as):
    app, user_id = app_with_user
    with app.app_context():
        top = Topic(name='Max Level Topic')
        db.session.add(top)
        db.session.flush()
        db.session.add(UserTopicProgress(user_id=user_id, topic_id=top.id, current_difficulty=5, consecutive_correct=2))
        top_replay = Topic(name='Replay Topic')
        db.session.add(top_replay)
        db.session.flush()
        task = Task(topic_id=top_replay.id, question='3*3?', correct_answer='9', difficulty=1)
        db.session.add(task)
        db.session.commit()
        top_id, tr_id, task_id = top.id, top_replay.id, task.id

        assert update_and_get_difficulty(user_id, top_id, is_correct=True)['new_difficulty'] == 5
        assert UserTopicProgress.query.filter_by(user_id=user_id, topic_id=top_id).first().consecutive_correct == 0

    login_as(client, user_id)
    for _ in range(2):
        assert client.post('/check-answer', data={'task_id': task_id, 'user_answer': '9'}).status_code == 200
        with app.app_context():
            prog = UserTopicProgress.query.filter_by(user_id=user_id, topic_id=tr_id).first()
            assert prog.consecutive_correct == 1 and prog.current_difficulty == 1


def test_uncategorized_labels_and_history_parity(app_with_user, client, login_as):
    app, user_id = app_with_user
    with app.app_context():
        cat = Category(name='Algebra Spójność')
        db.session.add(cat)
        db.session.flush()
        uncat_top = Topic(name='Temat Bez Cat', category_id=None)
        db.session.add(uncat_top)
        db.session.flush()
        task = Task(topic_id=uncat_top.id, question='2+2=?', options={'A': '3', 'B': '4'}, correct_answer='B', difficulty=1)
        db.session.add(task)
        db.session.flush()

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        db.session.add_all([
            Attempt(user_id=user_id, task_id=task.id, user_answer='B', is_correct=True, created_at=now - timedelta(hours=1)),
            ExamAttempt(user_id=user_id, score=1, total_tasks=20, passed=False, created_at=now),
        ])
        db.session.commit()
        uncat_id = uncat_top.id

        assert uncat_top.category_label == UNCATEGORIZED_CATEGORY_LABEL == 'Bez kategorii'
        user = db.session.get(User, user_id)
        listed_u = get_filtered_users_pagination(search_query=user.email).items[0]
        ctx = build_user_detail_context(user, tasks_page=1, exams_page=1, topics_page=1, badges_page=1)
        assert listed_u.last_activity == ctx['last_activity'] and ctx['active_admins'] == count_active_admins()
        assert clamp_page_bounds(0, 5, 10) == (1, 1) and clamp_page_bounds(25, 10, 10) == (3, 3)
        assert load_entities_by_ids(Task.query, Task.id, [task.id])[task.id].id == task.id

    login_as(client, user_id)
    for url in ('/dashboard', f'/practice/{uncat_id}', '/history'):
        html = client.get(url).data.decode('utf-8')
        assert 'Bez kategorii' in html and 'Inne zagadnienia' not in html
