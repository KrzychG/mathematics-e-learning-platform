import re
import json
import time
import random
import difflib
import logging
from openai import OpenAI
from flask import current_app
from config import Config
from app import db
from app.models import Task, Topic
from app.services.answer_service import resolve_choice_letter
from app.services.preset_task_service import (
    create_unique_exam_tasks,
    get_practice_fallback_bank,
    get_or_create_exam_topic,
    normalize_question_key,
)

logger = logging.getLogger(__name__)


def are_tasks_too_similar(q1: str | None, q2: str | None, threshold: float = 0.70) -> bool:
    # Wykrywanie duplikatów difflibem – próg 0.70 skutecznie wyłapuje sytuacje,
    # w których model sklonował treść zadania, zmieniając tylko pojedynczą liczbę.
    if not q1 or not q2:
        return False
    return difflib.SequenceMatcher(None, q1.strip().lower(), q2.strip().lower()).ratio() >= threshold


def _get_configured_model() -> str:
    if current_app:
        return current_app.config.get('GEMINI_MODEL') or Config.GEMINI_MODEL
    return Config.GEMINI_MODEL


_PLACEHOLDER_FRAGMENTS = ('klucz-api', 'przyklad', 'your-api-key', 'sk-xxx', 'gsk-xxx', 'aiza-xxx', 'twoj_klucz')


def _is_placeholder_key(key: str | None) -> bool:
    if not key:
        return True
    key_clean = key.strip()
    if not key_clean or len(key_clean) < 10:
        return True
    key_lower = key_clean.lower()
    return any(fragment in key_lower for fragment in _PLACEHOLDER_FRAGMENTS)


def get_ai_client():
    # Pobiera klienta OpenAI spiętego z endpointem Gemini REST API.
    # Jeśli klucza brak w środowisku lub został domyślny placeholder z .env.example,
    # zwracamy None i cały system transparentnie przełącza się na lokalny bank zadań.
    model = _get_configured_model()
    gemini_key = current_app.config.get('GEMINI_API_KEY') if current_app else None
    if gemini_key and not _is_placeholder_key(gemini_key):
        clean_key = gemini_key.strip()
        client = OpenAI(
            api_key=clean_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            default_headers={"x-goog-api-key": clean_key}
        )
        return client, model
    return None, model


def build_default_topic_system_prompt(topic_name: str) -> str:
    return (
        f"Jesteś nauczycielem matematyki przygotowującym zadania egzaminacyjne z tematu: '{topic_name}'.\n"
        "Twoim celem jest tworzenie unikalnych zadań jednokrotnego wyboru (A, B, C, D). "
        "Dbaj o różnorodność danych liczbowych i szukanych wielkości. "
        "Nie powtarzaj schematów ani tych samych danych w kolejnych zadaniach.\n\n"
        "Zwróć odpowiedź WYŁĄCZNIE jako obiekt JSON o strukturze:\n"
        "{\n"
        '  "task_content": "treść zadania z formułami LaTeX ($...$ w tekście, $$...$$ w wyodrębnionych liniach)",\n'
        '  "options": {"A": "...", "B": "...", "C": "...", "D": "..."},\n'
        '  "correct_answer": "litera A, B, C lub D",\n'
        '  "explanation": "zwięzłe rozwiązanie krok po kroku"\n'
        "}"
    )


def _get_fallback_tasks_for_level(difficulty_level: int) -> list[dict]:
    bank = get_practice_fallback_bank()
    tasks_for_level = bank.get(difficulty_level, bank.get(1, []))
    if not tasks_for_level and bank:
        tasks_for_level = list(bank.values())[0]
    return tasks_for_level


def _build_fallback_task_dict(item: dict) -> dict:
    return {
        "task_content": item["question"],
        "options": item["options"],
        "correct_answer": item["correct_answer"],
        "explanation": item.get("explanation"),
    }


def _simulate_math_task(difficulty_level: int) -> dict:
    tasks_for_level = _get_fallback_tasks_for_level(difficulty_level)
    return _build_fallback_task_dict(random.choice(tasks_for_level))


_OPTION_PREFIX_RE = re.compile(r'^[A-D][\)\.]\s*')


def _strip_option_prefix(value) -> str:
    return _OPTION_PREFIX_RE.sub('', str(value).strip())


def _normalize_llm_options(raw_options) -> dict[str, str]:
    letters = ('A', 'B', 'C', 'D')
    if isinstance(raw_options, str):
        try:
            raw_options = json.loads(raw_options)
        except Exception:
            return {}
    cleaned = {}
    if isinstance(raw_options, dict):
        for let in letters:
            val = raw_options.get(let) or raw_options.get(let.lower(), '')
            if val is not None:
                cleaned[let] = _strip_option_prefix(val)
    elif isinstance(raw_options, list) and len(raw_options) >= 4:
        for i, opt in enumerate(raw_options[:4]):
            let = letters[i]
            val = next(iter(opt.values()), '') if isinstance(opt, dict) else opt
            cleaned[let] = _strip_option_prefix(val)
    return cleaned


def normalize_correct_answer(raw_answer: str | None, options: dict | None = None) -> str:
    return resolve_choice_letter(raw_answer, options=options, fallback='A') or 'A'


def safe_parse_json(content: str) -> dict:
    if not content:
        return {}
    cleaned = content.strip()
    if cleaned.startswith('```'):
        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'\s*```$', '', cleaned, flags=re.MULTILINE)
        cleaned = cleaned.strip()
    try:
        return json.loads(cleaned, strict=False)
    except Exception:
        fixed = re.sub(r'\\(?![/u"bfnrt\\])', r'\\\\', cleaned)
        return json.loads(fixed, strict=False)
def _load_topic_tasks_by_key(topic_id: int) -> dict[str, Task]:
    existing_by_key: dict[str, Task] = {}
    for task in Task.query.filter_by(topic_id=topic_id).order_by(Task.id.asc()).all():
        q_key = normalize_question_key(task.question)
        if q_key:
            existing_by_key.setdefault(q_key, task)
    return existing_by_key


def _pick_fallback_math_task(
    topic_id: int,
    difficulty_level: int,
    existing_by_key: dict[str, Task] | None = None,
    recent_questions: list[str] | None = None,
) -> dict:
    if existing_by_key is not None:
        used_keys = set(existing_by_key.keys())
    else:
        used_keys = {
            normalize_question_key(q)
            for (q,) in db.session.query(Task.question).filter_by(topic_id=topic_id).all()
            if q
        }
    first_candidate = _simulate_math_task(difficulty_level)
    cand_q = first_candidate.get('task_content', '')
    is_cand_used = normalize_question_key(cand_q) in used_keys
    is_cand_similar = bool(recent_questions and any(are_tasks_too_similar(cand_q, rq) for rq in recent_questions))
    if not is_cand_used and not is_cand_similar:
        return first_candidate
    tasks_for_level = _get_fallback_tasks_for_level(difficulty_level)
    unused = [
        item for item in tasks_for_level
        if normalize_question_key(item.get('question')) not in used_keys
        and not (recent_questions and any(are_tasks_too_similar(item.get('question'), rq) for rq in recent_questions))
    ]
    if unused:
        return _build_fallback_task_dict(random.choice(unused))
    dissimilar = [
        item for item in tasks_for_level
        if not (recent_questions and any(are_tasks_too_similar(item.get('question'), rq) for rq in recent_questions))
    ]
    if dissimilar:
        return _build_fallback_task_dict(random.choice(dissimilar))
    return first_candidate


def _request_json_completion(
    client,
    configured_model: str | None,
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float = 0.7,
    timeout: float = 35.0,
    reasoning_effort: str | None = None,
) -> dict:
    kwargs = {
        "model": configured_model or _get_configured_model(),
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "timeout": timeout,
    }
    if reasoning_effort is not None:
        kwargs["reasoning_effort"] = reasoning_effort
    response = client.chat.completions.create(**kwargs)
    return safe_parse_json(response.choices[0].message.content)


def generate_math_task(
    topic_id: int,
    difficulty_level: int = 1,
    exclude_task_id: int | None = None,
) -> dict:
    # Generator pojedynczego zadania do modułu nauki:
    # Pobieramy do 8 ostatnich zadań z tego tematu i wrzucamy w prompt
    # Jeśli model wygeneruje zadanie zbyt podobne, robimy jedno ponowienie z ostrzeżeniem.
    # Przy braku klucza AI od razu sięgamy do lokalnego banku zadań.
    # Sprawdzamy 4 warianty odpowiedzi, wyznaczamy poprawną literę i zapisujemy nowe zadanie w bazie.
    topic = db.session.get(Topic, topic_id)
    topic_name = topic.name if topic else 'Matematyka'
    system_message = build_default_topic_system_prompt(topic_name)
    topic_context_parts = []
    if topic and topic.category:
        topic_context_parts.append(f"Dział: {topic.category.name}.")
    if topic and topic.description:
        topic_context_parts.append(f"Zakres materiału: {topic.description}")
    topic_context = (" " + " ".join(topic_context_parts)) if topic_context_parts else ""
    client, configured_model = get_ai_client()
    existing_by_key = None

    # Ostatnie zadania tematu pod kątem deduplikacji i unikania klonów
    recent_tasks = Task.query.filter_by(topic_id=topic_id).order_by(Task.id.desc()).limit(8).all()
    recent_questions: list[str] = []
    if exclude_task_id:
        ex_task = db.session.get(Task, exclude_task_id)
        if ex_task and ex_task.question:
            eq = ex_task.question.strip()
            if eq:
                recent_questions.append(eq)
    for rt in recent_tasks:
        rq = (rt.question or '').strip()
        if rq and not any(are_tasks_too_similar(rq, existing) for existing in recent_questions):
            recent_questions.append(rq)

    try:
        if client:
            user_prompt = f"Wygeneruj zadanie wielokrotnego wyboru (A, B, C, D). Poziom trudności: {difficulty_level}/5.{topic_context}"
            if recent_questions:
                history_text = "\n".join(f"- {q}" for q in recent_questions[:3])
                user_prompt += (
                    f"\n\nPoprzednie zadania z tego tematu (NIE powielaj ich treści):\n"
                    f"{history_text}\n"
                    f"Twoje nowe zadanie MUSI być inne: użyj innych danych liczbowych i zapytaj o inną wielkość."
                )

            task_data = _request_json_completion(
                client,
                configured_model,
                system_message,
                user_prompt,
                temperature=0.85,
                timeout=35.0,
                reasoning_effort="low",
            )
            candidate_q = task_data.get('task_content', '')
            # Jeśli AI wygenerowało klona, ponawiamy raz z mocniejszym upomnieniem
            if recent_questions and any(are_tasks_too_similar(candidate_q, rq) for rq in recent_questions):
                retry_user_prompt = (
                    f"Zadanie '{candidate_q[:80]}...' jest niemal identyczne z poprzednim zadaniem z tego tematu. "
                    f"Wygeneruj ZUPEŁNIE INNE zadanie na poziomie {difficulty_level}/5 z tematu '{topic_name}': "
                    f"użyj innych liczb i innej szukanej wielkości."
                )
                try:
                    retry_data = _request_json_completion(
                        client,
                        configured_model,
                        system_message,
                        retry_user_prompt,
                        temperature=0.9,
                        timeout=35.0,
                        reasoning_effort="low",
                    )
                    if retry_data and retry_data.get('task_content'):
                        task_data = retry_data
                except Exception as retry_err:
                    logger.warning("Błąd ponowienia generowania zadania AI: %s", retry_err)
        else:
            time.sleep(0.4)
            existing_by_key = _load_topic_tasks_by_key(topic_id)
            task_data = _pick_fallback_math_task(
                topic_id,
                difficulty_level,
                existing_by_key=existing_by_key,
                recent_questions=recent_questions,
            )
        task_question = task_data.get('task_content', 'Błąd generowania treści')
        cleaned_options = _normalize_llm_options(task_data.get('options'))
        correct_answer = normalize_correct_answer(task_data.get('correct_answer'), cleaned_options)
        explanation = (task_data.get('explanation') or '').strip() or None
        q_key = normalize_question_key(task_question)
        if not client and q_key and existing_by_key is not None:
            existing_task = existing_by_key.get(q_key)
            if existing_task:
                if explanation and not existing_task.explanation:
                    existing_task.explanation = explanation
                    db.session.commit()
                return existing_task.to_view_dict()
        new_task = Task(
            topic_id=topic_id,
            question=task_question,
            options=cleaned_options,
            correct_answer=correct_answer,
            difficulty=difficulty_level,
            explanation=explanation,
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task.to_view_dict()
    except Exception as e:
        db.session.rollback()
        logger.error("Błąd podczas generowania zadania: %s", e)
        raise
def generate_hint(task_content: str, correct_answer: str, user_answer: str, options: dict | None = None) -> str:
    # Generowanie spersonalizowanej podpowiedzi dydaktycznej:
    # Model analizuje prawdopodobną przyczynę
    # pomyłki ucznia
    # W trybie offline zwracamy czytelny szablon wyjaśniający rozbieżność.
    client, configured_model = get_ai_client()
    options_context = ""
    if options:
        options_context = "\nDostępne warianty:\n" + "\n".join([f"{k}: {v}" for k, v in options.items()])
    clean_user_answer = (user_answer or '').strip()[:200]
    clean_task_content = (task_content or '').strip()[:1000]
    system_prompt = (
        "Jesteś nauczycielem matematyki. Uczeń rozwiązał zadanie niepoprawnie. "
        "Twoim celem jest jasne wyjaśnienie: dlaczego poprawna odpowiedź jest właściwa "
        "oraz dlaczego wybór ucznia był błędny (jaki błąd rachunkowy, koncepcyjny lub znakowy został prawdopodobnie popełniony). "
        "Wyjaśnij rozwiązanie zwięźle, przystępnie i krok po kroku. Możesz używać składni LaTeX (np. $x^2$, $\\frac{a}{b}$). "
        "Zwróć poprawny JSON z jednym kluczem: 'hint' (po polsku)."
    )
    user_prompt = (
        f"Treść zadania: {clean_task_content}\n{options_context}\n"
        f"Poprawna odpowiedź: {correct_answer}\n"
        f"Odpowiedź ucznia: {clean_user_answer}\n"
        "Wyjaśnij zwięźle i precyzyjnie: dlaczego poprawna odpowiedź jest właściwa i dlaczego wybór ucznia był błędny."
    )
    try:
        if client:
            hint_data = _request_json_completion(
                client,
                configured_model,
                system_prompt,
                user_prompt,
                temperature=0.5,
                timeout=35.0,
                reasoning_effort="low",
            )
            return hint_data.get('hint', 'Sprawdź ponownie swoje obliczenia krok po kroku.')
        else:
            time.sleep(0.3)
            correct_val = options.get(correct_answer, correct_answer) if options else correct_answer
            user_val = options.get(user_answer, user_answer) if options else user_answer
            if options and (correct_answer in options or user_answer in options):
                return (
                    f"Prawidłowa odpowiedź to **{correct_answer}** ({correct_val}). "
                    f"Twój wybór **{user_answer}** ({user_val}) wynika najczęściej z pomyłki w znakach (+/-), "
                    f"błędnego przekształcenia algebraicznego lub pominięcia kolejności działań. "
                    f"Rozwiąż zadanie krok po kroku, stosując odpowiednie definicje i wzory."
                )
            return (
                f"Prawidłowy wynik to **{correct_answer}**, a Twoja odpowiedź to **{user_answer}**. "
                f"Różnica wynika z błędu rachunkowego lub pomyłki w przekształceniach wzoru. "
                f"Sprawdź dokładnie każdy krok swoich obliczeń oraz kolejność operacji."
            )
    except Exception as e:
        logger.error("Błąd generatora wskazówek: %s", e)
        correct_val = options.get(correct_answer, correct_answer) if options else correct_answer
        return (
            f"Prawidłowa odpowiedź to {correct_val}. "
            f"Sprawdź dokładnie kolejność wykonywania działań oraz znaki w przekształceniach."
        )
def generate_exam_tasks(required_count: int = 20) -> list[Task] | None:
    # Generowanie pełnego arkusza egzaminu maturalnego
    # W jednym wywołaniu model układa 20 unikalnych zadań pokrywających przekrój podstawy
    # Następnie przepuszczamy je przez create_unique_exam_tasks w celu eliminacji duplikatów.
    client, configured_model = get_ai_client()
    if not client:
        return None
    prompt = (
        f"Jesteś doświadczonym autorem arkuszy egzaminacyjnych z matematyki na poziomie podstawowym (Formuła 2023).\n"
        f"Twoim zadaniem jest wygenerowanie kompletnego arkusza egzaminacyjnego składającego się z dokładnie {required_count} unikalnych, "
        f"różnorodnych zadań zamkniętych jednokrotnego wyboru (A, B, C, D) w formacie JSON.\n\n"
        f"Zadania muszą pokrywać szeroki przekrój wymagań egzaminacyjnych:\n"
        f"1. Liczby rzeczywiste, potęgi o wykładnikach całkowitych i wymiernych, pierwiastki\n"
        f"2. Logarytmy i ich własności\n"
        f"3. Procenty, punkty procentowe i zadania tekstowe\n"
        f"4. Wzory skróconego mnożenia i wyrażenia algebraiczne\n"
        f"5. Równania liniowe i kwadratowe, równania iloczynowe\n"
        f"6. Nierówności liniowe i kwadratowe, przedziały liczbowe\n"
        f"7. Wartość bezwzględna i proste nierówności z modułem\n"
        f"8. Własności funkcji, dziedzina i zbiór wartości\n"
        f"9. Funkcja liniowa (współczynnik kierunkowy, prostopadłość/równoległość prostych)\n"
        f"10. Funkcja kwadratowa (postać ogólna, kanoniczna, iloczynowa, wierzchołek paraboli)\n"
        f"11. Ciąg arytmetyczny (wzór ogólny, suma początkowych wyrazów)\n"
        f"12. Ciąg geometryczny (iloraz, wzór ogólny)\n"
        f"13. Trygonometria (wartości funkcji kąta ostrego, tożsamości trygonometryczne)\n"
        f"14. Planimetria: trójkąty, twierdzenie Pitagorasa, kąty w okręgu\n"
        f"15. Planimetria: czworokąty, pola i obwody figur płaskich\n"
        f"16. Geometria analityczna (długość i środek odcinka, równanie prostej i okręgu)\n"
        f"17. Stereometria: graniastosłupy i ostrosłupy (objętość i pole powierzchni)\n"
        f"18. Elementy kombinatoryki (reguła mnożenia, proste permutacje/kombinacje)\n"
        f"19. Klasyczny rachunek prawdopodobieństwa (rzut kostką, losowanie kul)\n"
        f"20. Statystyka (średnia arytmetyczna, mediana, dominanta)\n\n"
        f"Wymogi formalne:\n"
        f"- Wzory i symbole matematyczne wplecione w treść zdania formatuj w zwięzłym LaTeXu z pojedynczymi dolarami: $...$ (np. $a_n$, $n \\ge 1$, $r$, $x^2$). Podwójne dolary $$...$$ stosuj wyłącznie dla dużych, samodzielnych równań.\n"
        f"- W formacie JSON pamiętaj o poprawnym znakowaniu ukośników LaTeX (\\\\frac, \\\\sqrt).\n"
        f"- Dokładnie 4 warianty odpowiedzi dla każdego zadania: A, B, C, D.\n"
        f"- Dokładnie jedna poprawna odpowiedź (wskazana jako 'A', 'B', 'C' lub 'D').\n\n"
        f"Zwróć odpowiedź WYŁĄCZNIE jako obiekt JSON o strukturze:\n"
        f"{{\n"
        f'  "tasks": [\n'
        f"    {{\n"
        f'      "question": "treść zadania z formułami LaTeX $$...$$",\n'
        f'      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},\n'
        f'      "correct_answer": "A",\n'
        f'      "difficulty": 2\n'
        f"    }}\n"
        f"  ]\n"
        f"}}"
    )
    try:
        data = _request_json_completion(
            client,
            configured_model,
            prompt,
            f"Wygeneruj pełny zestaw {required_count} zadań egzaminacyjnych.",
            temperature=0.7,
            timeout=60.0,
        )
        tasks_raw = data.get('tasks', [])
        if not tasks_raw or len(tasks_raw) < 5:
            raise ValueError(f"AI zwróciło zbyt mało zadań: {len(tasks_raw)}")
        exam_topic = get_or_create_exam_topic()
        def _normalize_llm_exam_item(item: dict) -> dict | None:
            cleaned_opts = _normalize_llm_options(item.get('options', {}))
            if len(cleaned_opts) < 4 or any(not v for v in cleaned_opts.values()):
                return None
            return {
                'options': cleaned_opts,
                'correct_answer': normalize_correct_answer(item.get('correct_answer'), cleaned_opts),
                'difficulty': item.get('difficulty', 2),
            }
        created_tasks = create_unique_exam_tasks(
            tasks_raw,
            topic_id=exam_topic.id,
            max_count=required_count,
            item_normalizer=_normalize_llm_exam_item,
        )
        db.session.commit()
        return created_tasks
    except Exception as e:
        db.session.rollback()
        logger.error("Błąd podczas generowania arkusza egzaminacyjnego przez AI: %s", e)
        return None
