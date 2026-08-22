"""
Obsługa uwierzytelniania dwuetapowego (2FA / TOTP) z wykorzystaniem biblioteki PyOTP.
"""
import time
import threading
import pyotp

# Słownik w pamięci do ochrony przed atakiem powtórzeniowym (replay attack).
# Zapamiętujemy użyte kody na czas okna ważności tokena (120 sekund).
_used_tokens_lock = threading.Lock()
_USED_LOGIN_TOKENS: dict[tuple[int, str], float] = {}
TOTP_REPLAY_WINDOW_SECONDS = 120


def clean_totp_token(token: str | None) -> str:
    """Usuwa zbędne spacje i białe znaki z wprowadzonego kodu 2FA."""
    return (token or "").strip().replace(" ", "")


def verify_totp_code(secret: str, token: str | None, *, valid_window: int = 1) -> tuple[bool, str]:
    """
    Weryfikuje wprowadzony przez użytkownika kod 6-cyfrowy względem sekretu Base32.
    valid_window=1 pozwala na akceptację kodu z poprzedniego i następnego 30-sekundowego okna
    w przypadku minimalnych rozbieżności czasu na urządzeniu użytkownika.
    """
    cleaned = clean_totp_token(token)
    if not secret or not cleaned:
        return False, cleaned
    try:
        totp = pyotp.TOTP(secret)
        is_valid = bool(totp.verify(cleaned, valid_window=valid_window))
        return is_valid, cleaned
    except Exception:
        return False, cleaned


def is_totp_replayed(user_id: int, token: str) -> bool:
    """Sprawdza, czy dany kod nie został już zużyty w bieżącym oknie czasowym."""
    now = time.time()
    clean_token = clean_totp_token(token)
    global _USED_LOGIN_TOKENS
    with _used_tokens_lock:
        # Usuwamy przedawnione tokeny starsze niż okno ważności
        _USED_LOGIN_TOKENS = {
            k: ts for k, ts in _USED_LOGIN_TOKENS.items()
            if now - ts <= TOTP_REPLAY_WINDOW_SECONDS
        }
        return (user_id, clean_token) in _USED_LOGIN_TOKENS


def record_totp_used(user_id: int, token: str) -> None:
    """Zapisuje kod jako wykorzystany, aby uniemożliwić ponowne logowanie tym samym kodem."""
    now = time.time()
    with _used_tokens_lock:
        _USED_LOGIN_TOKENS[(user_id, clean_totp_token(token))] = now

