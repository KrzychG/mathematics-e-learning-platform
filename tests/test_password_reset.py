from werkzeug.security import check_password_hash
from app.models import User
from app.blueprints.auth.routes import generate_reset_token, verify_reset_token


def test_forgot_password_views_and_requests(client, user_factory):
    assert '/forgot-password' in client.get('/login').data.decode('utf-8')
    assert 'Odzyskiwanie hasła' in client.get('/forgot-password').data.decode('utf-8')

    user_factory(email='student_reset@example.com', first_name='Marek', password='OldPassword123')
    resp_exist = client.post('/forgot-password', data={'email': 'student_reset@example.com'}, follow_redirects=True).data.decode('utf-8')
    assert 'Jeśli konto z tym adresem e-mail istnieje' in resp_exist and '/reset-password/' in resp_exist

    resp_ghost = client.post('/forgot-password', data={'email': 'ghost@example.com'}, follow_redirects=True).data.decode('utf-8')
    assert 'Jeśli konto z tym adresem e-mail istnieje' in resp_ghost and '/reset-password/' not in resp_ghost


def test_reset_password_token_validation_and_successful_update(client, user_factory, post_login):
    user_factory(email='complete_flow@example.com', first_name='Kasia', password='OldPassword123')
    token = generate_reset_token('complete_flow@example.com')

    html_v = client.get(f'/reset-password/{token}').data.decode('utf-8')
    assert 'Ustaw nowe hasło' in html_v and 'name="new_password"' in html_v
    assert 'Link do resetowania hasła jest nieprawidłowy lub wygasł' in client.post('/reset-password/invalid', follow_redirects=True).data.decode('utf-8')
    assert verify_reset_token(token, max_age=-1) is None

    resp_diff = client.post(f'/reset-password/{token}', data={'new_password': 'Valid123Password', 'confirm_password': 'Diff123Password'}, follow_redirects=True)
    assert 'Hasła nie są identyczne' in resp_diff.data.decode('utf-8')

    resp = client.post(f'/reset-password/{token}', data={'new_password': 'BrandNewPassword456', 'confirm_password': 'BrandNewPassword456'}, follow_redirects=True)
    assert resp.status_code == 200 and 'Hasło zostało pomyślnie zaktualizowane' in resp.data.decode('utf-8')

    u = User.query.filter_by(email='complete_flow@example.com').first()
    assert check_password_hash(u.password_hash, 'BrandNewPassword456') and not check_password_hash(u.password_hash, 'OldPassword123')

    assert verify_reset_token(token) is None
    replay_resp = client.post(f'/reset-password/{token}', data={'new_password': 'AnotherPassword789', 'confirm_password': 'AnotherPassword789'}, follow_redirects=True)
    assert 'Link do resetowania hasła jest nieprawidłowy lub wygasł' in replay_resp.data.decode('utf-8')

    login_resp = post_login(client, 'complete_flow@example.com', 'BrandNewPassword456', follow_redirects=True)
    assert login_resp.status_code == 200 and ('/dashboard' in login_resp.request.path or 'Panel' in login_resp.data.decode('utf-8'))
