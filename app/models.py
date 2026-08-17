import json
from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.mutable import MutableDict, MutableList
from werkzeug.security import check_password_hash, generate_password_hash
from app.services.sanitizer_service import (
    clean_latex,
    empty_if_meaningless,
    has_meaningful_theory,
    normalize_theory_input,
)
from app.services.timezone_service import ensure_utc, format_duration_seconds, utc_now


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    avatar_filename = db.Column(db.String(255), nullable=True)
    otp_secret = db.Column(db.String(255), nullable=True)
    is_otp_enabled = db.Column(db.Boolean, default=False)

    attempts = db.relationship('Attempt', backref='user', lazy='select', cascade='all, delete-orphan')
    progress = db.relationship('UserTopicProgress', backref='user', lazy='select', cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', backref='user', lazy='select', cascade='all, delete-orphan')
    exam_attempts = db.relationship('ExamAttempt', backref='user', lazy='select', cascade='all, delete-orphan')

    @property
    def display_name(self):
        name = (self.first_name or '').strip()
        if name:
            return name
        if self.email:
            return self.email.split('@')[0]
        return 'Uczeń'

    @property
    def initials(self):
        return self.display_name[0].upper()

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return bool(password) and check_password_hash(self.password_hash, password)

    def disable_2fa(self) -> None:
        self.is_otp_enabled = False
        self.otp_secret = None


UNCATEGORIZED_CATEGORY_LABEL = 'Bez kategorii'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    topics = db.relationship('Topic', backref='category', lazy='select')

    @classmethod
    def get_syllabus_tree(cls) -> tuple[list['Category'], list['Topic']]:
        # Pobiera pełną strukturę sylabusa
        # Używamy joinedload, żeby uniknąć N+1 zapytań przy renderowaniu menu bocznego i dashboardu.
        from sqlalchemy.orm import joinedload
        categories = (
            cls.query
            .options(joinedload(cls.topics))
            .order_by(cls.id.asc())
            .all()
        )
        uncategorized = (
            Topic.query
            .filter_by(category_id=None)
            .order_by(Topic.id.asc())
            .all()
        )
        return categories, uncategorized


class Topic(db.Model):
    __tablename__ = 'topics'
    __table_args__ = (
        db.UniqueConstraint('category_id', 'name', name='uq_topic_category_name'),
        db.Index(
            'uq_topic_uncategorized_name',
            'name',
            unique=True,
            sqlite_where=db.text('category_id IS NULL'),
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    theory = db.Column(db.Text)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', name='fk_topics_categories', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )

    tasks = db.relationship('Task', backref='topic', lazy='select', cascade="all, delete-orphan")
    progress = db.relationship('UserTopicProgress', backref='topic', lazy='select', cascade="all, delete-orphan")

    @property
    def has_theory(self) -> bool:
        return has_meaningful_theory(self.theory)

    @property
    def category_label(self) -> str:
        return self.category.name if self.category else UNCATEGORIZED_CATEGORY_LABEL

    @staticmethod
    def normalize_theory_value(value: str | None) -> str | None:
        # Sanityzacja teorii przed zapisem do bazy
        if value is None:
            return None
        val_str = str(value).strip()
        if not val_str:
            return ''
        if val_str.startswith('<') and '>' in val_str:
            return normalize_theory_input(val_str)
        import re
        from app.services.sanitizer_service import SCRIPT_REGEX, DANGLING_SCRIPT_REGEX
        cleaned = clean_latex(val_str)
        cleaned = SCRIPT_REGEX.sub('', cleaned)
        cleaned = DANGLING_SCRIPT_REGEX.sub('', cleaned)
        cleaned = re.sub(r'(?i)\bon\w+\s*=\s*(["\']).*?\1', '', cleaned)
        return empty_if_meaningless(cleaned)

    def set_sanitized_theory(self, sanitized_html: str | None) -> None:
        normalized = None if sanitized_html is None else empty_if_meaningless(sanitized_html)
        self._skip_theory_validation = True
        try:
            self.theory = normalized
        finally:
            self._skip_theory_validation = False

    @validates('theory')
    def validate_theory(self, key, value):
        if getattr(self, '_skip_theory_validation', False):
            return value
        return self.normalize_theory_value(value)

class Task(db.Model):
    __tablename__ = 'tasks'
    __table_args__ = (
        db.Index('ix_tasks_topic_difficulty', 'topic_id', 'difficulty'),
    )
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=True)
    correct_answer = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.Integer, default=1)
    graph_data = db.Column(db.JSON, nullable=True)
    explanation = db.Column(db.Text, nullable=True)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
    
    attempts = db.relationship('Attempt', backref='task', lazy='select', cascade="all, delete-orphan")

    @validates('question')
    def validate_question(self, key, value):
        return clean_latex(value)

    @validates('options')
    def validate_options(self, key, value):
        if not value:
            return None
        parsed = self._as_json_dict(value)
        if parsed is None:
            return None
        return {
            str(k).strip().upper(): clean_latex(v) if isinstance(v, str) else v
            for k, v in parsed.items()
        }

    @staticmethod
    def _as_json_dict(raw_value) -> dict | None:
        if isinstance(raw_value, dict):
            return raw_value
        if isinstance(raw_value, str):
            try:
                parsed = json.loads(raw_value)
                return parsed if isinstance(parsed, dict) else None
            except Exception:
                return None
        return None

    @property
    def options_dict(self) -> dict:
        return self._as_json_dict(self.options) or {}

    @property
    def has_four_options(self) -> bool:
        return len(self.options_dict) == 4

    @property
    def graph_spec(self) -> dict | None:
        return self._as_json_dict(self.graph_data)

    def to_view_dict(self) -> dict:
        return {
            "task_id": self.id,
            "question": self.question,
            "options": self.options_dict,
            "difficulty": self.difficulty,
            "graph_spec": self.graph_spec,
        }


class Attempt(db.Model):
    __tablename__ = 'attempts'
    __table_args__ = (
        db.Index('ix_attempts_user_task', 'user_id', 'task_id'),
        db.Index('ix_attempts_user_created', 'user_id', 'created_at'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False, index=True)
    user_answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean, default=False)
    llm_hint_provided = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)


class UserTopicProgress(db.Model):
    __tablename__ = 'user_topic_progress'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id', ondelete='CASCADE'), primary_key=True, index=True)
    current_difficulty = db.Column(db.Integer, default=1)
    consecutive_correct = db.Column(db.Integer, default=0)
    consecutive_wrong = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=utc_now)

    @property
    def mastery_percent(self) -> int:
        lvl = int(self.current_difficulty or 1)
        return int((lvl / 5.0) * 100)


class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    trigger_condition = db.Column(db.String(100), unique=True)
    icon_class = db.Column(db.String(255))


class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id', ondelete='CASCADE'), primary_key=True, index=True)
    unlocked_at = db.Column(db.DateTime, default=utc_now)
    achievement = db.relationship('Achievement')


EXAM_REQUIRED_TASKS = 20
EXAM_PASS_RATIO = 0.30


class ExamAttempt(db.Model):
    __tablename__ = 'exam_attempts'
    __table_args__ = (
        db.Index('ix_exam_attempts_user_completed', 'user_id', 'is_completed'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(120), default='Próbny Egzamin - Poziom Podstawowy')
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Integer, default=0)
    total_tasks = db.Column(db.Integer, default=EXAM_REQUIRED_TASKS)
    passed = db.Column(db.Boolean, default=False)
    is_completed = db.Column(db.Boolean, default=False)
    
    task_ids = db.Column(MutableList.as_mutable(db.JSON), nullable=False, default=list)
    answers = db.Column(MutableDict.as_mutable(db.JSON), nullable=False, default=dict)

    @property
    def percentage(self) -> int:
        if not self.total_tasks or self.total_tasks <= 0:
            return 0
        return int(round(((self.score or 0) / self.total_tasks) * 100))

    @property
    def time_spent_seconds(self) -> int:
        if not self.created_at:
            return 0
        start = ensure_utc(self.created_at)
        end = ensure_utc(self.completed_at or utc_now())
        return max(0, int((end - start).total_seconds()))

    @property
    def formatted_time_spent(self) -> str:
        return format_duration_seconds(self.time_spent_seconds)

    def prune_missing_task_ids(self, valid_ids: set[int]) -> bool:
        # Jeśli zadanie zostało skasowane z bazy przez CMS w trakcie trwającego egzaminu,
        # usuwamy osierocone ID z JSON-a i aktualizujemy total_tasks, chroniąc przed wywaleniem widoku.
        current_ids = list(self.task_ids or [])
        cleaned_ids = [tid for tid in current_ids if tid in valid_ids]
        current_answers = dict(self.answers or {})
        cleaned_answers = {
            k: v for k, v in current_answers.items()
            if str(k).isdigit() and int(k) in valid_ids
        }
        if cleaned_ids == current_ids and cleaned_answers == current_answers:
            return False
        self.task_ids = cleaned_ids
        self.answers = cleaned_answers
        if not self.is_completed:
            self.total_tasks = len(cleaned_ids)
        return True



