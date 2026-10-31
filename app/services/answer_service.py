"""
Deterministyczny Silnik Weryfikacji Odpowiedzi ABCD.
sprawdzanie odpowiedzi ucznia w zadaniach zamkniętych 
Normalizuje warianty usuwa kropki, nawiasy, znaki LaTeX
 Mapuje treść opcji na literę, jeśli model LLM lub formularz zwrócił tekst zamiast litery
Ochrona przed DoS/ReDoS poprzez twardy limit długości ciągów
"""

VALID_CHOICES = frozenset({'A', 'B', 'C', 'D'})


def extract_choice_letter(text: str | None) -> str | None:
    """Ekstrahuje literę wyboru (A, B, C lub D) z tekstu odpowiedzi."""
    if not text:
        return None
    raw = str(text).strip()
    if len(raw) > 250:
        return None
    clean = raw.strip('()[]$. \t\r\n')
    if clean.upper() in VALID_CHOICES:
        return clean.upper()
    return None


def resolve_choice_letter(
    raw_answer: str | None,
    options: dict | None = None,
    fallback: str | None = 'A'
) -> str | None:
    """
    Normalizuje odpowiedź z modelu LLM lub formularza do litery wyboru A, B, C lub D.
    Jeśli model zwrócił treść opcji zamiast litery, mapuje ją względem słownika options.
    """
    letter = extract_choice_letter(raw_answer)
    if letter:
        return letter

    if options and isinstance(options, dict) and raw_answer is not None:
        raw_str = str(raw_answer).strip().lower()
        for opt_key, opt_val in options.items():
            if str(opt_val).strip().lower() == raw_str:
                norm_key = extract_choice_letter(str(opt_key))
                if norm_key:
                    return norm_key

    return fallback


def answers_match(user_answer: str | None, correct_answer: str | None, options: dict | None = None) -> bool:
    """
    Sprawdza poprawność wyboru ucznia w standardzie zadań zamkniętych jednokrotnego wyboru (A, B, C, D).
    Porównuje litery wyboru (case-insensitive) lub treść wybranej opcji ze słownika options.
    """
    if not user_answer or not correct_answer:
        return False

    u_str = str(user_answer).strip()
    c_str = str(correct_answer).strip()
    if len(u_str) > 250 or len(c_str) > 250:
        return False

    # Bezpośrednia równość ciągów (np. 'A' == 'a', '9' == '9')
    if u_str.lower() == c_str.lower():
        return True

    u_choice = extract_choice_letter(u_str)
    c_choice = extract_choice_letter(c_str)

    # Bezpośrednie dopasowanie litery wyboru (np. 'A' == 'a', '(B)' == 'B.')
    if u_choice and c_choice:
        return u_choice == c_choice

    # Obsługa sytuacji, gdy jedna ze stron przekazała treść wariantu ze słownika options
    if options and isinstance(options, dict):
        if not u_choice and c_choice:
            opt_val = str(options.get(c_choice, '')).strip().lower()
            if opt_val and opt_val == u_str.lower():
                return True
        elif u_choice and not c_choice:
            opt_val = str(options.get(u_choice, '')).strip().lower()
            if opt_val and opt_val == c_str.lower():
                return True

    return False
