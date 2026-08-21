from functools import wraps
from flask import (
    Blueprint,
    current_app,
    flash,
    has_request_context,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from itsdangerous import URLSafeTimedSerializer

TWO_FACTOR_TTL_SECONDS = 300  # 5 minut (TTL sesji logowania dwuetapowego)
RESET_PASSWORD_SALT = 'password-reset-salt'
RESET_PASSWORD_MAX_AGE = 3600  # 1 godzina ważności linku
from flask_login import login_user, logout_user, current_user, login_required

from app import db, limiter
from app.models import User, utc_now
from app.forms.auth_forms import (
    LoginForm,
    RegisterForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    validate_form_or_flash,
)
from app.services.totp_service import is_totp_replayed, record_totp_used, verify_totp_code

from app.services.email_service import send_password_reset_email
from app.utils import safe_db_commit

auth_bp = Blueprint('auth', __name__)

MAX_2FA_ATTEMPTS = 5

def _get_safe_next_url(target: str | None) -> str:
    # Ochrona przed open redirect
    if target and target.startswith('/') and not target.startswith('//') and not target.startswith('/\\'):
        from urllib.parse import urlsplit
        parsed = urlsplit(target)
        if not parsed.netloc and not parsed.scheme:
            return target
    return url_for('dashboard.dashboard')


def anonymous_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute; 20 per day", methods=["POST"])
@anonymous_required
def register():
    form = RegisterForm()
    if validate_form_or_flash(form):
        email = form.email.data
        first_name = form.first_name.data
        password = form.password.data
        if User.query.filter_by(email=email).first():
            flash('Konto z tym adresem email już istnieje.', 'danger')
            return redirect(url_for('auth.register'))
        new_user = User(email=email, first_name=first_name)
        new_user.set_password(password)
        db.session.add(new_user)
        if safe_db_commit(
            success_msg='Rejestracja zakończona sukcesem! Możesz się zalogować.',
            error_msg='Wystąpił błąd podczas zapisywania użytkownika w bazie. Spróbuj ponownie.'
        ):
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute; 25 per hour", methods=["POST"])
@anonymous_required
def login():
    form = LoginForm()
    if validate_form_or_flash(form):
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.is_active:
                flash('Twoje konto zostało zablokowane przez administratora.', 'danger')
                return redirect(url_for('auth.login'))
            next_page = _get_safe_next_url(request.args.get('next'))
            if user.is_otp_enabled and user.otp_secret:
                session['2fa_user_id'] = user.id
                session['2fa_time'] = utc_now().timestamp()
                session['2fa_next'] = next_page
                return redirect(url_for('auth.verify_2fa'))
            login_user(user)
            return redirect(next_page)
        else:
            flash('Nieprawidłowy e-mail lub hasło.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    logout_user()
    flash('Zostałeś poprawnie wylogowany.', 'info')
    return redirect(url_for('auth.login'))


def _clear_2fa_session():
    session.pop('2fa_user_id', None)
    session.pop('2fa_time', None)
    session.pop('2fa_next', None)
    session.pop('2fa_attempts', None)


@auth_bp.route('/login/2fa', methods=['GET', 'POST'])
@limiter.limit("5 per minute; 20 per hour", methods=["POST"])
@anonymous_required
def verify_2fa():
    # Drugi etap logowania (TOTP / 2FA):
    # - Sesja tymczasowa żyje max 5 minut
    # - Dopuszczamy max 5 prób wprowadzenia kodu przed unieważnieniem sesji
    # - is_totp_replayed blokuje ponowne użycie tego samego kodu w tym samym oknie czasowym
    user_id = session.get('2fa_user_id')
    login_time = session.get('2fa_time')
    now = utc_now().timestamp()
    if not user_id or not login_time or (now - login_time) > TWO_FACTOR_TTL_SECONDS:
        _clear_2fa_session()
        flash('Sesja logowania dwuetapowego wygasła lub jest nieprawidłowa. Zaloguj się ponownie.', 'warning')
        return redirect(url_for('auth.login'))
    user = db.session.get(User, user_id)
    if not user or not user.is_active or not user.is_otp_enabled or not user.otp_secret:
        _clear_2fa_session()
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        attempts = session.get('2fa_attempts', 0) + 1
        session['2fa_attempts'] = attempts
        if attempts > MAX_2FA_ATTEMPTS:
            _clear_2fa_session()
            flash('Przekroczono limit prób weryfikacji dwuetapowej. Zaloguj się ponownie.', 'danger')
            return redirect(url_for('auth.login'))

        verified, token = verify_totp_code(user.otp_secret, request.form.get('totp_token'))
        if is_totp_replayed(user.id, token):
            flash('Ten kod jednorazowy został już wykorzystany. Poczekaj na wygenerowanie nowego kodu w aplikacji.', 'danger')
            return render_template('auth/login_2fa.html')
        if verified:
            record_totp_used(user.id, token)
            next_page = _get_safe_next_url(session.pop('2fa_next', None))
            _clear_2fa_session()
            login_user(user)
            flash(f'Witaj z powrotem, {user.display_name}!', 'success')
            return redirect(next_page)
        else:
            remaining = MAX_2FA_ATTEMPTS - attempts
            if remaining > 0:
                flash(f'Nieprawidłowy 6-cyfrowy kod weryfikacyjny. Pozostałe próby: {remaining}.', 'danger')
            else:
                _clear_2fa_session()
                flash('Przekroczono limit prób weryfikacji dwuetapowej. Zaloguj się ponownie.', 'danger')
                return redirect(url_for('auth.login'))
    return render_template('auth/login_2fa.html')
def _get_reset_salt(user: User | None) -> str:
    # Sól z hasha hasła - zmiana hasła automatycznie unieważnia stare tokeny
    import hashlib
    if user and user.password_hash:
        pwd_fingerprint = hashlib.sha256(user.password_hash.encode('utf-8')).hexdigest()[:16]
    else:
        pwd_fingerprint = 'no-pwd'
    return f"{RESET_PASSWORD_SALT}-{pwd_fingerprint}"


def generate_reset_token(user_or_email: User | str) -> str:
    if isinstance(user_or_email, User):
        user = user_or_email
        email = user.email
    else:
        email = str(user_or_email).strip().lower()
        user = User.query.filter_by(email=email).first()
    salt = _get_reset_salt(user)
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def verify_reset_token(token: str, max_age: int = RESET_PASSWORD_MAX_AGE) -> str | None:
    # Weryfikacja kryptograficzna tokena resetu hasła:
    # Najpierw wyciągamy adres email z ładunku bez sprawdzania podpisu
    # odnajdujemy usera w bazie i generujemy dynamiczną sól z hasha obecnego hasła.
    # Jeśli hasło zostało już zmienione, podpis przestaje pasować.
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        _, email = serializer.loads_unsafe(token)
    except Exception:
        return None
    user = User.query.filter_by(email=email).first()
    if not user or not user.is_active:
        return None
    salt = _get_reset_salt(user)
    try:
        return serializer.loads(token, salt=salt, max_age=max_age)
    except Exception:
        return None


def dispatch_password_reset(user: User) -> tuple[str, bool]:
    token = generate_reset_token(user)
    base_url = current_app.config.get('APP_BASE_URL')
    if base_url:
        reset_url = f"{base_url.rstrip('/')}/reset-password/{token}"
    else:
        reset_url = url_for('auth.reset_password', token=token, _external=True)
    if current_app.config.get('TESTING') and has_request_context():
        session['last_reset_url'] = reset_url
    sent = send_password_reset_email(user, reset_url)
    return reset_url, sent


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@limiter.limit("5 per minute; 20 per day", methods=["POST"])
@anonymous_required
def forgot_password():
    form = ForgotPasswordForm()
    if validate_form_or_flash(form):
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user and user.is_active:
            reset_url, _ = dispatch_password_reset(user)
            if current_app.config.get('TESTING'):
                flash(f'Link resetujący (tryb deweloperski/testowy): {reset_url}', 'info')
            else:
                current_app.logger.info("Zgłoszono reset hasła dla konta: %s", email)
        flash('Jeśli konto z tym adresem e-mail istnieje, przesłano instrukcję resetowania hasła.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
@limiter.limit("5 per minute; 20 per day", methods=["POST"])
@anonymous_required
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('Link do resetowania hasła jest nieprawidłowy lub wygasł. Wygeneruj nowy link.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    user = User.query.filter_by(email=email).first()
    if not user or not user.is_active:
        flash('Konto użytkownika powiązane z tym linkiem nie istnieje lub zostało zablokowane.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    form = ResetPasswordForm()
    if validate_form_or_flash(form):
        user.set_password(form.new_password.data)
        if safe_db_commit(
            success_msg='Hasło zostało pomyślnie zaktualizowane. Możesz się teraz zalogować nowym hasłem.',
            error_msg='Wystąpił błąd podczas zapisywania nowego hasła. Spróbuj ponownie.'
        ):
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, token=token)