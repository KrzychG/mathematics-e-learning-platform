"""
Serwis Historii i Audytu Aktywności Ucznia
Zasila widok pełnej historii rozwiązywania zadań i egzaminów
Wykorzystuje wrapper polimorficzny HistoryEntry łączący próby zadań i egzaminy
Obsługuje zaawansowane filtrowanie typ aktywności, status poprawności poprawne/błędne
Implementuje bezpieczną paginację w pamięci z zabezpieczeniem granic stron
"""

from sqlalchemy import literal, func, desc
from sqlalchemy.orm import joinedload
from app import db
from app.models import Attempt, ExamAttempt, Task, Topic
from app.services.timezone_service import format_duration_seconds

class HistoryEntry:
    def __init__(self, kind: str, obj):
        self.kind = kind
        self.id = obj.id
        self.is_task = (kind == 'task')
        self.is_exam = not self.is_task
        if self.is_task:
            self.created_at = obj.created_at
            self.is_correct = obj.is_correct
            self.task = obj.task
            self.user_answer = obj.user_answer
            self.llm_hint_provided = obj.llm_hint_provided
        else:
            self.created_at = obj.completed_at or obj.created_at
            self.is_correct = obj.passed
            self.exam = obj
            self.title = obj.title or 'Próbny Egzamin'
            self.score = obj.score
            self.total_tasks = obj.total_tasks
            self.percentage = obj.percentage
            self.passed = obj.passed
            self.time_spent_seconds = obj.time_spent_seconds
    @property
    def formatted_time_spent(self) -> str:
        if not self.is_exam:
            return ""
        return format_duration_seconds(self.time_spent_seconds)
def _filter_by_outcome(query, outcome_col, status_filter: str):
    if status_filter == 'correct':
        return query.filter(outcome_col.is_(True))
    if status_filter == 'incorrect':
        return query.filter(outcome_col.is_(False))
    return query
def clamp_page_bounds(total: int, page: int, per_page: int) -> tuple[int, int]:
    pages = max(1, (total + per_page - 1) // per_page) if per_page else 1
    clamped_page = max(1, min(page or 1, pages))
    return clamped_page, pages


def load_entities_by_ids(query, id_column, ids) -> dict:
    if not ids:
        return {}
    return {obj.id: obj for obj in query.filter(id_column.in_(ids)).all()}


class MemoryPagination:
    def __init__(self, page, per_page, total, items):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items
        _, self.pages = clamp_page_bounds(total, page, per_page)

    @classmethod
    def from_sequence(cls, sequence, page: int, per_page: int):
        total = len(sequence)
        clamped_page, _ = clamp_page_bounds(total, page, per_page)
        start = (clamped_page - 1) * per_page if per_page else 0
        items = list(sequence[start:start + per_page]) if per_page else list(sequence)
        return cls(page=clamped_page, per_page=per_page, total=total, items=items)
    @property
    def has_prev(self):
        return self.page > 1
    @property
    def has_next(self):
        return self.page < self.pages
    @property
    def prev_num(self):
        return self.page - 1
    @property
    def next_num(self):
        return self.page + 1
    def iter_pages(self, left_edge=1, right_edge=1, left_current=2, right_current=2):
        last = 0
        for num in range(1, self.pages + 1):
            if (
                num <= left_edge
                or (self.page - left_current <= num <= self.page + right_current)
                or num > self.pages - right_edge
            ):
                if last + 1 != num:
                    yield None
                yield num
                last = num
def paginate_clamped(target, page: int, per_page: int):
    # Bezpieczne stronicowanie zapytań SQL oraz list w pamięci
    # W razie podania strony poza zakresem (np. page=999) automatycznie przycina do ostatniej
    # dostępnej strony zamiast rzucać 404 czy zwracać pustą listę.
    safe_page = max(1, page or 1)
    if not hasattr(target, 'paginate'):
        return MemoryPagination.from_sequence(target, page=safe_page, per_page=per_page)
    pagination = target.paginate(page=safe_page, per_page=per_page, error_out=False)
    if pagination.pages > 0 and safe_page > pagination.pages:
        pagination = target.paginate(page=pagination.pages, per_page=per_page, error_out=False)
    return pagination


def get_user_history_paginated(user_id: int, type_filter: str = 'all', status_filter: str = 'all', page: int = 1, per_page: int = 20):
    if type_filter in ('tasks', 'exams'):
        if type_filter == 'tasks':
            entry_type = 'task'
            query = (
                Attempt.query
                .options(joinedload(Attempt.task).joinedload(Task.topic).joinedload(Topic.category))
                .filter_by(user_id=user_id)
            )
            query = _filter_by_outcome(query, Attempt.is_correct, status_filter).order_by(Attempt.id.desc())
        else:
            entry_type = 'exam'
            query = ExamAttempt.query.filter_by(user_id=user_id, is_completed=True)
            query = _filter_by_outcome(query, ExamAttempt.passed, status_filter).order_by(ExamAttempt.id.desc())
        pagination = paginate_clamped(query, page=page, per_page=per_page)
        pagination.items = [HistoryEntry(entry_type, item) for item in pagination.items]
        return pagination
    else:
        task_sub = (
            db.session.query(
                literal('task').label('entry_type'),
                Attempt.id.label('id'),
                Attempt.created_at.label('created_at')
            )
            .filter(Attempt.user_id == user_id)
        )
        task_sub = _filter_by_outcome(task_sub, Attempt.is_correct, status_filter)
        exam_sub = (
            db.session.query(
                literal('exam').label('entry_type'),
                ExamAttempt.id.label('id'),
                func.coalesce(ExamAttempt.completed_at, ExamAttempt.created_at).label('created_at')
            )
            .filter(ExamAttempt.user_id == user_id, ExamAttempt.is_completed.is_(True))
        )
        exam_sub = _filter_by_outcome(exam_sub, ExamAttempt.passed, status_filter)
        combined_union = task_sub.union_all(exam_sub).subquery()
        total_items = db.session.query(func.count()).select_from(combined_union).scalar() or 0
        clamped_page, _ = clamp_page_bounds(total_items, page, per_page)
        page_rows = (
            db.session.query(combined_union.c.entry_type, combined_union.c.id)
            .order_by(desc(combined_union.c.created_at), desc(combined_union.c.id))
            .limit(per_page)
            .offset((clamped_page - 1) * per_page)
            .all()
        )
        page_task_ids = [row.id for row in page_rows if row.entry_type == 'task']
        page_exam_ids = [row.id for row in page_rows if row.entry_type == 'exam']
        tasks_by_id = load_entities_by_ids(
            Attempt.query.options(joinedload(Attempt.task).joinedload(Task.topic).joinedload(Topic.category)),
            Attempt.id,
            page_task_ids,
        )
        exams_by_id = load_entities_by_ids(ExamAttempt.query, ExamAttempt.id, page_exam_ids)
        entity_map = {'task': tasks_by_id, 'exam': exams_by_id}
        page_items = [
            HistoryEntry(row.entry_type, entity_map[row.entry_type][row.id])
            for row in page_rows
            if row.id in entity_map.get(row.entry_type, {})
        ]
        return MemoryPagination(page=clamped_page, per_page=per_page, total=total_items, items=page_items)
