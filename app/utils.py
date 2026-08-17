from flask import flash, jsonify, request
from app import db


def safe_db_commit(
    success_msg: str | None = None,
    error_msg: str = 'Wystąpił błąd podczas zapisywania w bazie danych.',
    success_category: str = 'success',
    error_category: str = 'danger'
) -> bool:
    # Bezpieczny commit do bazy danych z automatycznym rollbackiem w razie wyjątku:
    # Zwraca True/False i wyświetla odpowiedni komunikat flash, zapobiegając zawieszeniu sesji SQLAlchemy.
    try:
        db.session.commit()
        if success_msg:
            flash(success_msg, success_category)
        return True
    except Exception:
        db.session.rollback()
        if error_msg:
            flash(error_msg, error_category)
        return False


def has_duplicate(model, *filters, exclude_id: int | None = None) -> bool:
    query = model.query.filter(*filters)
    if exclude_id is not None:
        query = query.filter(model.id != exclude_id)
    return query.first() is not None


def is_ajax_request() -> bool:
    return (
        request.is_json
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    )


def wants_json_response() -> bool:
    # Wykrywa, czy klient oczekuje odpowiedzi JSON zamiast przekierowania HTML:
    # Sprawdza nagłówki AJAX (X-Requested-With: XMLHttpRequest) oraz preferencje MIME (Accept: application/json).
    return (
        is_ajax_request()
        or 'application/json' in request.headers.get('Accept', '')
        or request.accept_mimetypes['application/json'] > request.accept_mimetypes['text/html']
    )


def json_success(**payload):
    return jsonify({"success": True, **payload})


def json_error(message: str, status: int = 400, **extra):
    return jsonify({"success": False, "error": message, **extra}), status
