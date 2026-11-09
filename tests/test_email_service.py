from unittest.mock import patch, MagicMock
from flask import render_template
from app.models import User
from app.services.email_service import send_email


def test_password_reset_email_templates_render(app):
    user = User(first_name='Krzysztof', email='krzysztof@example.com')
    url = 'https://example.com/reset-password/sample-token-xyz'

    html = render_template('emails/reset_password.html', user=user, reset_url=url)
    assert 'Krzysztof' in html
    assert 'Axioma' in html
    assert url in html
    assert 'Zresetuj hasło' in html

    text = render_template('emails/reset_password.txt', user=user, reset_url=url)
    assert 'Krzysztof' in text
    assert url in text
    assert '60 minut' in text


def test_send_email_smtp_and_fallbacks(app):
    assert app.config.get('MAIL_SUPPRESS_SEND') is True
    assert send_email('test@example.com', 'Temat', '<p>Treść</p>', 'Treść', sync=True) is True

    app.config.update(MAIL_SUPPRESS_SEND=False, MAIL_SERVER=None, MAIL_USERNAME=None, MAIL_PASSWORD=None)
    assert send_email('test@example.com', 'Temat', '<p>Treść</p>', sync=True) is False

    for use_ssl, smtp_cls, port in [(False, 'smtplib.SMTP', 587), (True, 'smtplib.SMTP_SSL', 465)]:
        with patch(smtp_cls) as mock_cls:
            srv = MagicMock()
            mock_cls.return_value = srv
            app.config.update(
                MAIL_SUPPRESS_SEND=False,
                MAIL_SERVER='smtp.example.com',
                MAIL_PORT=port,
                MAIL_USE_TLS=not use_ssl,
                MAIL_USE_SSL=use_ssl,
                MAIL_USERNAME='user@example.com',
                MAIL_PASSWORD='p',
                MAIL_DEFAULT_SENDER='no-reply@example.com'
            )
            assert send_email('r@example.com', 'Sub', '<h1>H</h1>', 'T', sync=True) is True
            mock_cls.assert_called_once_with('smtp.example.com', port, timeout=10)
            srv.login.assert_called_once_with('user@example.com', 'p')
            srv.send_message.assert_called_once()

    with patch('smtplib.SMTP') as mock_smtp:
        srv = MagicMock()
        srv.login.side_effect = Exception("SMTP auth failed")
        mock_smtp.return_value = srv
        app.config.update(MAIL_SUPPRESS_SEND=False, MAIL_SERVER='smtp.example.com', MAIL_USERNAME='u', MAIL_PASSWORD='p')
        assert send_email('r@example.com', 'B', 'T', sync=True) is False


def test_forgot_password_mailer_integration(client, user_factory):
    user_factory(email='student_mailer@example.com', first_name='Kamil', password='OldPassword1')
    with patch('app.blueprints.auth.routes.send_password_reset_email') as mock_send:
        resp = client.post('/forgot-password', data={'email': 'student_mailer@example.com'}, follow_redirects=True)
        assert resp.status_code == 200
        assert mock_send.called
        assert mock_send.call_args[0][0].email == 'student_mailer@example.com'
        assert '/reset-password/' in mock_send.call_args[0][1]
