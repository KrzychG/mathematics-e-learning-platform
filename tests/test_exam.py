import pytest
from app import db
from app.models import Topic, Category, Task, ExamAttempt
from app.services.sanitizer_service import format_math


@pytest.fixture
def exam_client(app, client, user_factory, login_as):
    u1 = user_factory(email='zdajacy@example.com', first_name='Kamil', password_hash='hash')
    u2 = user_factory(email='inny@example.com', first_name='Anna', password_hash='hash')
    login_as(client, u1)
    return client, u1.id, u2.id, app


def test_exam_lobby_and_scratchpad(exam_client, admin_user, login_as):
    client, _, _, app = exam_client
    assert client.get('/exam/lobby').status_code == 200
    html = client.get('/exam/lobby').data.decode('utf-8')
    for item in ('Egzamin Testowy', 'Arkusz Próbny: 20 Zadań Zamkniętych', '20 pytań', 'Próg zdawalności', '30%', 'Rozpocznij nowy egzamin',
                 'scratchpadDrawer', 'scratchpad-dock', 'scratchpadCanvas', 'Brudnopis', 'scratchpadClearBtn', 'scratchpad.js'):
        assert item in html

    for c in (client, login_as(app.test_client(), admin_user)):
        url = '/dashboard' if c == client else '/admin'
        assert 'scratchpadDrawer' not in c.get(url).data.decode('utf-8')


def test_start_exam_and_answer_lifecycle(exam_client, login_as):
    client, u1_id, u2_id, app = exam_client
    app_client = app.test_client()
    assert app_client.get('/exam/lobby').status_code == 302

    assert client.post('/exam/start', follow_redirects=True).status_code == 200
    with app.app_context():
        att = ExamAttempt.query.filter_by(user_id=u1_id).first()
        att_id, tid = att.id, att.task_ids[0]
        assert att and not att.is_completed and len(att.task_ids) == 20

    assert client.post('/exam/start', follow_redirects=True).status_code == 200
    with app.app_context():
        assert ExamAttempt.query.filter_by(user_id=u1_id).count() == 1

    assert client.post(f'/exam/session/{att_id}/save-answer', json={'task_id': tid, 'selected_option': 'XYZ'}).status_code == 400
    assert client.post(f'/exam/session/{att_id}/save-answer', json={'task_id': tid, 'selected_option': 'A'}).status_code == 200
    with app.app_context():
        assert db.session.get(ExamAttempt, att_id).answers[str(tid)] == 'A'

    other_client = login_as(app.test_client(), u2_id)
    assert other_client.get(f'/exam/session/{att_id}').status_code == 403
    assert other_client.post(f'/exam/session/{att_id}/save-answer', json={'task_id': tid, 'selected_option': 'A'}).status_code == 403


def test_submit_exam_scoring_thresholds(exam_client):
    client, u1_id, _, app = exam_client
    for correct_count, expect_passed, expected_badge, expected_score_text in [
        (6, True, 'EGZAMIN ZDANY', '6 / 20'),
        (5, False, 'EGZAMIN NIEZALICZONY', '5 / 20'),
    ]:
        client.post('/exam/start')
        with app.app_context():
            att = ExamAttempt.query.filter_by(user_id=u1_id, is_completed=False).order_by(ExamAttempt.id.desc()).first()
            att_id = att.id
            answers = [(t.id, t.correct_answer) for t in [db.session.get(Task, tid) for tid in att.task_ids]]

        for tid, corr in answers[:correct_count]:
            client.post(f'/exam/session/{att_id}/save-answer', json={'task_id': tid, 'selected_option': corr})
        for tid, corr in answers[correct_count:]:
            client.post(f'/exam/session/{att_id}/save-answer', json={'task_id': tid, 'selected_option': 'B' if corr == 'A' else 'A'})

        html = client.post(f'/exam/session/{att_id}/submit', follow_redirects=True).data.decode('utf-8')
        assert expected_badge in html and expected_score_text in html
        with app.app_context():
            final = db.session.get(ExamAttempt, att_id)
            assert final.score == correct_count and final.passed is expect_passed


def test_exam_views_formatting_and_xss(exam_client):
    assert format_math(r'\frac{1}{2}') == r'\(\frac{1}{2}\)'
    client, u1_id, _, app = exam_client
    with app.app_context():
        cat = Category(name='Bezpieczeństwo Egzamin')
        db.session.add(cat)
        db.session.flush()
        top = Topic(name='Test XSS', category_id=cat.id)
        db.session.add(top)
        db.session.flush()
        task = Task(topic_id=top.id, question='Oblicz $$2+2$$<script>alert("q_xss")</script>',
                    options={'A': '4', 'B': '3', 'C': '2', 'D': '1'}, correct_answer='A', difficulty=1,
                    explanation='Wyjaśnienie: $$2+2=4$$<img src=x onerror="alert(1)"><script>alert("e_xss")</script>')
        db.session.add(task)
        db.session.flush()
        att = ExamAttempt(user_id=u1_id, title='Test XSS', score=1, total_tasks=1, passed=True, is_completed=False, task_ids=[task.id], answers={str(task.id): 'A'})
        db.session.add(att)
        db.session.commit()
        att_id = att.id

    h_sess = client.get(f'/exam/session/{att_id}').get_data(as_text=True)
    assert 'Oblicz $$2+2$$' in h_sess and 'q_xss' not in h_sess and '<script>alert' not in h_sess
    assert 'flex-wrap' in h_sess

    client.post(f'/exam/session/{att_id}/submit')
    h_res = client.get(f'/exam/result/{att_id}').get_data(as_text=True)
    assert 'Wyjaśnienie: $$2+2=4$$' in h_res
    for x in ('q_xss', 'e_xss', 'onerror=', '<img'):
        assert x not in h_res


def test_exam_result_cards_and_generating(exam_client):
    client, u1_id, _, app = exam_client
    assert 'Trwa generowanie zadań' in client.get('/exam/generating').data.decode('utf-8')
    assert client.post('/exam/start', headers={'Accept': 'application/json'}).get_json()['success'] is True

    with app.app_context():
        att_unans = ExamAttempt(user_id=u1_id, title='Unans', score=0, total_tasks=20, passed=False, is_completed=True, task_ids=[1], answers={})
        att_orph = ExamAttempt(user_id=u1_id, title='Orph', score=0, total_tasks=20, passed=False, is_completed=True, task_ids=[999901], answers={})
        db.session.add_all([att_unans, att_orph])
        db.session.commit()
        unans_id, orph_id = att_unans.id, att_orph.id

    res_unans = client.get(f'/exam/result/{unans_id}').data.decode('utf-8')
    assert 'Brak odpowiedzi (0 pkt)' in res_unans
    assert 'Prawidłowa odpowiedź' in res_unans
    assert 'border-dashed' in res_unans
    assert 'id="examEmptyBreakdownCard"' in client.get(f'/exam/result/{orph_id}').data.decode('utf-8')
