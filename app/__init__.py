from flask import Flask, flash, redirect, request, url_for, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFError, CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import event, text
from sqlalchemy.engine import Engine
import sqlite3
import os
from config import Config, DockerConfig, ProductionConfig, config_dict, load_instance_secret_key

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection) or type(dbapi_connection).__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.close()


def get_rate_limit_key():
    if current_user and current_user.is_authenticated:
        return f"user:{current_user.id}"
    return get_remote_address()


limiter = Limiter(key_func=get_rate_limit_key)


def create_app(config_class=None):
    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    if config_class is None:
        config_class = os.environ.get('FLASK_CONFIG') or os.environ.get('FLASK_ENV') or 'default'
    
    if isinstance(config_class, str):
        app.config.from_object(config_dict.get(config_class.lower(), config_dict.get(config_class, Config)))
    else:
        app.config.from_object(config_class)

    is_production = (
        config_class is ProductionConfig
        or (isinstance(config_class, str) and config_class.lower() in ('production', 'prod'))
    )
    if is_production and not app.config.get('SECRET_KEY'):
        raise RuntimeError(
            'SECRET_KEY musi być ustawiony w zmiennych środowiskowych w środowisku produkcyjnym.'
        )

    is_docker = (
        config_class is DockerConfig
        or (isinstance(config_class, str) and config_class.lower() == 'docker')
    )
    if is_docker:
        if not app.config.get('SECRET_KEY'):
            app.config['SECRET_KEY'] = load_instance_secret_key(app.instance_path)

    if is_production or app.config.get('USE_PROXY_FIX', True):
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=app.config.get('PROXY_FIX_X_FOR', 1),
            x_proto=app.config.get('PROXY_FIX_X_PROTO', 1),
            x_host=app.config.get('PROXY_FIX_X_HOST', 0),
            x_prefix=app.config.get('PROXY_FIX_X_PREFIX', 1)
        )

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    from app.services.sanitizer_service import sanitize_theory_html, format_math
    from app.services.theory_renderer_service import render_theory_markdown
    app.jinja_env.filters['sanitize_html'] = sanitize_theory_html
    app.jinja_env.filters['format_math'] = format_math
    app.jinja_env.filters['render_theory'] = render_theory_markdown

    from app.services.timezone_service import (
        TIME_FORMAT_TEMPLATES,
        format_local_datetime,
        to_utc_iso,
    )
    app.jinja_env.filters['local_dt'] = format_local_datetime
    app.jinja_env.filters['utc_iso'] = to_utc_iso
    app.jinja_env.globals['TIME_FORMAT_TEMPLATES'] = TIME_FORMAT_TEMPLATES

    from app.models import (
        EXAM_PASS_RATIO,
        EXAM_REQUIRED_TASKS,
        UNCATEGORIZED_CATEGORY_LABEL,
    )
    from app.forms.auth_forms import PASSWORD_MIN_LENGTH

    exam_pass_percent = int(round(EXAM_PASS_RATIO * 100))
    app.jinja_env.globals.update(
        UNCATEGORIZED_LABEL=UNCATEGORIZED_CATEGORY_LABEL,
        PASSWORD_MIN_LENGTH=PASSWORD_MIN_LENGTH,
        EXAM_REQUIRED_TASKS=EXAM_REQUIRED_TASKS,
        EXAM_PASS_PERCENT=exam_pass_percent,
        EXAM_PASS_MIN_POINTS=int(round(EXAM_REQUIRED_TASKS * EXAM_PASS_RATIO)),
    )

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Zaloguj się, aby uzyskać dostęp do tej strony."
    login_manager.login_message_category = "warning"

    with app.app_context():
        from app.blueprints.auth.routes import auth_bp
        from app.blueprints.dashboard.routes import dashboard_bp
        from app.blueprints.learning.routes import learning_bp
        from app.blueprints.admin.routes import admin_bp
        from app.blueprints.exam.routes import exam_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(learning_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(exam_bp, url_prefix='/exam')

        from app.utils import wants_json_response

        @app.errorhandler(CSRFError)
        def handle_csrf_error(_error):
            flash('Sesja wygasła lub formularz jest nieprawidłowy. Spróbuj ponownie.', 'danger')
            return redirect(request.referrer or url_for('dashboard.index'))

        def _handle_error(e, code: int, error_msg: str):
            if wants_json_response():
                desc = getattr(e, 'description', str(e))
                return jsonify({
                    'success': False,
                    'error': error_msg,
                    'description': str(desc)
                }), code
            return render_template(f'errors/{code}.html', error=e), code

        @app.errorhandler(403)
        def handle_forbidden_error(e):
            return _handle_error(e, 403, 'Brak uprawnień do tego zasobu (403).')

        @app.errorhandler(404)
        def handle_not_found_error(e):
            return _handle_error(e, 404, 'Nie znaleziono żądanego zasobu (404).')

        @app.errorhandler(429)
        def handle_rate_limit_exceeded(e):
            return _handle_error(e, 429, 'Zbyt wiele żądań (Rate Limit). Odczekaj chwilę przed kolejną próbą.')

        @app.teardown_request
        def teardown_request_func(exception=None):
            if exception:
                db.session.rollback()

        @app.after_request
        def add_security_headers(response):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.cdnfonts.com; "
                "font-src 'self' https://cdn.jsdelivr.net https://fonts.cdnfonts.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self'; "
                "frame-ancestors 'self'; "
                "base-uri 'self'; "
                "form-action 'self';"
            )
            if is_production or app.config.get('FORCE_HSTS', False):
                response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
            return response

        @app.errorhandler(500)
        def handle_internal_server_error(e):
            db.session.rollback()
            app.logger.error("Wewnętrzny błąd serwera (500): %s", e, exc_info=True)
            if wants_json_response():
                description = str(e) if app.config.get('DEBUG') else "Wystąpił nieoczekiwany błąd serwera."
                return jsonify({
                    'success': False,
                    'error': 'Wewnętrzny błąd serwera. Transakcja została wycofana.',
                    'description': description
                }), 500
            error_to_render = e if app.config.get('DEBUG') else None
            return render_template('errors/500.html', error=error_to_render), 500

        @app.get('/healthz')
        @limiter.exempt
        def healthcheck():
            try:
                db.session.execute(text('SELECT 1'))
            except Exception:
                return jsonify({'status': 'error'}), 503
            return jsonify({'status': 'ok'}), 200

    return app
