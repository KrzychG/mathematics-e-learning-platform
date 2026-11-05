import secrets
from functools import partial
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user

from app import db
from app.blueprints.admin.routes import _redirect_to_admin_list, admin_bp, admin_required
from app.blueprints.auth.routes import dispatch_password_reset
from app.forms.auth_forms import AdminCreateUserForm, AdminEditUserForm, flash_form_errors
from app.models import User
from app.services.admin_service import (
    USER_SORT_OPTIONS,
    build_user_detail_context,
    get_admin_system_counts,
    get_filtered_users_pagination,
)
from app.utils import has_duplicate, safe_db_commit
from app.services.user_service import (
    delete_user_avatar,
    detach_user_avatar,
    is_blocked_last_active_admin,
    is_last_active_admin,
    remove_user_avatar_file,
    safe_delete_user_account,
)


def _get_protected_target_user(
    user_id: int,
    *,
    self_action_msg: str,
    last_admin_msg: str,
    condition_attr: str | None = None,
) -> User | None:
    # Nie pozwól na akcję na samym sobie ani na ostatnim adminie
    if user_id == current_user.id:
        flash(self_action_msg, 'danger')
        return None
    user = db.get_or_404(User, user_id)
    condition = getattr(user, condition_attr) if condition_attr else True
    if is_blocked_last_active_admin(
        user,
        last_admin_msg,
        condition=condition,
        checker=is_last_active_admin,
    ):
        return None
    return user


def _fail_user_form(state_saver, message: str | None = None):
    if message:
        flash(message, 'danger')
    state_saver()
    return _redirect_to_admin_list()


def _store_user_form_state(session_key: str, **extra) -> None:
    session[session_key] = {
        'first_name': request.form.get('first_name', '').strip(),
        'email': request.form.get('email', '').strip(),
        **extra,
    }


def _store_create_user_form_state() -> None:
    _store_user_form_state(
        'create_user_form_data',
        role=(request.form.get('role') or 'student').strip().lower(),
        is_active=bool(request.form.get('is_active')),
        send_welcome_email=bool(request.form.get('send_welcome_email')),
    )


def _store_edit_user_form_state(user: User) -> None:
    _store_user_form_state(
        'edit_user_form_data',
        user_id=user.id,
        remove_avatar=bool(request.form.get('remove_avatar')),
        has_avatar=bool(user.avatar_filename),
    )


def _validate_user_admin_form(form, state_saver, *, exclude_user_id: int | None = None):
    if not form.validate_on_submit():
        flash_form_errors(form)
        return _fail_user_form(state_saver)
    email = form.email.data
    if has_duplicate(User, User.email == email, exclude_id=exclude_user_id):
        return _fail_user_form(
            state_saver,
            f'Użytkownik o adresie {email} już istnieje w systemie.',
        )
    return None


@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()
    role_filter = request.args.get('role', 'all').strip()
    status_filter = request.args.get('status', 'all').strip()
    otp_filter = request.args.get('otp', 'all').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    sort_by = request.args.get('sort', 'id_desc').strip()
    if sort_by not in USER_SORT_OPTIONS:
        sort_by = 'id_desc'
    counts = get_admin_system_counts()
    users_pagination = get_filtered_users_pagination(
        search_query=search_query,
        role_filter=role_filter,
        status_filter=status_filter,
        otp_filter=otp_filter,
        page=page,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
    )
    create_form_data = session.pop('create_user_form_data', None)
    edit_form_data = session.pop('edit_user_form_data', None)
    create_data = dict(create_form_data) if create_form_data else None
    if create_data is not None:
        create_data['send_welcome_email'] = bool(
            create_data.get('send_welcome_email') and create_data.get('is_active')
        )
    create_form = AdminCreateUserForm(formdata=None, data=create_data)
    edit_form = AdminEditUserForm(formdata=None, data=edit_form_data)
    return render_template(
        'admin/admin_dashboard.html',
        **counts,
        active_tab='users',
        users=users_pagination.items,
        users_pagination=users_pagination,
        search_query=search_query,
        role_filter=role_filter,
        status_filter=status_filter,
        otp_filter=otp_filter,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        sort_options=USER_SORT_OPTIONS,
        create_form=create_form,
        edit_form=edit_form,
        create_form_data=create_form_data,
        edit_form_data=edit_form_data,
    )
@admin_bp.route('/admin/user/<int:user_id>/toggle_admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    user = _get_protected_target_user(
        user_id,
        self_action_msg='Nie możesz zmienić własnych uprawnień.',
        last_admin_msg='Nie można odebrać uprawnień ostatniemu aktywnemu administratorowi w systemie.',
        condition_attr='is_admin',
    )
    if not user:
        return _redirect_to_admin_list()
    user.is_admin = not user.is_admin
    action = 'Nadano' if user.is_admin else 'Odebrano'
    safe_db_commit(
        success_msg=f'{action} uprawnienia administratora użytkownikowi {user.email}.',
        error_msg='Wystąpił błąd podczas zmiany uprawnień administratora.',
    )
    return _redirect_to_admin_list()
@admin_bp.route('/admin/user/<int:user_id>/toggle_active', methods=['POST'])
@admin_required
def toggle_active(user_id):
    user = _get_protected_target_user(
        user_id,
        self_action_msg='Nie możesz zablokować własnego konta.',
        last_admin_msg='Nie można zablokować ostatniego aktywnego administratora w systemie.',
        condition_attr='is_active',
    )
    if not user:
        return _redirect_to_admin_list()
    user.is_active = not user.is_active
    status = 'odblokowane' if user.is_active else 'zablokowane'
    safe_db_commit(
        success_msg=f'Konto {user.email} zostało {status}.',
        error_msg='Wystąpił błąd podczas zmiany statusu konta użytkownika.',
    )
    return _redirect_to_admin_list()
@admin_bp.route('/admin/user/<int:user_id>/reset_2fa', methods=['POST'])
@admin_required
def reset_user_2fa(user_id):
    # Awaryjne wyłączenie 2FA przez administratora
    # Przydatne, gdy uczeń zgubi telefon lub usunie aplikację Authenticator.
    # Usuwa sekret TOTP z bazy i pozwala zalogować się samym hasłem.
    user = db.get_or_404(User, user_id)
    if not user.is_otp_enabled:
        flash(f'Użytkownik {user.email} nie ma aktywnej weryfikacji dwuetapowej (2FA).', 'info')
        return _redirect_to_admin_list()
    user.disable_2fa()
    safe_db_commit(
        success_msg=f'Weryfikacja dwuetapowa (2FA) dla użytkownika {user.email} została pomyślnie zresetowana. Użytkownik może zalogować się hasłem.',
        error_msg='Wystąpił błąd podczas resetowania weryfikacji dwuetapowej.',
    )
    return _redirect_to_admin_list()
@admin_bp.route('/admin/user/<int:user_id>/send_password_reset', methods=['POST'])
@admin_required
def send_user_password_reset(user_id):
    # Wysłanie bezpiecznego linku do ustawienia nowego hasła bezpośrednio z panelu admina:
    # Generuje podpisany kryptograficznie token czasowy i wysyła maila.
    user = db.get_or_404(User, user_id)
    if not user.is_active:
        flash(f'Konto użytkownika {user.email} jest zablokowane. Odblokuj je przed wysłaniem linku resetującego.', 'warning')
        return _redirect_to_admin_list()
    _, sent = dispatch_password_reset(user)
    if sent:
        flash(f'Wiadomość z linkiem do resetowania hasła została pomyślnie wysłana na adres {user.email}.', 'success')
    else:
        flash(f'Wystąpił błąd podczas wysyłania e-maila do {user.email}. Sprawdź konfigurację serwera pocztowego SMTP lub ustaw hasło ręcznie w edycji użytkownika.', 'danger')
    return _redirect_to_admin_list()
@admin_bp.route('/admin/user/<int:user_id>')
@admin_required
def user_details(user_id):
    user = db.get_or_404(User, user_id)
    active_detail_tab = request.args.get('tab', 'tasks')
    if active_detail_tab not in {'tasks', 'exams', 'syllabus', 'badges'}:
        active_detail_tab = 'tasks'
    context = build_user_detail_context(
        user=user,
        tasks_page=request.args.get('tasks_page', 1, type=int),
        exams_page=request.args.get('exams_page', 1, type=int),
        topics_page=request.args.get('topics_page', 1, type=int),
        badges_page=request.args.get('badges_page', 1, type=int),
    )
    edit_form_data = session.pop('edit_user_form_data', None)
    if edit_form_data and edit_form_data.get('user_id') != user_id:
        edit_form_data = None
    edit_form = AdminEditUserForm(formdata=None, data=edit_form_data)
    return render_template(
        'admin/user_detail.html',
        **context,
        active_detail_tab=active_detail_tab,
        edit_form=edit_form,
        edit_form_data=edit_form_data,
    )
@admin_bp.route('/admin/user/create', methods=['POST'])
@admin_required
def create_user():
    form = AdminCreateUserForm()
    err_resp = _validate_user_admin_form(form, _store_create_user_form_state)
    if err_resp:
        return err_resp
    first_name = form.first_name.data
    email = form.email.data
    role_name = (form.role.data or 'student').strip().lower()
    password = (form.password.data or '').strip()
    is_active = bool(form.is_active.data)
    send_welcome_email = bool(form.send_welcome_email.data)
    generated_pwd = False
    if not password:
        password = secrets.token_urlsafe(9) + '1A'
        generated_pwd = True
    new_user = User(
        email=email,
        first_name=first_name,
        is_active=is_active,
        is_admin=(role_name == 'admin'),
    )
    new_user.set_password(password)
    db.session.add(new_user)
    if not safe_db_commit(error_msg='Wystąpił błąd podczas zapisywania użytkownika w bazie danych.'):
        return _fail_user_form(_store_create_user_form_state)
    email_note = ''
    if send_welcome_email:
        if not is_active:
            email_note = ' (Pominięto wysyłkę linku resetu hasła — konto utworzono jako zablokowane).'
        else:
            _, sent = dispatch_password_reset(new_user)
            email_note = ' Na adres e-mail wysłano link do ustalenia hasła.' if sent else ' (Nie udało się wysłać powiadomienia e-mail).'
    role_label = 'Administrator' if role_name == 'admin' else 'Uczeń'
    pwd_info = f' Wygenerowane hasło startowe: {password}.' if generated_pwd else ''
    flash(f'Pomyślnie utworzono użytkownika {email} ({role_label}).{pwd_info}{email_note}', 'success')
    return _redirect_to_admin_list()
@admin_bp.route('/admin/user/<int:user_id>/edit', methods=['POST'])
@admin_required
def edit_user(user_id):
    user = db.get_or_404(User, user_id)
    state_saver = partial(_store_edit_user_form_state, user)
    form = AdminEditUserForm()
    err_resp = _validate_user_admin_form(form, state_saver, exclude_user_id=user.id)
    if err_resp:
        return err_resp
    new_password = (form.new_password.data or '').strip()
    remove_avatar = bool(form.remove_avatar.data)
    user.first_name = form.first_name.data
    user.email = form.email.data
    if new_password:
        user.set_password(new_password)
    old_avatar = detach_user_avatar(user) if remove_avatar else None
    if not safe_db_commit(error_msg='Wystąpił błąd podczas zapisywania zmian użytkownika.'):
        return _fail_user_form(state_saver)
    if old_avatar:
        remove_user_avatar_file(old_avatar)
    details = []
    if new_password:
        details.append('Ustawiono nowe hasło')
    if old_avatar:
        details.append('Usunięto awatar')
    suffix = f" ({', '.join(details)})." if details else ''
    flash(f'Zaktualizowano dane użytkownika {user.email}.{suffix}', 'success')
    return _redirect_to_admin_list()
@admin_bp.route('/admin/user/<int:user_id>/delete_avatar', methods=['POST'])
@admin_required
def delete_user_avatar_admin(user_id):
    user = db.get_or_404(User, user_id)
    if not user.avatar_filename:
        flash(f'Użytkownik {user.email} nie posiada wgranego awatara.', 'info')
        return _redirect_to_admin_list()
    success, msg, cat = delete_user_avatar(user)
    if success:
        flash(f'Awatar użytkownika {user.email} został usunięty.', 'info')
    else:
        flash(msg, cat)
    return _redirect_to_admin_list()
@admin_bp.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = _get_protected_target_user(
        user_id,
        self_action_msg='Nie możesz usunąć własnego konta z poziomu panelu administratora.',
        last_admin_msg='Nie można usunąć ostatniego aktywnego administratora w systemie.',
    )
    if not user:
        return _redirect_to_admin_list()
    email = user.email
    safe_delete_user_account(
        user,
        success_msg=f'Konto użytkownika {email} zostało trwale usunięte wraz z powiązaną historią.',
        error_msg=f'Wystąpił błąd podczas usuwania konta {email}.',
    )
    if request.referrer and f'/admin/user/{user_id}' in request.referrer:
        return redirect(url_for('admin.admin_dashboard'))
    return _redirect_to_admin_list()
