import io
import os
import time
from datetime import datetime, timezone
from PIL import Image
import pyotp
import pytest
from app import db
from app.models import User
from app.services import totp_service


@pytest.fixture(autouse=True)
def _clear_totp_replay_cache():
    with totp_service._used_tokens_lock:
        totp_service._USED_LOGIN_TOKENS.clear()


def _png_stream():
    buf = io.BytesIO()
    Image.new('RGB', (16, 16), color='blue').save(buf, format='PNG')
    buf.seek(0)
    return buf


def test_avatar_operations_and_account_deletion(app, client, user_factory, login_as):
    user = user_factory(email='del_u@example.com', first_name='T', password='SafePassword123!')
    login_as(client, user.id)

    for bad_d in ({'avatar': (io.BytesIO(b'txt'), 'test.txt')}, {'avatar': (io.BytesIO(b'<?php'), 'm.png')}):
        resp = client.post('/upload_avatar', data=bad_d, content_type='multipart/form-data', follow_redirects=True)
        assert resp.status_code == 200 and db.session.get(User, user.id).avatar_filename is None

    resp_ok = client.post('/upload_avatar', data={'avatar': (_png_stream(), 'avatar.png')}, content_type='multipart/form-data', follow_redirects=True)
    assert 'został pomyślnie zaktualizowany' in resp_ok.data.decode('utf-8')
    av_filename = db.session.get(User, user.id).avatar_filename
    assert av_filename.endswith('.png')
    av_path = os.path.join(app.config.get('AVATAR_UPLOAD_DIR') or os.path.join(app.root_path, 'static', 'uploads', 'avatars'), av_filename)
    assert os.path.exists(av_path)

    assert 'Nieprawidłowe hasło' in client.post('/delete_account', data={'password': 'wrong'}, follow_redirects=True).data.decode('utf-8')
    assert 'Twoje konto zostało trwale usunięte' in client.post('/delete_account', data={'password': 'SafePassword123!'}, follow_redirects=True).data.decode('utf-8')
    assert db.session.get(User, user.id) is None and not os.path.exists(av_path)


def test_2fa_full_lifecycle_and_ttl(client, user_factory, login_as, post_login):
    raw_pwd = 'Password123!'
    user = user_factory(email='totp_user@example.com', first_name='Janusz', password=raw_pwd)
    login_as(client, user)

    client.get('/settings')
    with client.session_transaction() as sess:
        secret = sess.get('pending_2fa_secret')

    assert 'Nieprawidłowy 6-cyfrowy kod' in client.post('/enable_2fa', data={'totp_token': '000000'}, follow_redirects=True).data.decode('utf-8')
    valid_token = pyotp.TOTP(secret).now()
    assert 'została pomyślnie aktywowana' in client.post('/enable_2fa', data={'totp_token': valid_token}, follow_redirects=True).data.decode('utf-8')

    client.post('/logout')
    assert '/login/2fa' in post_login(client, 'totp_user@example.com', raw_pwd).headers['Location']

    assert 'został już wykorzystany' in client.post('/login/2fa', data={'totp_token': valid_token}, follow_redirects=True).data.decode('utf-8')
    assert 'Nieprawidłowy 6-cyfrowy kod' in client.post('/login/2fa', data={'totp_token': '999999'}, follow_redirects=True).data.decode('utf-8')

    with client.session_transaction() as sess:
        sess['2fa_time'] = datetime.now(timezone.utc).timestamp() - 360
    assert 'Sesja logowania dwuetapowego wygasła' in client.post('/login/2fa', data={'totp_token': pyotp.TOTP(secret).at(time.time() + 30)}, follow_redirects=True).data.decode('utf-8')

    post_login(client, 'totp_user@example.com', raw_pwd)
    token_next = pyotp.TOTP(secret).at(time.time() + 30)
    assert 'Dashboard' in client.post('/login/2fa', data={'totp_token': token_next}, follow_redirects=True).data.decode('utf-8')

    assert 'Nieprawidłowe hasło' in client.post('/disable_2fa', data={'password': 'wrong'}, follow_redirects=True).data.decode('utf-8')
    assert 'została pomyślnie wyłączona' in client.post('/disable_2fa', data={'password': raw_pwd}, follow_redirects=True).data.decode('utf-8')
    assert not db.session.get(User, user.id).is_otp_enabled


def test_registration_and_email_normalization(client, post_login):
    resp = client.post('/register', data={'email': 'New.Student@EXAMPLE.COM', 'first_name': 'Kamil', 'password': 'Password123!', 'confirm_password': 'Password123!'}, follow_redirects=True)
    assert 'Rejestracja zakończona sukcesem' in resp.data.decode('utf-8')
    u = User.query.filter_by(email='new.student@example.com').first()
    assert u and u.is_admin is False and u.first_name == 'Kamil'

    for e in ('NEW.STUDENT@EXAMPLE.COM', 'new.student@example.com'):
        assert 'Dashboard' in post_login(client, e, 'Password123!', follow_redirects=True).data.decode('utf-8')
        client.post('/logout')


def test_user_profile_settings_and_update(client, user_factory, login_as):
    user = user_factory(email='card@example.com', first_name='Zofia', password='password123', avatar_filename='avatar.png')
    login_as(client, user.id)

    html = client.get('/settings').data.decode('utf-8')
    for term in ('W Axioma od:', 'ZADANIA', 'SKUTECZNOŚĆ', 'ODZNAKI', 'id="appConfirmModal"', 'data-confirm-title="Usunięcie awatara"'):
        assert term in html

    assert 'Imię musi mieć od 2 do 50 znaków.' in client.post('/update_profile', data={'first_name': 'A'}, follow_redirects=True).data.decode('utf-8')
    client.post('/update_profile', data={'first_name': '  Zofia Maria  '}, follow_redirects=True)
    assert db.session.get(User, user.id).first_name == 'Zofia Maria'
