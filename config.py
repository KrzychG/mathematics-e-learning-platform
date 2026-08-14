import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def _bool_env(key: str, default: str = 'false') -> bool:
    return os.environ.get(key, default).lower() in ('true', '1', 'yes')


def load_instance_secret_key(instance_path: str, filename: str = '.secret_key') -> str | None:
    # Utrwalanie klucza sesji w Dockerze
    # Zapobiega wylogowywaniu wszystkich użytkowników po restarcie kontenera, gdy zmienna SECRET_KEY nie została przekazana.
    env_key = os.environ.get('SECRET_KEY')
    if env_key:
        return env_key
    secret_file = os.path.join(instance_path, filename)
    if os.path.isfile(secret_file):
        try:
            with open(secret_file, 'r', encoding='utf-8') as f:
                val = f.read().strip()
                return val or None
        except OSError:
            pass
    return None


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    APP_BASE_URL = os.environ.get('APP_BASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.8-flash')
    FORCE_HSTS = _bool_env('FORCE_HSTS', 'false')
    USE_PROXY_FIX = _bool_env('USE_PROXY_FIX', 'true')
    PROXY_FIX_X_FOR = int(os.environ.get('PROXY_FIX_X_FOR', 1))
    PROXY_FIX_X_PROTO = int(os.environ.get('PROXY_FIX_X_PROTO', 1))
    PROXY_FIX_X_HOST = int(os.environ.get('PROXY_FIX_X_HOST', 0))
    PROXY_FIX_X_PREFIX = int(os.environ.get('PROXY_FIX_X_PREFIX', 1))
    
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    RATELIMIT_DEFAULT = "2000 per day; 500 per hour"

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = _bool_env('MAIL_USE_TLS', 'true')
    MAIL_USE_SSL = _bool_env('MAIL_USE_SSL', 'false')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or os.environ.get('MAIL_USERNAME') or 'no-reply@axioma.pl'
    MAIL_SENDER_NAME = os.environ.get('MAIL_SENDER_NAME', 'Axioma - Platforma Edukacyjna')
    MAIL_TIMEOUT = int(os.environ.get('MAIL_TIMEOUT', 10))
    MAIL_SUPPRESS_SEND = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    GEMINI_API_KEY = None

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    FORCE_HSTS = True

class DockerConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = _bool_env('SESSION_COOKIE_SECURE', 'false')
    FORCE_HSTS = _bool_env('FORCE_HSTS', 'false')

config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}
