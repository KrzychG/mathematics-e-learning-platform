import random
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import (
    Achievement,
    Attempt,
    ExamAttempt,
    Task,
    Topic,
    User,
    UserAchievement,
    UserTopicProgress,
)
from app.services.preset_task_service import (
    create_unique_exam_tasks,
    get_or_create_exam_topic,
    get_preset_exam_tasks,
    normalize_question_key,
)
from seed import seed_all


def _get_or_create_demo_user(email: str, first_name: str, password: str, is_admin: bool = False, is_active: bool = True) -> User:
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            email=email,
            first_name=first_name,
            password_hash=generate_password_hash(password),
            is_admin=is_admin,
            is_active=is_active,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=30),
        )
        db.session.add(user)
        db.session.flush()
    else:
        user.first_name = first_name
        user.password_hash = generate_password_hash(password)
        user.is_admin = is_admin
        user.is_active = is_active
        db.session.flush()
    return user


def _ensure_exam_tasks() -> list[Task]:
    fallback_topic = get_or_create_exam_topic()
    preset_items = get_preset_exam_tasks()
    preset_questions = [p["question"] for p in preset_items if "question" in p]

    existing_preset = {
        normalize_question_key(t.question): t
        for t in Task.query.filter(Task.question.in_(preset_questions)).all()
    }

    create_unique_exam_tasks(
        preset_items,
        topic_id=fallback_topic.id,
        existing_by_key=existing_preset,
    )
    db.session.commit()

    all_exam_tasks = (
        Task.query.filter_by(topic_id=fallback_topic.id)
        .order_by(Task.id.asc())
        .limit(20)
        .all()
    )
    return all_exam_tasks


def _ensure_topic_practice_tasks(topics: list[Topic]) -> list[Task]:
    tasks = []
    sample_definitions = [
        ("Dla jakiej wartości parametru $m$ prosta $y = (2m-4)x + 3$ jest rosnąca?", {"A": "$m > 2$", "B": "$m < 2$", "C": "$m = 2$", "D": "$m > 0$"}, "A", 2, r"Prosta jest rosnąca, gdy współczynnik kierunkowy $a > 0$, czyli $2m - 4 > 0 \implies m > 2$."),
        ("Wierzchołek paraboli o równaniu $y = 2(x-3)^2 + 5$ ma współrzędne:", {"A": "$(-3, 5)$", "B": "$(3, 5)$", "C": "$(3, -5)$", "D": "$(-3, -5)$"}, "B", 1, "Z postaci kanonicznej $y = a(x-p)^2 + q$ odczytujemy wierzchołek $W = (p, q) = (3, 5)$."),
        ("Wskaż rozwiązanie równania $|x - 4| = 7$:", {"A": "$x = 11$ lub $x = -3$", "B": "$x = 11$", "C": "$x = 3$", "D": "$x = -11$ lub $x = 3$"}, "A", 2, r"$x - 4 = 7 \implies x = 11$ lub $x - 4 = -7 \implies x = -3$."),
        ("Liczba $\\log_2 32 - \\log_2 4$ jest równa:", {"A": "$3$", "B": "$4$", "C": "$2$", "D": "$8$"}, "A", 1, "$\\log_2(32 / 4) = \\log_2 8 = 3$."),
        ("Ciąg arytmetyczny $(a_n)$ ma wyrazy $a_1 = 3$ oraz $a_2 = 7$. Ile wynosi dziesiąty wyraz $a_{10}$?", {"A": "$39$", "B": "$43$", "C": "$35$", "D": "$40$"}, "A", 2, "Różnica $r = 7 - 3 = 4$. $a_{10} = a_1 + 9r = 3 + 36 = 39$."),
        ("W trójkącie prostokątnym o przyprostokątnych $6$ i $8$ sinus kąta leżącego naprzeciwko boku o długości $6$ wynosi:", {"A": "$\\frac{3}{5}$", "B": "$\\frac{4}{5}$", "C": "$\\frac{3}{4}$", "D": "$\\frac{4}{3}$"}, "A", 2, "Przeciwprostokątna wynosi $\\sqrt{6^2 + 8^2} = 10$. Zatem $\\sin \\alpha = 6/10 = 3/5$."),
        ("Ile jest wszystkich liczb naturalnych dwucyfrowych o różnych cyfrach?", {"A": "$81$", "B": "$90$", "C": "$72$", "D": "$80$"}, "A", 3, "Pierwszą cyfrę wybieramy na 9 sposobów (bez 0), a drugą na 9 sposobów (dowolna z pozostałych cyfr): $9 \\cdot 9 = 81$."),
        ("Rzucamy dwukrotnie symetryczną sześcienną kostką do gry. Prawdopodobieństwo wyrzucenia sumy oczek równej $7$ wynosi:", {"A": "$\\frac{1}{6}$", "B": "$\\frac{5}{36}$", "C": "$\\frac{7}{36}$", "D": "$\\frac{1}{12}$"}, "A", 2, "Wszystkich zdarzeń elementarnych jest 36. Zdarzenia sprzyjające: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) – łącznie 6. $P = 6/36 = 1/6$."),
        ("Wskaż zbiór wartości funkcji $f(x) = x^2 - 4x + 7$:", {"A": "$\\langle 3, +\\infty)$", "B": "$\\langle -3, +\\infty)$", "C": "$\\langle 7, +\\infty)$", "D": "$\\mathbb{R}$"}, "A", 3, "$q = -\\Delta / 4a = -(16 - 28) / 4 = 12 / 4 = 3$. Ramiona w górę, więc $ZW = \\langle 3, +\\infty)$."),
        ("Proste o równaniach $y = 3x - 1$ oraz $y = (a + 1)x + 4$ są prostopadłe, gdy:", {"A": "$a = -\\frac{4}{3}$", "B": "$a = 2$", "C": "$a = -\\frac{1}{3}$", "D": "$a = 3$"}, "A", 3, "$3 \\cdot (a+1) = -1 \\implies a+1 = -1/3 \\implies a = -4/3$."),
    ]

    for idx, (q, opts, ans, diff, expl) in enumerate(sample_definitions):
        topic = topics[idx % len(topics)]
        task = Task.query.filter_by(question=q).first()
        if not task:
            task = Task(
                topic_id=topic.id,
                question=q,
                options=opts,
                correct_answer=ans,
                difficulty=diff,
                explanation=expl,
            )
            db.session.add(task)
            db.session.flush()
        tasks.append(task)

    db.session.commit()
    return tasks


def seed_demo_data(clean: bool = False):
    app = create_app()
    with app.app_context():
        print("=== [1/5] Inicjalizacja struktury bazy, sylabusa i osiągnięć ===")
        seed_all()

        topics = Topic.query.filter(Topic.category_id.isnot(None)).order_by(Topic.id.asc()).limit(15).all()
        if not topics:
            topics = Topic.query.order_by(Topic.id.asc()).limit(10).all()

        print("=== [2/5] Weryfikacja banku zadań egzaminacyjnych i treningowych ===")
        exam_tasks = _ensure_exam_tasks()
        practice_tasks = _ensure_topic_practice_tasks(topics)

        all_achievements = {a.trigger_condition: a for a in Achievement.query.all()}
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        # Czyścimy dotychczasowych użytkowników
        for u in User.query.all():
            db.session.delete(u)
        db.session.commit()

        # Reset autoincrement w SQLite dla czytelnych ID 1-5
        try:
            db.session.execute(db.text("DELETE FROM sqlite_sequence WHERE name IN ('users', 'attempts', 'exam_attempts')"))
            db.session.commit()
        except Exception:
            pass

        print("=== [3/5] Tworzenie kont demonstracyjnych ===")
        _get_or_create_demo_user(
            email='admin@axioma.pl',
            first_name='Administrator',
            password='Admin123!',
            is_admin=True,
            is_active=True,
        )

        anna = _get_or_create_demo_user(
            email='anna.kowalska@axioma.pl',
            first_name='Anna',
            password='Student123!',
            is_admin=False,
            is_active=True,
        )

        jan = _get_or_create_demo_user(
            email='jan.nowak@axioma.pl',
            first_name='Jan',
            password='Student123!',
            is_admin=False,
            is_active=True,
        )

        piotr = _get_or_create_demo_user(
            email='piotr.zielinski@axioma.pl',
            first_name='Piotr',
            password='Student123!',
            is_admin=False,
            is_active=True,
        )

        _get_or_create_demo_user(
            email='kamil.zablokowany@axioma.pl',
            first_name='Kamil',
            password='Student123!',
            is_admin=False,
            is_active=False,
        )
        db.session.commit()

        print("=== [4/5] Generowanie postępów, prób zadań i historii AI dla Anny Kowalskiej (Prymus) ===")
        # Postępy Anny
        for idx, top in enumerate(topics[:8]):
            prog = UserTopicProgress.query.filter_by(user_id=anna.id, topic_id=top.id).first()
            if not prog:
                prog = UserTopicProgress(user_id=anna.id, topic_id=top.id)
                db.session.add(prog)
            prog.current_difficulty = 5 if idx in (0, 1, 4) else (4 if idx in (2, 3) else 3)
            prog.consecutive_correct = 4 if idx in (0, 1) else 2
            prog.consecutive_wrong = 0
            prog.last_activity = now - timedelta(days=idx % 5, hours=idx * 2)

        # Próby z ostatnich 7 dni (pod wykres)
        sample_ai_hints = [
            "Wskazówka dydaktyczna AI: Pamiętaj, że współczynnik kierunkowy $a$ w postaci ogólnej prostej decyduje o jej monotoniczności. Rozwiąż nierówność $a > 0$.",
            "Wskazówka dydaktyczna AI: Zwróć uwagę na znak przy podstawie potęgi oraz kolejność wykonywania działań w ułamku.",
            "Wskazówka dydaktyczna AI: Zastosuj twierdzenie Pitagorasa: $a^2 + b^2 = c^2$. Wyznacz najpierw przeciwprostokątną trójkąta.",
        ]

        existing_anna_attempts = Attempt.query.filter_by(user_id=anna.id).count()
        if existing_anna_attempts < 30:
            for day_offset in range(6, -1, -1):
                day_base = now - timedelta(days=day_offset)
                tasks_today = 5 if day_offset in (0, 1, 2) else 4
                for t_idx in range(tasks_today):
                    target_task = practice_tasks[(day_offset * 3 + t_idx) % len(practice_tasks)]
                    is_err = (day_offset == 3 and t_idx == 1) or (day_offset == 1 and t_idx == 2)
                    chosen_ans = "B" if is_err else target_task.correct_answer
                    hint = random.choice(sample_ai_hints) if is_err else None
                    attempt_time = day_base.replace(hour=10 + t_idx * 2, minute=15 + t_idx * 7)

                    att = Attempt(
                        user_id=anna.id,
                        task_id=target_task.id,
                        user_answer=chosen_ans,
                        is_correct=(not is_err),
                        llm_hint_provided=hint,
                        created_at=attempt_time,
                    )
                    db.session.add(att)

        # Odznaki Anny
        anna_badges = [
            'first_task', 'streak_3', 'daily_goal_5', 'correct_10', 'correct_25',
            'level_3', 'level_4', 'level_5', 'topics_5', 'accuracy_80', 'exam_passed', 'exam_high_80',
        ]
        for badge_code in anna_badges:
            ach = all_achievements.get(badge_code)
            if ach:
                has_badge = UserAchievement.query.filter_by(user_id=anna.id, achievement_id=ach.id).first()
                if not has_badge:
                    db.session.add(UserAchievement(user_id=anna.id, achievement_id=ach.id, unlocked_at=now - timedelta(days=2)))

        # Egzamin Anny (18/20 = 90%)
        existing_exam = ExamAttempt.query.filter_by(user_id=anna.id).first()
        if not existing_exam and len(exam_tasks) >= 20:
            exam_tids = [t.id for t in exam_tasks[:20]]
            exam_answers = {}
            score = 0
            for idx, t in enumerate(exam_tasks[:20]):
                if idx in (7, 14):
                    exam_answers[str(t.id)] = "C" if t.correct_answer != "C" else "B"
                else:
                    exam_answers[str(t.id)] = t.correct_answer
                    score += 1

            exam_start = now - timedelta(days=2, hours=3)
            exam_end = exam_start + timedelta(minutes=28, seconds=45)
            exam_att = ExamAttempt(
                user_id=anna.id,
                title='Próbny Egzamin – Poziom Podstawowy',
                created_at=exam_start,
                completed_at=exam_end,
                score=score,
                total_tasks=20,
                passed=True,
                is_completed=True,
                task_ids=exam_tids,
                answers=exam_answers,
            )
            db.session.add(exam_att)

        print("=== [5/5] Generowanie postępów dla Jana Nowaka (Średni) i Piotra Zielińskiego ===")
        # Postępy Jana
        for idx, top in enumerate(topics[:4]):
            prog = UserTopicProgress.query.filter_by(user_id=jan.id, topic_id=top.id).first()
            if not prog:
                prog = UserTopicProgress(user_id=jan.id, topic_id=top.id)
                db.session.add(prog)
            prog.current_difficulty = 3 if idx == 0 else 2
            prog.consecutive_correct = 1
            prog.last_activity = now - timedelta(days=1, hours=4)

        if Attempt.query.filter_by(user_id=jan.id).count() < 10:
            for i in range(12):
                target_task = practice_tasks[i % len(practice_tasks)]
                is_cor = (i % 3 != 0)
                db.session.add(Attempt(
                    user_id=jan.id,
                    task_id=target_task.id,
                    user_answer=target_task.correct_answer if is_cor else "D",
                    is_correct=is_cor,
                    llm_hint_provided="Wskazówka AI: Spróbuj zapisać równanie pomocnicze." if not is_cor else None,
                    created_at=now - timedelta(days=i // 4, hours=i * 2),
                ))

        for badge_code in ['first_task', 'streak_3']:
            ach = all_achievements.get(badge_code)
            if ach and not UserAchievement.query.filter_by(user_id=jan.id, achievement_id=ach.id).first():
                db.session.add(UserAchievement(user_id=jan.id, achievement_id=ach.id, unlocked_at=now - timedelta(days=3)))

        # Egzamin Jana (50%)
        if not ExamAttempt.query.filter_by(user_id=jan.id).first() and len(exam_tasks) >= 20:
            exam_tids = [t.id for t in exam_tasks[:20]]
            exam_answers = {
                str(t.id): (t.correct_answer if idx < 10 else "D")
                for idx, t in enumerate(exam_tasks[:20])
            }
            db.session.add(ExamAttempt(
                user_id=jan.id,
                title='Próbny Egzamin – Poziom Podstawowy',
                created_at=now - timedelta(days=4),
                completed_at=now - timedelta(days=4) + timedelta(minutes=42),
                score=10,
                total_tasks=20,
                passed=True,
                is_completed=True,
                task_ids=exam_tids,
                answers=exam_answers,
            ))

        # Piotr (początkujący)
        if not UserTopicProgress.query.filter_by(user_id=piotr.id).first():
            db.session.add(UserTopicProgress(user_id=piotr.id, topic_id=topics[0].id, current_difficulty=1, last_activity=now))
            db.session.add(Attempt(
                user_id=piotr.id,
                task_id=practice_tasks[0].id,
                user_answer=practice_tasks[0].correct_answer,
                is_correct=True,
                created_at=now - timedelta(hours=2),
            ))
            first_ach = all_achievements.get('first_task')
            if first_ach:
                db.session.add(UserAchievement(user_id=piotr.id, achievement_id=first_ach.id, unlocked_at=now - timedelta(hours=2)))

        db.session.commit()


if __name__ == '__main__':
    seed_demo_data()
