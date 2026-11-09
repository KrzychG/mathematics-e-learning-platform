import io
from PIL import Image
import pytest
from werkzeug.security import generate_password_hash
from app import db
from app.models import User


def test_logout_session_and_method(app_with_user, client, login_as):
    _, user_id = app_with_user
    login_as(client, user_id, pending_task_1=999, pending_2fa_secret='SECRETXYZ')
    assert client.get('/logout').status_code == 405
    assert client.post('/logout', follow_redirects=True).status_code == 200
    with client.session_transaction() as sess:
        assert 'pending_task_1' not in sess and '_user_id' not in sess


def test_avatar_upload(app_with_user, client, login_as):
    _, user_id = app_with_user
    login_as(client, user_id)
    buf = io.BytesIO()
    Image.new('RGB', (100, 100), color='blue').save(buf, format='PNG')
    buf.seek(0)
    assert client.post('/upload_avatar', data={'avatar': (buf, 'test.png')}, content_type='multipart/form-data', follow_redirects=True).status_code == 200
    user = db.session.get(User, user_id)
    assert user.avatar_filename and user.avatar_filename.startswith(f"avatar_{user_id}_") and user.avatar_filename.endswith(".png")


def test_login_next_redirect_safety(app_with_user, client, post_login):
    assert post_login(client, 'test_user@example.com', 'user_password123', query='?next=/learning').headers['Location'] == '/learning'
    client.get('/logout')
    assert '/dashboard' in post_login(client, 'test_user@example.com', 'user_password123', query='?next=https://evil.com').headers['Location']


def test_2fa_secret_persistence(app_with_user):
    app, user_id = app_with_user
    with app.app_context():
        user = db.session.get(User, user_id)
        user.otp_secret = "JBSWY3DPEHPK3PXP"
        user.is_otp_enabled = True
        db.session.commit()

        db.session.expire_all()
        reloaded = db.session.get(User, user_id)
        assert reloaded.otp_secret == "JBSWY3DPEHPK3PXP"
        assert reloaded.is_otp_enabled is True

        user.otp_secret = None
        user.is_otp_enabled = False
        db.session.commit()
        db.session.expire_all()
        assert db.session.get(User, user_id).otp_secret is None


@pytest.mark.parametrize('other_admin_active,expected_msg,should_delete', [
    (None, 'Nie można usunąć konta jedynego administratora', False),
    (True, 'Twoje konto zostało trwale usunięte', True),
])
def test_delete_admin_rules(app_with_user, client, login_as, other_admin_active, expected_msg, should_delete):
    app, user_id = app_with_user
    with app.app_context():
        db.session.get(User, user_id).is_admin = True
        if other_admin_active is not None:
            db.session.add(User(email='other_admin@example.com', first_name='Admin2', password_hash=generate_password_hash('pass123'), is_admin=True, is_active=other_admin_active))
        db.session.commit()

    login_as(client, user_id)
    resp = client.post('/delete_account', data={'password': 'user_password123'}, follow_redirects=True)
    assert resp.status_code == 200 and expected_msg in resp.get_data(as_text=True)
    with app.app_context():
        assert (db.session.get(User, user_id) is None) == should_delete


@pytest.mark.parametrize('email,pwd,cpwd,msg,created', [
    ('k1@ex.com', 'Abc12', 'Abc12', 'Hasło musi mieć co najmniej 8 znaków', False),
    ('ks@ex.com', 'SilneHaslo123', 'SilneHaslo123', 'Rejestracja zakończona sukcesem', True),
])
def test_register_password_validation(app_with_user, email, pwd, cpwd, msg, created):
    app, _ = app_with_user
    with app.test_client() as client:
        resp = client.post('/register', data={'first_name': 'Kamil', 'email': email, 'password': pwd, 'confirm_password': cpwd}, follow_redirects=True)
        assert resp.status_code == 200 and msg in resp.data.decode('utf-8')
        if created:
            with app.app_context():
                assert User.query.filter_by(email=email).first() is not None


def test_2fa_max_attempts_lockout(client, user_factory, post_login):
    import pyotp
    raw_pwd = 'SafePassword123!'
    user = user_factory(email='lockout_2fa@example.com', first_name='Adam', password=raw_pwd)
    secret = pyotp.random_base32()
    with client.application.app_context():
        u = db.session.get(User, user.id)
        u.otp_secret = secret
        u.is_otp_enabled = True
        db.session.commit()

    post_login(client, 'lockout_2fa@example.com', raw_pwd)

    for _ in range(4):
        resp = client.post('/login/2fa', data={'totp_token': '000000'}, follow_redirects=True)
        assert resp.status_code == 200
        assert 'Nieprawidłowy 6-cyfrowy kod' in resp.data.decode('utf-8')

    resp_locked = client.post('/login/2fa', data={'totp_token': '000000'}, follow_redirects=True)
    assert resp_locked.status_code == 200
    assert 'Przekroczono limit prób weryfikacji dwuetapowej' in resp_locked.data.decode('utf-8')
    with client.session_transaction() as sess:
        assert '2fa_user_id' not in sess

