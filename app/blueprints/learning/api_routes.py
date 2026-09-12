from flask import request, session
from flask_login import current_user, login_required
from app import db, limiter
from app.models import Topic, Task
from app.services.progress_service import get_current_difficulty
from app.utils import is_ajax_request, json_error, json_success
from app.services.sanitizer_service import format_math
from app.blueprints.learning.routes import (
    learning_bp,
    _pending_topic_task_key,
    _pick_random_topic,
    _get_active_random_task,
    _task_topic_meta,
    _resolve_existing_task,
    _try_generate_pending_task,
)

def _validate_get_task_request() -> tuple[bool, tuple | None]:
    # Ochrona przed nadużyciami endpointu pobierania zadań
    # Odrzucamy żądania cross-site i niedozwolone Sec-Fetch-Dest, a przy wymuszeniu nowego zadania 
    # wymagamy nagłówka AJAX lub metody POST z tokenem CSRF, żeby boty i prefetchery nie paliły limitu LLM.
    sec_dest = request.headers.get('Sec-Fetch-Dest', '').lower()
    if sec_dest in ('image', 'script', 'style', 'video', 'audio', 'embed', 'object', 'track'):
        return False, json_error("Niedozwolony typ żądania (Sec-Fetch-Dest).", 400)
    sec_site = request.headers.get('Sec-Fetch-Site', '').lower()
    if sec_site == 'cross-site':
        return False, json_error("Żądania cross-site do tego zasobu są zabronione.", 403)
    json_data = request.get_json(silent=True) or {}
    force_new = (
        request.args.get('force_new', type=int) == 1
        or json_data.get('force_new') in (1, True, '1', 'true')
    )
    if force_new and request.method == 'GET' and not is_ajax_request():
        return False, json_error(
            "Wymuszenie nowego zadania metodą GET bez nagłówka AJAX (X-Requested-With: XMLHttpRequest) jest niedozwolone ze względów bezpieczeństwa (CSRF). Użyj metody POST z tokenem CSRF lub żądania AJAX.",
            400,
        )
    return force_new, None


def _format_task_json_payload(task_data: dict) -> dict:
    payload = dict(task_data)
    payload["formatted_question"] = format_math(payload.get("question"))
    raw_options = payload.get("options") or {}
    payload["formatted_options"] = {k: format_math(v) for k, v in raw_options.items()}
    return payload


def _build_task_json_response(task_data: dict, *, topic: Topic | None = None, reused: bool):
    if topic is not None:
        task_data.update(_task_topic_meta(topic))
    task_data["reused"] = reused
    return json_success(**_format_task_json_payload(task_data))


def _generate_task_json_response(topic: Topic, session_key: str, include_topic_meta: bool = False):
    difficulty = get_current_difficulty(current_user.id, topic.id)
    task_data, err = _try_generate_pending_task(topic.id, difficulty, session_key)
    if err is not None or task_data is None:
        return json_error(f"Nie udało się przygotować zadania: {str(err)}", 500)
    return _build_task_json_response(
        task_data,
        topic=topic if include_topic_meta else None,
        reused=False,
    )


def _serve_or_generate_task_json(context_loader, *, include_topic_meta: bool = False):
    force_new, err_resp = _validate_get_task_request()
    if err_resp:
        return err_resp
    existing_task, topic, session_key, err_resp = context_loader(force_new)
    if err_resp:
        return err_resp
    if existing_task:
        meta_topic = existing_task.topic if include_topic_meta else None
        return _build_task_json_response(
            existing_task.to_view_dict(),
            topic=meta_topic,
            reused=True,
        )
    return _generate_task_json_response(topic, session_key, include_topic_meta=include_topic_meta)


def _load_random_task_context(force_new: bool):
    if not force_new:
        active_task = _get_active_random_task(current_user.id)
        if active_task:
            return active_task, active_task.topic, 'pending_random_task', None
    exclude_topic_id = None
    prev_task_id = session.pop('pending_random_task', None)
    if prev_task_id:
        session['_prev_pending_random_task'] = prev_task_id
        prev_task = db.session.get(Task, prev_task_id)
        if prev_task:
            exclude_topic_id = prev_task.topic_id
    topic = _pick_random_topic(exclude_topic_id=exclude_topic_id)
    if not topic:
        return None, None, 'pending_random_task', json_error("Brak dostępnych tematów w bazie danych.", 404)
    return None, topic, 'pending_random_task', None


@learning_bp.route('/practice/random/get-task', methods=['GET', 'POST'])
@login_required
@limiter.limit("15 per minute; 60 per hour")
def get_or_create_random_task():
    return _serve_or_generate_task_json(_load_random_task_context, include_topic_meta=True)


@learning_bp.route('/practice/<int:topic_id>/get-task', methods=['GET', 'POST'])
@login_required
@limiter.limit("15 per minute; 60 per hour")
def get_or_create_task(topic_id):
    def _load_topic_task_context(force_new: bool):
        topic = db.get_or_404(Topic, topic_id)
        existing_task = _resolve_existing_task(current_user.id, topic.id, force_new=force_new)
        return existing_task, topic, _pending_topic_task_key(topic.id), None
    return _serve_or_generate_task_json(_load_topic_task_context)
