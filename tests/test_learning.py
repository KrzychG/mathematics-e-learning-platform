import pytest
from app import db
from app.models import Topic, Category, Task, Attempt, UserTopicProgress
from app.services.preset_task_service import EXAM_TOPIC_NAME


@pytest.fixture
def test_client_and_user(app, client, user_factory, login_as):
    user = user_factory(email='student_learning@example.com', first_name='Tomasz', password_hash='hash')
    cat = Category(name='Kategoria Testowa')
    db.session.add(cat)
    db.session.flush()

    top_theory = Topic(category_id=cat.id, name='Temat z teoria', description='Opis',
                       theory='<h4>Wlasnosci poteg</h4><p>Wzor: $$a^n \\cdot a^m = a^{n+m}$$</p>')
    top_empty = Topic(category_id=cat.id, name='Temat pusty', description='Opis', theory='')
    db.session.add_all([top_theory, top_empty])
    db.session.commit()

    login_as(client, user)
    return client, top_theory.id, top_empty.id, app, user.id


def test_learning_desk_views_and_fallbacks(test_client_and_user):
    c, top_theory_id, top_empty_id, _, _ = test_client_and_user

    h_theory = c.get(f'/learning/{top_theory_id}').data.decode('utf-8')
    assert '<h4>Wlasnosci poteg</h4>' in h_theory and '$$a^n \\cdot a^m = a^{n+m}$$' in h_theory
    assert 'chapter1' not in h_theory and 'ignore missing' not in h_theory
    assert 'workspace-content-container' in h_theory and 'mx-auto' in h_theory and 'id="learningDeskWrapper"' in h_theory

    assert 'Brak treści teoretycznej' in c.get(f'/learning/{top_empty_id}').data.decode('utf-8')
    assert 'Wybrany temat nie istnieje' in c.get('/learning/99999', follow_redirects=True).data.decode('utf-8')


def test_unauthenticated_redirects(client):
    assert client.get('/learning/1').status_code == 302
    assert client.get('/practice/random').status_code == 302


def test_practice_idempotency_and_clearing(test_client_and_user):
    client, topic_id, _, app, user_id = test_client_and_user
    with app.app_context():
        tasks_before = Task.query.count()

    assert client.get(f'/practice/{topic_id}?sync=1').status_code == 200
    with app.app_context():
        tasks_after_first = Task.query.count()
        assert tasks_after_first == tasks_before + 1

    for _ in range(2):
        assert client.get(f'/practice/{topic_id}').status_code == 200
        with app.app_context():
            assert Task.query.count() == tasks_after_first

    d1 = client.get(f'/practice/{topic_id}/get-task').get_json()
    assert d1['success'] and d1['reused'] and d1['task_id'] is not None

    with app.app_context():
        corr = db.session.get(Task, d1['task_id']).correct_answer
    assert client.post('/check-answer', data={'task_id': d1['task_id'], 'user_answer': corr}).status_code == 200

    with app.app_context():
        assert Attempt.query.filter_by(user_id=user_id, task_id=d1['task_id']).first().is_correct

    d_next = client.get(f'/practice/{topic_id}/get-task').get_json()
    assert d_next['success'] and d_next['task_id'] != d1['task_id']


def test_random_practice_handles_empty_syllabus(client, student_user, login_as):
    login_as(client, student_user)
    assert 'Brak tematów w bazie danych' in client.get('/practice/random', follow_redirects=True).data.decode('utf-8')


def test_random_practice_full_flow(test_client_and_user):
    c, t1_id, t2_id, app, user_id = test_client_and_user
    with app.app_context():
        cat2 = Category(name='Druga Cat')
        db.session.add(cat2)
        db.session.flush()
        exam_top = Topic(category_id=cat2.id, name=EXAM_TOPIC_NAME)
        db.session.add(exam_top)
        db.session.commit()
        exam_top_id = exam_top.id

    resp_init = c.get('/practice/random?new=1', follow_redirects=False)
    assert resp_init.status_code == 302 and resp_init.headers['Location'].endswith('/practice/random')

    d1 = c.get('/practice/random/get-task', headers={'X-Requested-With': 'XMLHttpRequest'}).get_json()
    assert d1['success'] and d1['topic_id'] in (t1_id, t2_id) and d1['topic_id'] != exam_top_id

    assert c.get('/practice/random/get-task').get_json()['reused']
    assert c.get('/practice/random/get-task?force_new=1').status_code == 400

    d2 = c.get('/practice/random/get-task?force_new=1', headers={'X-Requested-With': 'XMLHttpRequest'}).get_json()
    assert d2['success'] and not d2['reused'] and d2['task_id'] != d1['task_id'] and d2['topic_id'] != exam_top_id

    with app.app_context():
        task2 = db.session.get(Task, d2['task_id'])
        corr, drawn_top = task2.correct_answer, task2.topic_id
    html_res = c.post('/check-answer', data={'task_id': d2['task_id'], 'user_answer': corr, 'mode': 'random'}).data.decode('utf-8')
    assert 'Losuj kolejne zadanie' in html_res and '/practice/random?new=1' in html_res

    with app.app_context():
        assert UserTopicProgress.query.filter_by(user_id=user_id, topic_id=drawn_top).first().consecutive_correct == 1


@pytest.mark.parametrize('payload,expected_code', [
    ({'task_id': 'abc', 'user_answer': 'A'}, 400),
    ({'task_id': '999999', 'user_answer': 'A'}, 404),
])
def test_check_answer_validation(test_client_and_user, payload, expected_code):
    c, *_ = test_client_and_user
    assert c.post('/check-answer', data=payload).status_code == expected_code
