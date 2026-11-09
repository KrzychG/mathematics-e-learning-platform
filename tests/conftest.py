import itertools
import pytest
from flask import g
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User


@pytest.fixture
def app_factory(tmp_path):
    created_apps = []

    def _create_app(config='testing', init_db=True):
        test_app = create_app(config)
        test_app.config['AVATAR_UPLOAD_DIR'] = str(tmp_path)
        if init_db:
            with test_app.app_context(): db.create_all()
            @test_app.before_request
            def _clear_stale():
                g.pop('_login_user', None)
                if not (db.session.new or db.session.dirty or db.session.deleted): db.session.rollback()
            @test_app.teardown_request
            def _cleanup(exc=None):
                g.pop('_login_user', None)
                db.session.rollback()
        created_apps.append((test_app, init_db))
        return test_app

    yield _create_app
    for test_app, has_db in reversed(created_apps):
        with test_app.app_context():
            db.session.remove()
            if has_db: db.drop_all()
            db.engine.dispose()


@pytest.fixture
def app(app_factory):
    test_app = app_factory('testing')
    with test_app.app_context(): yield test_app


@pytest.fixture
def client(app):
    with app.test_client() as test_client: yield test_client


@pytest.fixture
def user_factory(app):
    seq = itertools.count(1)
    def _create_user(email=None, first_name='Uczen', password='password123', password_hash=None, is_admin=False, commit=True, **kwargs):
        idx = next(seq)
        user = User(email=email or f'user_{idx}@example.com', first_name=first_name, password_hash=password_hash if password_hash is not None else generate_password_hash(password), is_admin=is_admin, **kwargs)
        db.session.add(user)
        if commit: db.session.commit()
        return user
    return _create_user


@pytest.fixture
def login_as():
    def _login(test_client, user, fresh=True, **extra):
        with test_client.session_transaction() as sess:
            sess['_user_id'] = str(getattr(user, 'id', user))
            sess['_fresh'] = fresh
            sess.update(extra)
        return test_client
    return _login


@pytest.fixture
def post_login():
    def _post(client, email, password, query='', follow_redirects=False):
        return client.post(f'/login{query}', data={'email': email, 'password': password}, follow_redirects=follow_redirects)
    return _post


@pytest.fixture
def student_user(user_factory): return user_factory(email='student@example.com', first_name='Uczen', is_admin=False)


@pytest.fixture
def admin_user(user_factory): return user_factory(email='admin@example.com', first_name='Admin', is_admin=True)


@pytest.fixture
def student_client(client, student_user, login_as): return login_as(client, student_user)


@pytest.fixture
def admin_client(client, admin_user, login_as): return login_as(client, admin_user)


@pytest.fixture
def app_with_user(app, user_factory):
    return app, user_factory(email='test_user@example.com', first_name='Jan', password='user_password123', is_admin=False).id

