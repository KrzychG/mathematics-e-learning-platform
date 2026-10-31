"""
Serwis Wysyłki Poczty elektronicznej smtp
Obsługuje wysyłkę wiadomości transakcyjnych
Domyślnie działa asynchronicznie w osobnym wątku tła aby nie blokować UI
Wspiera szyfrowanie STARTTLS (port 587) oraz SSL/TLS
Zawiera tryb mock/bezpieczny: przy braku konfiguracji SMTP loguje linki w konsoli zamiast rzucać błędem
"""

import logging
import smtplib
import threading
from email.message import EmailMessage
from flask import current_app, render_template

logger = logging.getLogger(__name__)

def _send_async_email(app, msg, to_email):
    with app.app_context():
        _deliver_message(msg, to_email)


def _deliver_message(msg: EmailMessage, to_email: str) -> bool:
    mail_server = current_app.config.get('MAIL_SERVER')
    mail_port = current_app.config.get('MAIL_PORT', 587)
    mail_username = current_app.config.get('MAIL_USERNAME')
    mail_password = current_app.config.get('MAIL_PASSWORD')
    mail_use_tls = current_app.config.get('MAIL_USE_TLS', True)
    mail_use_ssl = current_app.config.get('MAIL_USE_SSL', False)
    timeout = current_app.config.get('MAIL_TIMEOUT', 10)
    try:
        if mail_use_ssl:
            server = smtplib.SMTP_SSL(mail_server, mail_port, timeout=timeout)
        else:
            server = smtplib.SMTP(mail_server, mail_port, timeout=timeout)
            if mail_use_tls:
                server.starttls()
        if mail_username and mail_password:
            server.login(mail_username, mail_password)
        server.send_message(msg)
        server.quit()
        logger.info(f"[EMAIL] Wiadomość e-mail została pomyślnie wysłana do {to_email}")
        return True
    except Exception as exc:
        logger.error(f"[EMAIL ERROR] Błąd podczas wysyłania wiadomości SMTP do {to_email}: {exc}", exc_info=True)
        return False
def send_email(to_email: str, subject: str, html_body: str, text_body: str = None, sync: bool = False) -> bool:
    # Wysyłka przez SMTP (w testach mock/suppress, przy braku konfiguracji log w konsoli)
    if current_app.config.get('MAIL_SUPPRESS_SEND'):
        logger.debug(f"[EMAIL TEST] Wysyłka pominięta dla {to_email} (MAIL_SUPPRESS_SEND=True)")
        return True
    mail_server = current_app.config.get('MAIL_SERVER')
    mail_username = current_app.config.get('MAIL_USERNAME')
    mail_password = current_app.config.get('MAIL_PASSWORD')
    sender_email = current_app.config.get('MAIL_DEFAULT_SENDER') or 'no-reply@axioma.pl'
    sender_name = current_app.config.get('MAIL_SENDER_NAME') or 'Axioma'
    if not mail_server or not mail_username or not mail_password:
        logger.warning(
            f"[EMAIL MOCK / CONSOLE] Brak pełnej konfiguracji SMTP w pliku .env. Wiadomość do '{to_email}' nie została wysłana do sieci.\n"
            f"--- TREŚĆ WIADOMOŚCI ({subject}) ---\n"
            f"{text_body or html_body}\n"
            f"----------------------------------------"
        )
        return False
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"{sender_name} <{sender_email}>" if sender_name else sender_email
    msg['To'] = to_email
    if text_body:
        msg.set_content(text_body)
    if html_body:
        msg.add_alternative(html_body, subtype='html')
    if sync:
        return _deliver_message(msg, to_email)
    else:
        app = current_app._get_current_object()
        thread = threading.Thread(target=_send_async_email, args=(app, msg, to_email), daemon=True)
        thread.start()
        return True


def send_password_reset_email(user, reset_url: str, sync: bool = False) -> bool:
    subject = "Resetowanie hasła w serwisie Axioma"
    try:
        html_body = render_template('emails/reset_password.html', user=user, reset_url=reset_url)
        text_body = render_template('emails/reset_password.txt', user=user, reset_url=reset_url)
        return send_email(user.email, subject, html_body, text_body, sync=sync)
    except Exception as exc:
        logger.error(f"[EMAIL ERROR] Błąd podczas renderowania szablonu e-mail dla {user.email}: {exc}", exc_info=True)
        return False
