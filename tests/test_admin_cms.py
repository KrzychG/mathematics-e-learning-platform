import pytest
from app import db
from app.models import Category, Topic


@pytest.fixture
def cms_test_setup(app, admin_user, student_user):
    cat1 = Category(name='Kategoria Testowa 1')
    db.session.add(cat1)
    db.session.flush()
    topic1 = Topic(category_id=cat1.id, name='Temat Testowy 1', description='Opis testowy', theory='<h4>Wstęp</h4><p>$$x = 1$$</p>')
    db.session.add(topic1)
    db.session.commit()
    return app, admin_user.id, student_user.id, cat1.id, topic1.id


def test_admin_content_access_control(cms_test_setup, client, login_as):
    _, admin_id, student_id, _, _ = cms_test_setup

    assert client.get('/admin/content').status_code == 302
    login_as(client, student_id)
    assert client.get('/admin/content').status_code == 403
    login_as(client, admin_id)
    resp = client.get('/admin/content')
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    for item in ('Kategorie i Tematy', 'Kategoria Testowa 1', 'Temat Testowy 1'):
        assert item in html


def test_category_and_topic_crud(cms_test_setup, client, login_as):
    app, admin_id, _, cat_id, _ = cms_test_setup
    login_as(client, admin_id)

    assert client.post('/admin/category/new', data={'name': 'Nowa Kat'}, follow_redirects=True).status_code == 200
    with app.app_context():
        c_id = Category.query.filter_by(name='Nowa Kat').first().id
    assert client.post(f'/admin/category/{c_id}/edit', data={'name': 'Kat Zmieniona'}, follow_redirects=True).status_code == 200
    with app.app_context():
        assert db.session.get(Category, c_id).name == 'Kat Zmieniona'
    assert client.post(f'/admin/category/{c_id}/delete', follow_redirects=True).status_code == 200
    with app.app_context():
        assert db.session.get(Category, c_id) is None

    client.post('/admin/topic/new', data={'name': 'Nowy Temat', 'category_id': str(cat_id), 'description': 'O', 'theory': '<p>$$sin^2 x$$</p>'}, follow_redirects=True)
    with app.app_context():
        t_id = Topic.query.filter_by(name='Nowy Temat').first().id
    assert 'Nowy Temat' in client.get(f'/admin/topic/{t_id}/edit').data.decode('utf-8')

    client.post(f'/admin/topic/{t_id}/edit', data={'name': 'Temat Zmieniony', 'category_id': str(cat_id), 'description': 'O2', 'theory': '<h4>Teoria</h4>'}, follow_redirects=True)
    with app.app_context():
        assert db.session.get(Topic, t_id).name == 'Temat Zmieniony'
    assert client.post(f'/admin/topic/{t_id}/delete', follow_redirects=True).status_code == 200
    with app.app_context():
        assert db.session.get(Topic, t_id) is None


def test_topic_theory_sanitizes_xss(cms_test_setup, login_as):
    app, admin_id, _, _, topic_id = cms_test_setup
    client = app.test_client()
    login_as(client, admin_id)

    dirty = '<script>alert("hack")</script><p onclick="steal()">Wzór: $$x^2$$</p>'
    client.post(f'/admin/topic/{topic_id}/edit', data={'name': 'Temat Testowy 1', 'theory': dirty}, follow_redirects=True)
    with app.app_context():
        saved = db.session.get(Topic, topic_id).theory
        assert '<script>' not in saved and 'onclick' not in saved and 'Wzór: $$x^2$$' in saved


def test_new_topic_metadata_and_uncategorized(cms_test_setup, client, login_as):
    app, admin_id, _, _, _ = cms_test_setup
    login_as(client, admin_id)
    client.post('/admin/topic/new', data={'name': 'Temat Bez Kategorii', 'category_id': '', 'description': 'D', 'theory': '<p>T</p>'}, follow_redirects=True)
    with app.app_context():
        t = Topic.query.filter_by(name='Temat Bez Kategorii').first()
        assert t is not None and t.category_id is None and t.description == 'D'
