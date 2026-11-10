import json
from unittest.mock import patch, MagicMock
import pytest
from app import db
from app.models import Topic, Task
from app.services.llm_service import generate_math_task, _normalize_llm_options, are_tasks_too_similar


def test_llm_service_normalizes_options(app_with_user):
    app, _ = app_with_user
    with app.app_context():
        t = Topic(name="Test Topic Options")
        db.session.add(t)
        db.session.commit()

        cases = [
            ({"task_content": "3*5?", "options": ["12", "15", "18", "20"], "correct_answer": "15"}, {"A": "12", "B": "15", "C": "18", "D": "20"}, "B"),
            ({"task_content": "Pyt", "options": ["A) Wwa", "B) Krk", "C) Gdn", "D) Poz"], "correct_answer": "C"}, {"A": "Wwa", "B": "Krk", "C": "Gdn", "D": "Poz"}, "C"),
        ]
        for mock_d, exp_opts, exp_ans in cases:
            with patch("app.services.llm_service._simulate_math_task", return_value=mock_d):
                res = generate_math_task(t.id, difficulty_level=1)
                assert res["options"] == exp_opts
                assert db.session.get(Task, res["task_id"]).correct_answer == exp_ans

    raw = [{"A": "A) 2"}, {"B": "B. 4"}, {"C": "C) 6"}, {"D": "D. 8"}]
    assert _normalize_llm_options(raw) == {"A": "2", "B": "4", "C": "6", "D": "8"}


def test_llm_service_errors(app_with_user):
    app, _ = app_with_user
    with app.app_context():
        t = Topic(name="Err")
        db.session.add(t)
        db.session.commit()
        with patch("app.services.llm_service._simulate_math_task", side_effect=RuntimeError("Awaria")):
            with pytest.raises(RuntimeError):
                generate_math_task(t.id, difficulty_level=1)


def test_are_tasks_too_similar_detection():
    q1 = "Podstawą graniastosłupa prostego jest kwadrat o boku długości $a = 4$. Przekątna graniastosłupa jest nachylona do płaszczyzny podstawy pod kątem $\\alpha = 45^\\circ$. Oblicz objętość $V$ tego graniastosłupa."
    q2 = "Podstawą graniastosłupa prostego jest kwadrat o boku długości $a = 4$. Przekątna graniastosłupa tworzy z płaszczyzną podstawy kąt $\\alpha = 45^\\circ$. Oblicz objętość tego graniastosłupa."
    q3 = "Podstawą graniastosłupa prostego jest kwadrat o boku długości $a = 4$. Przekątna ściany bocznej tego graniastosłupa jest nachylona do krawędzi podstawy pod kątem $\\alpha = 45^\\circ$. Oblicz objętość tego graniastosłupa."
    q_diff = "Oblicz objętość ostrosłupa prawidłowego czworokątnego o krawędzi podstawy $6$ i wysokości $H = 8$."

    assert are_tasks_too_similar(q1, q2) is True
    assert are_tasks_too_similar(q1, q3) is True
    assert are_tasks_too_similar(q2, q3) is True
    assert are_tasks_too_similar(q1, q_diff) is False
    assert are_tasks_too_similar("", q1) is False
    assert are_tasks_too_similar(None, q1) is False


def test_generate_math_task_diversity_and_recent_exclusions(app_with_user):
    app, _ = app_with_user
    with app.app_context():
        t = Topic(name="Stereometria - Graniastosłupy")
        db.session.add(t)
        db.session.commit()

        existing_task = Task(
            topic_id=t.id,
            question="Podstawą graniastosłupa prostego jest kwadrat o boku długości $a = 4$. Oblicz objętość.",
            options={"A": "16", "B": "32", "C": "64", "D": "48"},
            correct_answer="C",
            difficulty=1,
        )
        db.session.add(existing_task)
        db.session.commit()

        distinct_content = "W ostrosłupie prawidłowym trójkątnym krawędź podstawy wynosi $6$, a wysokość $9$. Oblicz objętość."
        choice = MagicMock(message=MagicMock(content=json.dumps({
            "task_content": distinct_content,
            "options": {"A": "10", "B": "20", "C": "30", "D": "40"},
            "correct_answer": "B",
            "explanation": "Rozwiązanie krok po kroku",
        })))
        resp = MagicMock(choices=[choice], usage=None, model="gemini-3.8-flash")
        client = MagicMock()
        client.chat.completions.create.return_value = resp

        with patch("app.services.llm_service.get_ai_client", return_value=(client, "gemini-3.8-flash")):
            result = generate_math_task(t.id, difficulty_level=1, exclude_task_id=existing_task.id)
            assert result["question"] == distinct_content

            kwargs = client.chat.completions.create.call_args[1]
            user_msg = next(m["content"] for m in kwargs["messages"] if m["role"] == "user")
            assert "Poprzednie zadania z tego tematu" in user_msg
            assert "NIE powielaj" in user_msg
            assert "temperature" in kwargs and kwargs["temperature"] >= 0.8

