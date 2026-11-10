from datetime import datetime
from unittest.mock import patch
import pytest
from werkzeug.security import check_password_hash
from app import db
from app.models import User


@pytest.fixture
def admin_client(client, user_factory, login_as):
    admin = user_factory(email='superadmin@example.com', first_name='Aleksander', password='password123', is_active=True, is_otp_enabled=True, is_admin=True)
    user_factory(email='anna.kowalska@school.pl', first_name='Anna', password='password123', is_active=True, is_otp_enabled=True)
    user_factory(email='bartek.nowak@school.pl', first_name='Bartosz', password='password123', is_active=True, is_otp_enabled=False)
    user_factory(email='cezary.zablokowany@school.pl', first_name='Cezary', password='password123', is_active=False, is_otp_enabled=False)
    return login_as(client, admin)


def test_admin_dashboard_filters(admin_client):
    for query, expected, unexpected in [
        ('?q=kowalska', ['anna.kowalska@school.pl'], ['bartek.nowak@school.pl']),
        ('?role=admin', ['superadmin@example.com'], ['anna.kowalska@school.pl']),
        ('?status=blocked', ['cezary.zablokowany@school.pl'], ['anna.kowalska@school.pl']),
    ]:
        resp = admin_client.get(f'/admin{query}')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        for item in expected: assert item in html
        for item in unexpected: assert item not in html


def test_admin_reset_user_2fa(admin_client):
    with admin_client.application.app_context():
        u_anna = User.query.filter_by(email='anna.kowalska@school.pl').first()
        u_bartek = User.query.filter_by(email='bartek.nowak@school.pl').first()
        anna_id, bartek_id = u_anna.id, u_bartek.id

    html1 = admin_client.post(f'/admin/user/{anna_id}/reset_2fa', follow_redirects=True).data.decode('utf-8')
    assert 'została pomyślnie zresetowana' in html1
    with admin_client.application.app_context():
        assert not db.session.get(User, anna_id).is_otp_enabled

    html2 = admin_client.post(f'/admin/user/{bartek_id}/reset_2fa', follow_redirects=True).data.decode('utf-8')
    assert 'nie ma aktywnej weryfikacji dwuetapowej' in html2


def test_admin_send_password_reset_flows(admin_client):
    with admin_client.application.app_context():
        u_anna = User.query.filter_by(email='anna.kowalska@school.pl').first().id
        u_cezary = User.query.filter_by(email='cezary.zablokowany@school.pl').first().id

    assert 'jest zablokowane. Odblokuj je' in admin_client.post(f'/admin/user/{u_cezary}/send_password_reset', follow_redirects=True).data.decode('utf-8')
    resp = admin_client.post(f'/admin/user/{u_anna}/send_password_reset', follow_redirects=True)
    assert 'została pomyślnie wysłana' in resp.data.decode('utf-8')

    with patch('app.blueprints.admin.user_routes.dispatch_password_reset', return_value=('http://localhost/reset', False)):
        h_smtp = admin_client.post(f'/admin/user/{u_anna}/send_password_reset', follow_redirects=True).data.decode('utf-8')
        assert 'SMTP' in h_smtp and 'Brevo' not in h_smtp


def test_admin_create_and_delete_user(admin_client):
    r1 = admin_client.post('/admin/user/create', data={'first_name': 'Katarzyna', 'email': 'katarzyna.nowa@school.pl', 'role': 'student', 'password': 'Password123!', 'is_active': 'on'}, follow_redirects=True)
    assert 'Pomyślnie utworzono użytkownika katarzyna.nowa@school.pl' in r1.data.decode('utf-8')

    r2 = admin_client.post('/admin/user/create', data={'first_name': 'Tomasz', 'email': 'tomasz.uczen@school.pl', 'role': 'student', 'password': '', 'send_welcome_email': 'on', 'is_active': 'on'}, follow_redirects=True)
    assert 'Pomyślnie utworzono użytkownika tomasz.uczen@school.pl' in r2.data.decode('utf-8') and 'Wygenerowane hasło startowe:' in r2.data.decode('utf-8')

    r3 = admin_client.post('/admin/user/create', data={'first_name': 'Kamil', 'email': 'anna.kowalska@school.pl', 'role': 'admin', 'password': 'Password123!', 'is_active': 'on', 'send_welcome_email': 'on'}, follow_redirects=True)
    assert 'już istnieje w systemie' in r3.data.decode('utf-8') and 'value="Kamil"' in r3.data.decode('utf-8')

    assert 'Pominięto wysyłkę linku resetu hasła' in admin_client.post('/admin/user/create', data={'first_name': 'Nieaktywny', 'email': 'nieaktywny.nowy@school.pl', 'role': 'student', 'password': 'Password123!', 'send_welcome_email': 'on'}, follow_redirects=True).data.decode('utf-8')

    with admin_client.application.app_context():
        u_cezary_id = User.query.filter_by(email='cezary.zablokowany@school.pl').first().id
        admin_id = User.query.filter_by(email='superadmin@example.com').first().id
    assert 'Nie możesz usunąć własnego konta' in admin_client.post(f'/admin/user/{admin_id}/delete', follow_redirects=True).data.decode('utf-8')
    assert 'zostało trwale usunięte' in admin_client.post(f'/admin/user/{u_cezary_id}/delete', follow_redirects=True).data.decode('utf-8')
    with admin_client.application.app_context():
        assert db.session.get(User, u_cezary_id) is None


def test_admin_edit_user_profile_and_sorting(admin_client, tmp_path):
    admin_client.application.config['AVATAR_UPLOAD_DIR'] = str(tmp_path)
    av_f = tmp_path / 'av.png'
    av_f.write_bytes(b'png')

    with admin_client.application.app_context():
        u = User.query.filter_by(email='bartek.nowak@school.pl').first()
        u.avatar_filename = 'av.png'
        u_anna = User.query.filter_by(email='anna.kowalska@school.pl').first()
        u_cezary = User.query.filter_by(email='cezary.zablokowany@school.pl').first()
        u_admin = User.query.filter_by(email='superadmin@example.com').first()
        u_admin.created_at = datetime(2026, 1, 5, 10, 0)
        u_anna.created_at = datetime(2026, 1, 10, 23, 30)
        u.created_at = datetime(2026, 1, 15, 12, 0)
        u_cezary.created_at = datetime(2026, 2, 1, 9, 0)
        db.session.commit()
        tid = u.id

    assert 'już istnieje w systemie' in admin_client.post(f'/admin/user/{tid}/edit', data={'first_name': 'Bart', 'email': 'anna.kowalska@school.pl', 'new_password': ''}, follow_redirects=True).data.decode('utf-8')
    r_ok = admin_client.post(f'/admin/user/{tid}/edit', data={'first_name': 'Bartłomiej', 'email': 'bart.nowak@school.pl', 'new_password': 'NewManualPass99', 'remove_avatar': 'on'}, follow_redirects=True)
    assert 'Zaktualizowano dane' in r_ok.data.decode('utf-8') and 'Usunięto awatar' in r_ok.data.decode('utf-8')
    with admin_client.application.app_context():
        assert check_password_hash(db.session.get(User, tid).password_hash, 'NewManualPass99')

    h_name = admin_client.get('/admin?sort=name_asc').data.decode('utf-8')
    assert h_name.index('superadmin@example.com') < h_name.index('anna.kowalska@school.pl') < h_name.index('bart.nowak@school.pl')
    h_dates = admin_client.get('/admin?date_from=2026-01-11&date_to=2026-01-20').data.decode('utf-8')
    assert 'bart.nowak@school.pl' in h_dates and 'superadmin@example.com' not in h_dates
    assert admin_client.get('/admin?date_from=invalid&sort=unknown').status_code == 200
