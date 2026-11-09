import pytest
from app import db
from app.models import Topic, Task
from app.services.sanitizer_service import (
    sanitize_theory_html,
    format_math,
)


@pytest.mark.parametrize('dirty,forbidden,required', [
    (
        '<p>Treść</p><script type="text/javascript">alert("XSS");</script><div onload="evil()"><a href="javascript:alert(1)">link</a></div>',
        ['<script', 'alert(', 'onload', 'javascript:'],
        ['<p>Treść</p>', 'link']
    ),
    (
        '<a href="https://example.com/math" title="Podręcznik">Podręcznik</a><p>Bezpieczny akapit</p>',
        [],
        ['href="https://example.com/math"', 'title="Podręcznik"', '<p>Bezpieczny akapit</p>']
    ),
])
def test_sanitizer_rules(dirty, forbidden, required):
    cleaned = sanitize_theory_html(dirty)
    for f in forbidden:
        assert f not in cleaned
    for r in required:
        assert r in cleaned


def test_topic_model_sanitization(app):
    topic = Topic(name='Sanitize Model', theory='<script>alert("x")</script><p>Akapit</p>')
    db.session.add(topic)
    db.session.commit()
    assert '<script>' not in topic.theory and '<p>Akapit</p>' in topic.theory
    topic.theory = '<div onclick="hack()">Nowa treść</div>'
    db.session.commit()
    assert 'onclick' not in topic.theory and '<div>Nowa treść</div>' in topic.theory


def test_format_math_and_task_fraction_sanitization(app):
    assert format_math(r'$$\frac{6}{8}$$') == r'$$\frac{6}{8}$$'
    assert format_math(r'\frac{1}{2}') == r'\(\frac{1}{2}\)'
    assert format_math(r'x^2 + 4') == r'\(x^2 + 4\)'

    topic = Topic(name='Matematyka Test')
    db.session.add(topic)
    db.session.commit()
    task = Task(
        topic_id=topic.id,
        question=r'Uprość: $$\frac{6}{8}$$',
        options=r'{"A": "\\frac{2}{3}", "B": "\\frac{1}{2}"}',
        correct_answer='A',
    )
    assert task.options_dict['A'] == r'\frac{2}{3}'
    assert task.options_dict['B'] == r'\frac{1}{2}'
