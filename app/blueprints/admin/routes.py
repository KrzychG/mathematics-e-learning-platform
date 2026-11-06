from functools import wraps
from flask import Blueprint, abort, redirect, request, url_for
from flask_login import current_user, login_required

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    # Dekorator dostępu do strefy administracyjnej:
    # Wymaga zalogowania oraz flagi is_admin == True
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return login_required(decorated_function)
__all__ = ['admin_bp', 'admin_required', 'redirect_to_admin_list']


def redirect_to_admin_list():
    # Bezpieczny powrót do poprzedniej podstrony
    # Sprawdza referrer pod kątem open redirect – wraca do referrera tylko, gdy host się zgadza i ścieżka zaczyna się od /admin.
    ref = request.referrer
    if ref:
        from urllib.parse import urlsplit
        parsed = urlsplit(ref)
        if (not parsed.netloc or parsed.netloc == request.host) and parsed.path.startswith('/admin'):
            return redirect(ref)
    return redirect(url_for('admin.admin_dashboard'))
from app.blueprints.admin import content_routes, user_routes 
