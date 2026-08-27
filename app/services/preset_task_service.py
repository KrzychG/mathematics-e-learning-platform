import os
import re
import json
from functools import lru_cache

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
_CANDIDATES = [
    os.path.join(_ROOT_DIR, 'content', 'preset_tasks.json'),
    os.path.join(_APP_DIR, 'content', 'preset_tasks.json'),
]
_JSON_PATH = next((p for p in _CANDIDATES if os.path.exists(p)), _CANDIDATES[0])
EXAM_TOPIC_NAME = "Arkusz Egzaminacyjny"


def normalize_question_key(text: str | None) -> str:
    if not text:
        return ''
    return re.sub(r'\s+', ' ', text.strip().lower())


@lru_cache(maxsize=1)
def load_preset_data() -> dict:
    if not os.path.exists(_JSON_PATH):
        return {"exam_tasks": [], "practice_fallback_tasks": {}}
    with open(_JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_preset_exam_tasks() -> list[dict]:
    return list(load_preset_data().get("exam_tasks", []))


@lru_cache(maxsize=1)
def get_preset_explanations_map() -> dict[str, str | None]:
    return {
        p["question"]: p.get("explanation")
        for p in get_preset_exam_tasks()
        if "question" in p
    }


def clamp_difficulty(raw_difficulty, default: int = 2) -> int:
    try:
        return max(1, min(5, int(raw_difficulty)))
    except (TypeError, ValueError):
        return default


def create_unique_exam_tasks(
    raw_items: list[dict],
    *,
    topic_id: int | None = None,
    existing_by_key: dict | None = None,
    seen_keys: set[str] | None = None,
    max_count: int | None = None,
    item_normalizer=None,
) -> list:
    from app import db
    from app.models import Task
    resolved_topic_id = topic_id if topic_id is not None else get_or_create_exam_topic().id
    seen = seen_keys if seen_keys is not None else set()
    existing = existing_by_key or {}
    tasks: list[Task] = []
    for item in raw_items:
        if max_count is not None and len(tasks) >= max_count:
            break
        q_text = str(item.get('question') or '').strip()
        q_key = normalize_question_key(q_text)
        if not q_text or not q_key or q_key in seen:
            continue
        task = existing.get(q_key)
        if task is None:
            payload = item_normalizer(item) if item_normalizer else item
            if not payload:
                continue
            task = Task(
                topic_id=resolved_topic_id,
                question=q_text,
                options=payload['options'],
                correct_answer=payload['correct_answer'],
                difficulty=clamp_difficulty(payload.get('difficulty', 2)),
                graph_data=payload.get('graph_data'),
                explanation=payload.get('explanation'),
            )
            db.session.add(task)
        seen.add(q_key)
        tasks.append(task)
    return tasks


def get_practice_fallback_bank() -> dict[int, list[dict]]:
    raw = load_preset_data().get("practice_fallback_tasks", {})
    return {int(k): v for k, v in raw.items()}


def get_or_create_exam_topic():
    from app import db
    from app.models import Topic, Category
    exam_topic = Topic.query.filter_by(name=EXAM_TOPIC_NAME).first()
    if exam_topic:
        return exam_topic
    fallback = Topic.query.first()
    if fallback:
        return fallback
    cat = Category.query.first()
    if not cat:
        cat = Category(name="Egzaminy")
        db.session.add(cat)
        db.session.flush()
    exam_topic = Topic(
        name=EXAM_TOPIC_NAME,
        description="Zadania wygenerowane do próbnych arkuszy egzaminacyjnych",
        category_id=cat.id
    )
    db.session.add(exam_topic)
    db.session.flush()
    return exam_topic
