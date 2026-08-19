import re
from flask import flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d).+$'


def flash_form_errors(form: FlaskForm, category: str = 'danger') -> None:
    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, category)


def validate_form_or_flash(form: FlaskForm, category: str = 'danger') -> bool:
    if form.validate_on_submit():
        return True
    if request.method == 'POST':
        flash_form_errors(form, category=category)
    return False


def validate_password_complexity(password: str, label: str = 'Hasło') -> tuple[bool, str | None]:
    if not password or len(password) < PASSWORD_MIN_LENGTH or not re.search(PASSWORD_REGEX, password):
        return (
            False,
            f'{label} musi mieć co najmniej {PASSWORD_MIN_LENGTH} znaków oraz zawierać co najmniej jedną literę i co najmniej jedną cyfrę.',
        )
    if len(password) > PASSWORD_MAX_LENGTH:
        return False, f'{label} może mieć maksymalnie {PASSWORD_MAX_LENGTH} znaków.'
    return True, None


def _password_rule_validator(label: str = 'Hasło', *, required: bool = True):
    def _validator(form, field):
        raw_val = field.data or ''
        pwd = raw_val if required else raw_val.strip()
        if not pwd:
            if not required and raw_val:
                raise ValidationError(f'{label} nie może składać się wyłącznie ze spacji.')
            return
        valid, msg = validate_password_complexity(pwd, label=label)
        if not valid:
            raise ValidationError(msg)

    return _validator


def password_validators(prefix: str = '') -> list:
    name = f'{prefix} hasło' if prefix else 'Hasło'
    return [
        DataRequired(message=f'{name} jest wymagane.'),
        _password_rule_validator(label=name, required=True),
    ]


def _strip_string(value):
    return value.strip() if isinstance(value, str) else value


def _first_name_field(*, combined_msg: str | None = None):
    return StringField(
        'Imię',
        filters=[_strip_string],
        validators=[
            DataRequired(message=combined_msg or 'Imię jest wymagane.'),
            Length(min=2, max=50, message=combined_msg or 'Imię musi mieć od 2 do 50 znaków.'),
        ]
    )


def _strip_lower_string(value):
    return value.strip().lower() if isinstance(value, str) else value


def _email_field(*, required_msg: str = 'Adres e-mail jest wymagany.', max_length: int | None = None):
    validators = [
        DataRequired(message=required_msg),
        Email(message='Podaj poprawny adres e-mail.'),
    ]
    if max_length is not None:
        validators.append(Length(max=max_length, message=f'Adres e-mail może mieć maksymalnie {max_length} znaków.'))
    return StringField('Adres e-mail', filters=[_strip_lower_string], validators=validators)


def _confirm_password_field(
    target_field: str = 'password',
    *,
    label: str = 'Powtórz hasło',
    required_msg: str = 'Powtórzenie hasła jest wymagane.',
    mismatch_msg: str = 'Hasła nie są identyczne.',
):
    return PasswordField(
        label,
        validators=[
            DataRequired(message=required_msg),
            EqualTo(target_field, message=mismatch_msg),
        ]
    )


class LoginForm(FlaskForm):
    email = _email_field()
    password = PasswordField('Hasło', validators=[DataRequired(message='Hasło jest wymagane.')])


class ProfileForm(FlaskForm):
    first_name = _first_name_field()


class RegisterForm(FlaskForm):
    first_name = _first_name_field()
    email = _email_field()
    password = PasswordField('Hasło', validators=password_validators())
    confirm_password = _confirm_password_field()


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Aktualne hasło',
        validators=[DataRequired(message='Aktualne hasło jest wymagane.')]
    )
    new_password = PasswordField('Nowe hasło', validators=password_validators('Nowe'))
    confirm_password = _confirm_password_field(
        'new_password',
        label='Powtórz nowe hasło',
        required_msg='Powtórzenie nowego hasła jest wymagane.',
        mismatch_msg='Nowe hasła nie są identyczne.',
    )


class ForgotPasswordForm(FlaskForm):
    email = _email_field()
    submit = SubmitField('Wyślij link do resetu')


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Nowe hasło', validators=password_validators('Nowe'))
    confirm_password = _confirm_password_field(
        'new_password',
        label='Powtórz nowe hasło',
        required_msg='Powtórzenie nowego hasła jest wymagane.',
    )
    submit = SubmitField('Zmień hasło i zaloguj się')


class AdminCreateUserForm(FlaskForm):
    first_name = _first_name_field(combined_msg='Imię jest wymagane i musi zawierać od 2 do 50 znaków.')
    email = _email_field(required_msg='Podaj poprawny adres e-mail.', max_length=120)
    role = SelectField(
        'Rola',
        choices=[
            ('student', 'Uczeń (Dostęp do nauki, zadań i egzaminów)'),
            ('admin', 'Administrator (Pełny dostęp zarządczy)'),
        ],
        default='student'
    )
    password = PasswordField('Hasło początkowe', validators=[_password_rule_validator(required=False)])
    is_active = BooleanField('Konto aktywne', default=True)
    send_welcome_email = BooleanField('Wyślij powitanie', default=False)


class AdminEditUserForm(FlaskForm):
    first_name = _first_name_field(combined_msg='Imię jest wymagane i musi zawierać od 2 do 50 znaków.')
    email = _email_field(required_msg='Podaj poprawny adres e-mail.', max_length=120)
    new_password = PasswordField('Nowe hasło', validators=[_password_rule_validator(required=False)])
    remove_avatar = BooleanField('Usuń awatar użytkownika', default=False)


