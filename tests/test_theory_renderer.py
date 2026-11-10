import pytest
from app import db
from app.models import Topic
from app.services.theory_renderer_service import render_theory_markdown


@pytest.mark.parametrize('md_input,expected_fragments,forbidden_fragments', [
    (
        '# Tytuł\n\n**pogrubiony** i *kursywa*\n\n> Ważna definicja klasyfikacji\n\n$$\\mathbb{N}$$\n\n| $x$ | $f(x)$ |\n| --- | --- |\n| $0$ | $1$ |',
        ['<h1>Tytuł</h1>', '<strong>pogrubiony</strong>', '<blockquote>', 'Ważna definicja klasyfikacji', 'table-responsive', '$x$'],
        []
    ),
    (
        '<script>alert("x")</script><img src="x" onerror="steal()"><a href="javascript:alert(1)">link</a>',
        [],
        ['<script>', 'alert("x")', 'onerror', 'javascript:']
    ),
])
def test_render_theory_markdown_features(md_input, expected_fragments, forbidden_fragments):
    html = render_theory_markdown(md_input)
    for exp in expected_fragments:
        assert exp in html
    for fbd in forbidden_fragments:
        assert fbd not in html


def test_markdown_storage_in_topic_model(app):
    raw_md = '# Teoria Podstawowa\n\n> **Definicja:** Równanie kwadratowe\n\n$$ax^2 + bx + c = 0$$'
    topic = Topic(name='Test Markdown DB', theory=raw_md)
    db.session.add(topic)
    db.session.commit()

    saved = db.session.get(Topic, topic.id)
    assert saved.theory == raw_md

    rendered = render_theory_markdown(saved.theory)
    assert '<h1>Teoria Podstawowa</h1>' in rendered
    assert '<blockquote>' in rendered
    assert '$$ax^2 + bx + c = 0$$' in rendered
