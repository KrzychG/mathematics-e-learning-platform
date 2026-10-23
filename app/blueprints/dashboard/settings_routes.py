import base64
import pyotp
import qrcode
from qrcode.image.svg import SvgPathImage
from flask import render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_required, logout_user

from app import limiter
from app.blueprints.dashboard.routes import dashboard_bp
from app.models import Attempt, UserTopicProgress
from app.forms.auth_forms import (
    ChangePasswordForm,
    ProfileForm,
    flash_form_errors,
)
from app.services.dashboard_service import build_student_settings_stats
from app.utils import safe_db_commit
from app.services.totp_service import record_totp_used, verify_totp_code
from app.services.user_service import (
    delete_user_avatar,
    is_blocked_last_active_admin,
    safe_delete_user_account,
    save_user_avatar,
)

def _redirect_settings(anchor: str):
    return redirect(f"{url_for('dashboard.settings')}#{anchor}")
def _generate_2fa_qr_svg(email: str, secret: str) -> str:
    # Generowanie kodu QR dla Authenticatora jako wektorowy SVG w Data URL (base64)
    # Działa całkowicie w pamięci RAM bez zapisywania plików na dysku i bez wycieku danych do zewnętrznych CDN-ów.
    provisioning_uri = pyotp.TOTP(secret).provisioning_uri(name=email, issuer_name='Axioma')
    img = qrcode.make(provisioning_uri, image_factory=SvgPathImage)
    svg_base64 = base64.b64encode(img.to_string()).decode('ascii')
    return f"data:image/svg+xml;base64,{svg_base64}"
@dashboard_bp.route('/settings')
@login_required
def settings():
    qr_code_data = None
    pending_secret = None
    if not current_user.is_otp_enabled:
        pending_secret = session.get('pending_2fa_secret')
        if not pending_secret:
            pending_secret = pyotp.random_base32()
            session['pending_2fa_secret'] = pending_secret
        qr_code_data = _generate_2fa_qr_svg(current_user.email, pending_secret)
    return render_template(
        'dashboard/settings.html',
        user=current_user,
        qr_code_data=qr_code_data,
        pending_secret=pending_secret,
        student_stats=build_student_settings_stats(current_user),
        profile_form=ProfileForm(obj=current_user),
        password_form=ChangePasswordForm(),
    )
@dashboard_bp.route('/upload_avatar', methods=['POST'])
@login_required
@limiter.limit('10 per minute')
def upload_avatar():
    file = request.files.get('avatar')
    _, msg, cat = save_user_avatar(current_user, file)
    flash(msg, cat)
    return _redirect_settings('profile')
@dashboard_bp.route('/delete_avatar', methods=['POST'])
@login_required
@limiter.limit('10 per minute')
def delete_avatar():
    _, msg, cat = delete_user_avatar(current_user)
    flash(msg, cat)
    return _redirect_settings('profile')
@dashboard_bp.route('/enable_2fa', methods=['POST'])
@login_required
@limiter.limit('5 per minute')
def enable_2fa():
    # Aktywacja 2FA
    # Weryfikujemy kod z telefonu przed zapisaniem sekretu w bazie – dzięki temu uczeń
    # nie zablokuje sobie konta, jeśli źle przepisał kod lub ma rozsynchronizowany zegar w telefonie.
    pending_secret = session.get('pending_2fa_secret')
    if not pending_secret:
        flash('Sesja konfiguracji 2FA wygasła. Spróbuj ponownie.', 'danger')
        return _redirect_settings('security')
    verified, token = verify_totp_code(pending_secret, request.form.get('totp_token'))
    if verified:
        current_user.otp_secret = pending_secret
        current_user.is_otp_enabled = True
        session.pop('pending_2fa_secret', None)
        record_totp_used(current_user.id, token)
        safe_db_commit(
            success_msg='Weryfikacja dwuetapowa (2FA) została pomyślnie aktywowana!',
            error_msg='Wystąpił błąd podczas aktywacji 2FA.',
        )
    else:
        flash('Nieprawidłowy 6-cyfrowy kod weryfikacyjny. Sprawdź czas na telefonie i spróbuj ponownie.', 'danger')
    return _redirect_settings('security')
@dashboard_bp.route('/disable_2fa', methods=['POST'])
@login_required
@limiter.limit('5 per minute; 20 per hour')
def disable_2fa():
    # Wyłączenie weryfikacji dwuetapowej
    # Wymagamy potwierdzenia aktualnym hasłem, żeby nikt nie wyłączył 2FA na chwilowo pozostawionym komputerze.
    password = request.form.get('password', '')
    if not current_user.check_password(password):
        flash('Nieprawidłowe hasło. Weryfikacja 2FA nie została wyłączona.', 'danger')
        return _redirect_settings('security')
    current_user.disable_2fa()
    safe_db_commit(
        success_msg='Weryfikacja dwuetapowa (2FA) została pomyślnie wyłączona.',
        error_msg='Wystąpił błąd podczas wyłączania 2FA.',
        success_category='warning',
    )
    return _redirect_settings('security')
@dashboard_bp.route('/update_password', methods=['POST'])
@login_required
@limiter.limit('5 per minute; 20 per hour')
def update_password():
    form = ChangePasswordForm()
    if not form.validate_on_submit():
        flash_form_errors(form)
        return _redirect_settings('security')
    if not current_user.check_password(form.current_password.data):
        flash('Aktualne hasło jest nieprawidłowe.', 'danger')
        return _redirect_settings('security')
    current_user.set_password(form.new_password.data)
    safe_db_commit(
        success_msg='Twoje hasło zostało pomyślnie zaktualizowane!',
        error_msg='Wystąpił błąd podczas aktualizacji hasła.',
    )
    return _redirect_settings('security')
@dashboard_bp.route('/update_profile', methods=['POST'])
@login_required
@limiter.limit('10 per minute')
def update_profile():
    form = ProfileForm()
    if not form.validate_on_submit():
        flash_form_errors(form)
        return _redirect_settings('profile')
    current_user.first_name = form.first_name.data
    safe_db_commit(
        success_msg='Twoje dane profilowe zostały pomyślnie zaktualizowane!',
        error_msg='Wystąpił błąd podczas aktualizacji profilu.',
    )
    return _redirect_settings('profile')
@dashboard_bp.route('/reset_progress', methods=['POST'])
@login_required
@limiter.limit('5 per minute')
def reset_progress():
    UserTopicProgress.query.filter_by(user_id=current_user.id).delete()
    Attempt.query.filter_by(user_id=current_user.id).delete()
    safe_db_commit(
        success_msg='Zresetowano wszystkie postępy i pamięć algorytmu AI.',
        error_msg='Wystąpił błąd podczas resetowania postępów.',
        success_category='warning',
    )
    return _redirect_settings('danger-zone')
@dashboard_bp.route('/delete_account', methods=['POST'])
@login_required
@limiter.limit('5 per minute')
def delete_account():
    password = request.form.get('password', '')
    if not current_user.check_password(password):
        flash('Nieprawidłowe hasło. Konto nie zostało usunięte.', 'danger')
        return _redirect_settings('danger-zone')
    if is_blocked_last_active_admin(current_user, 'Nie można usunąć konta jedynego administratora w systemie.'):
        return _redirect_settings('danger-zone')
    if safe_delete_user_account(
        current_user,
        error_msg='Wystąpił błąd podczas usuwania konta.',
    ):
        session.clear()
        logout_user()
        flash('Twoje konto zostało trwale usunięte.', 'info')
        return redirect(url_for('auth.login'))
    return _redirect_settings('danger-zone')
