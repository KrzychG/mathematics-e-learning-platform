import json
import pytest
from app import db
from app.models import Topic, Category, Task


@pytest.fixture
def app_and_client(app, client, user_factory):
    user = user_factory(email='graph_student@test.com', first_name='Zdający', password_hash='scrypt:dummy', is_admin=False)
    cat = Category(name="V. Funkcje Test")
    db.session.add(cat)
    db.session.commit()
    topic = Topic(name="Wykres funkcji kwadratowej", description="Testowy", category_id=cat.id, theory="<p>Teoria</p>")
    db.session.add(topic)
    db.session.commit()
    return app, client, user, topic


def test_task_graph_spec_property(app_and_client):
    app, _, _, topic = app_and_client
    with app.app_context():
        spec = {"formula": "-(x-2)^2 + 4", "points": [{"x": 2, "y": 4, "label": "W(2, 4)"}], "xRange": [-4, 6], "yRange": [-5, 6]}
        t1 = Task(topic_id=topic.id, question="Q1", options=json.dumps({"A": "1"}), correct_answer="A", difficulty=2, graph_data=json.dumps(spec))
        t2 = Task(topic_id=topic.id, question="Q2", options=json.dumps({"A": "1"}), correct_answer="A", difficulty=1, graph_data=None)
        t3 = Task(topic_id=topic.id, question="Q3", options=json.dumps({"A": "1"}), correct_answer="A", difficulty=1, graph_data="bad json")
        db.session.add_all([t1, t2, t3])
        db.session.commit()

        reloaded = db.session.get(Task, t1.id)
        assert reloaded.graph_spec["formula"] == "-(x-2)^2 + 4" and reloaded.graph_spec["points"][0]["x"] == 2
        assert db.session.get(Task, t2.id).graph_spec is None
        assert db.session.get(Task, t3.id).graph_spec is None


def test_graph_explorer_views(app_and_client, login_as):
    _, client, user, _ = app_and_client
    resp = client.get('/graph-explorer')
    assert resp.status_code == 302 and '/login' in resp.headers.get('Location', '')

    login_as(client, user)
    resp = client.get('/graph-explorer?family=quadratic')
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    for expected in [
        'Wykresy funkcji', 'explorerGraphContainer', 'graph/engine.js', 'graph/explorer.js', 'Układ Kartezjański',
        'Współczynnik $a$', 'singleFormulaInput', 'modeBtn_custom', 'modeBtn_linear', 'modeBtn_quadratic',
        'graphActiveLegend', 'mathAnalysisPills', 'Predefiniowane wykresy funkcji', 'preset-pill',
        'data-fn="2*x - 3"', 'data-fn="x^2 - 4"', 'data-fn="abs(x)"', 'data-fn="sin(x)"', 'data-fn="1/x"', 'data-fn="2^x"'
    ]:
        assert expected in html


def test_get_task_and_check_answer_with_graph_spec(app_and_client, login_as):
    app, client, user, _ = app_and_client
    login_as(client, user)
    spec = {"formula": "-(x-2)^2 + 4", "points": [{"x": 2, "y": 4, "label": "W(2, 4)"}], "xRange": [-3, 4], "yRange": [-4, 4]}
    with app.app_context():
        top = Topic(name="Wykres specjalny", theory="<p>T</p>")
        db.session.add(top)
        db.session.flush()
        task = Task(topic_id=top.id, question="Odczytaj wierzchołek", options=json.dumps({"A": "W(2, 4)", "B": "0", "C": "1", "D": "2"}), correct_answer="A", difficulty=1, graph_data=json.dumps(spec))
        db.session.add(task)
        db.session.commit()
        t_id, top_id = task.id, top.id

    resp = client.get(f'/practice/{top_id}/get-task', headers={"X-Requested-With": "XMLHttpRequest"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True and data["graph_spec"]["formula"] == "-(x-2)^2 + 4"

    resp_check = client.post('/check-answer', data={"task_id": t_id, "user_answer": "A"})
    assert resp_check.status_code == 200
    html = resp_check.get_data(as_text=True)
    assert 'INTERPRETACJA GRAFICZNA:' in html and 'resultGraphContainer' in html and 'graph/engine.js' in html
