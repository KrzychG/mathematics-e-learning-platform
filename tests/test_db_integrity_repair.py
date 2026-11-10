import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Attempt, Category, Task, Topic, UserTopicProgress


@pytest.fixture
def integrity_app(app, admin_user, student_user):
    return app, admin_user.id, student_user.id


def test_database_category_and_topic_integrity(integrity_app):
    app, _, _ = integrity_app
    with app.app_context():
        cat = Category(name='Algebra DDL')
        db.session.add(cat)
        db.session.flush()
        topic = Topic(name='Równania DDL', category_id=cat.id)
        db.session.add(topic)
        db.session.commit()
        cat_id, topic_id = cat.id, topic.id

        db.session.execute(text("DELETE FROM categories WHERE id = :cid"), {"cid": cat_id})
        db.session.commit()
        db.session.expunge_all()
        reloaded = db.session.get(Topic, topic_id)
        assert reloaded is not None and reloaded.category_id is None

        cat1, cat2 = Category(name='Dział A'), Category(name='Dział B')
        db.session.add_all([cat1, cat2])
        db.session.flush()
        db.session.add_all([
            Topic(name='Wspólna nazwa', category_id=cat1.id),
            Topic(name='Wspólna nazwa', category_id=cat2.id),
            Topic(name='Bez kategorii Unikalny', category_id=None),
        ])
        db.session.commit()
        db.session.add(Topic(name='Bez kategorii Unikalny', category_id=None))
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


def test_admin_delete_category_actions(integrity_app, client, login_as):
    app, admin_id, student_id = integrity_app
    login_as(client, admin_id)

    for action, expect_topic in [('detach', True), ('delete_all', False)]:
        with app.app_context():
            cat = Category(name=f'Kat {action}')
            db.session.add(cat)
            db.session.flush()
            topic = Topic(name=f'Temat {action}', category_id=cat.id)
            db.session.add(topic)
            db.session.flush()
            task = Task(topic_id=topic.id, question='2+2=?', options={'A': '3', 'B': '4'}, correct_answer='B', difficulty=1)
            db.session.add(task)
            db.session.flush()
            db.session.add_all([
                Attempt(user_id=student_id, task_id=task.id, user_answer='B', is_correct=True),
                UserTopicProgress(user_id=student_id, topic_id=topic.id, current_difficulty=2),
            ])
            db.session.commit()
            cat_id, topic_id, task_id = cat.id, topic.id, task.id

        resp = client.post(f'/admin/category/{cat_id}/delete', data={'topic_action': action}, follow_redirects=True)
        assert resp.status_code == 200

        with app.app_context():
            assert db.session.get(Category, cat_id) is None
            top = db.session.get(Topic, topic_id)
            if expect_topic:
                assert top is not None and top.category_id is None
            else:
                assert top is None and db.session.get(Task, task_id) is None
                assert Attempt.query.filter_by(task_id=task_id).count() == 0
                assert UserTopicProgress.query.filter_by(topic_id=topic_id).count() == 0
