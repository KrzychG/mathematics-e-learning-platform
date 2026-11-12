# Axioma – Inteligentna Platforma E-Learningowa do Nauki Matematyki

> **Projekt zrealizowany w ramach pracy inżynierskiej dyplomowej**  
> **Kierunek:** Informatyka

---

## 1. Cel i Zakres Pracy Inżynierskiej

Celem projektu inżynierskiego było zaprojektowanie, zaimplementowanie i przetestowanie nowoczesnej, internetowej platformy edukacyjnej wspomagającej naukę matematyki na poziomie szkoły średniej i przygotowanie do egzaminu maturalnego z matematyki na poziomie podstawowym. 

Platforma wykorzystuje **generatywną sztuczną inteligencję (LLM – Google Gemini 3.8 Flash)** do dynamicznego tworzenia spersonalizowanych zadań egzaminacyjnych oraz deterministyczny, zoptymalizowany silnik weryfikacji odpowiedzi oparty na standardzie zadań zamkniętych jednokrotnego wyboru (A, B, C, D).

### Główne obszary funkcjonalne systemu:
- **Format zadań egzaminacyjnych**: generowanie i prezentacja zadań zamkniętych jednokrotnego wyboru (A, B, C, D) z pełnym renderowaniem wzorów matematycznych w formacie $\mathrm{\LaTeX}$ za pośrednictwem biblioteki MathJax 3.
- **Deterministyczny silnik weryfikacji odpowiedzi (ABCD)**: natychmiastowe sprawdzanie wyborów A, B, C, D, normalizacja wariantów, obsługa równoważności numerycznych i pełne zabezpieczenie przed atakami DoS/iniekcjami.
- **Adaptacyjny proces dydaktyczny**: dynamiczne dostosowywanie poziomu trudności (1–5) na podstawie bieżących wyników i serii poprawnych/błędnych odpowiedzi.
- **Kontekstowe wsparcie dydaktyczne (AI Hinting)**: generowanie spersonalizowanych wskazówek do zadań z uwzględnieniem wybranej błędnej odpowiedzi i treści zadania.
- **System grywalizacji (Gamification)**: system osiągnięć, odznak, celów dziennych, statystyk dokładności oraz śledzenia historii prób.
- **Panel administracyjny i CMS**: pełne zarządzanie strukturą programu nauczania (kategorie, tematy, wizualny edytor teorii) oraz zarządzanie kontami i uprawnieniami administratorów.
- **Bezpieczeństwo i uwierzytelnianie**: uwierzytelnianie dwuetapowe (2FA TOTP – RFC 6238) z kodami QR (Google Authenticator, Microsoft Authenticator), ochrona przed atakami powtórzeniowymi (*replay attacks*), ochrona CSRF, sanitizacja HTML (Bleach) oraz granularny *Rate Limiting* (Flask-Limiter).
- **Interaktywny układ współrzędnych i Eksplorator Wykresów (MathGraph Engine)**: zaawansowany, responsywny silnik wektorowy SVG kartezjańskiego układu współrzędnych z dynamiczną siatką, przycinaniem obszaru rysowania (`clipPath`), automatyczną adaptacją do motywu jasnego/ciemnego, interaktywnym celownikiem (*crosshair probe*), wykrywaniem przerw w punktach nieciągłości (bieguny funkcji wymiernych), wyznaczaniem punktów kluczowych (wierzchołek paraboli, miejsca zerowe, punkty przecięcia nakładanych wykresów) oraz bezpiecznym parserem formuł (biblioteka math.js, bez użycia `eval()`). Zintegrowany z zadaniami egzaminacyjnymi (zadania z wykresem) oraz dedykowaną pracownią funkcyjną.
- **Wirtualny brudnopis matematyczny (Scratchpad)**: cyfrowe płótno do odręcznych notatek i szkiców obliczeniowych bezpośrednio w widoku rozwiązywania zadań.
- **Dostępność cyfrowa (WCAG 2.1 / a11y)**: wsparcie dla motywu jasnego/ciemnego, dedykowana czcionka dla dyslektyków (*OpenDyslexic*), dynamiczne skalowanie rozmiaru tekstu oraz tryb redukcji ruchu.

---

## 2. Stos Technologiczny

Projekt został zbudowany w oparciu o sprawdzone, nowoczesne technologie inżynierii oprogramowania:

### Backend & Logika Biznesowa
- **Python 3.13 / 3.12**: główny język programowania logiki serwerowej.
- **Flask (3.1.x)**: lekki, mikro-framework webowy wykorzystujący architekturę *Application Factory* i modularny podział *Flask Blueprints*.
- **Flask-Login (0.6.x)**: kompleksowe zarządzanie sesją użytkowników, autoryzacją i stanem zalogowania (`@login_required`).
- **SQLAlchemy (2.0.x) & Flask-SQLAlchemy**: zaawansowany ORM (Object-Relational Mapping) z optymalizacjami zapytań (*eager loading*, indeksowanie kluczy obcych).
- **Alembic & Flask-Migrate**: wersjonowanie i automatyczna migracja schematów relacyjnej bazy danych.
- **Google Gemini 3.8 Flash API (OpenAI Python SDK)**: bezpośrednia integracja z modelem LLM (Google Gemini 3.8 Flash) do dynamicznej generacji zadań egzaminacyjnych i kontekstowych podpowiedzi dydaktycznych.
- **Markdown (3.11.x)**: silnik parsowania i renderowania artykułów teoretycznych w formacie Extended Markdown z obsługą dedykowanych kontenerów edukacyjnych.
- **Pillow (13.x)**: bezpieczne przetwarzanie, walidacja i optymalizacja grafik awatarów użytkowników.
- **Gunicorn (>=23.x)**: wydajny, wielowątkowy serwer WSGI dla wdrożeń produkcyjnych i kontenerów Docker.

### Frontend & Interfejs Użytkownika
- **HTML5 & Jinja2**: semantyczne szablony z mechanizmem dziedziczenia (`base.html`).
- **Bootstrap 5.3 & Bootstrap Icons**: responsywny interfejs użytkownika (RWD) dostosowany do urządzeń mobilnych i desktopowych.
- **MathJax 3**: renderowanie zapisu matematycznego $\mathrm{\LaTeX}$ bezpośrednio po stronie klienta.
- **math.js**: biblioteka matematyczna do bezpiecznego parsowania, walidacji i ewaluacji formuł funkcyjnych bez użycia `eval()`.
- **MathGraph Engine (SVG & ES6+)**: autorski silnik wektorowy do renderowania funkcji matematycznych z obsługą przycinania SVG (`clipPath`), przerywania krzywej w nieciągłościach (biegunach) oraz wyznaczania punktów charakterystycznych (miejsca zerowe, wierzchołek paraboli, punkty przecięcia).
- **Vanilla JavaScript (ES6+)**: asynchroniczna komunikacja z serwerem (AJAX Fetch API), obsługa motywów i dynamiczne ładowanie zadań AI bez zamrażania widoku.

### Bezpieczeństwo & Walidacja
- **PyOTP & QRCode**: obsługa standardu Time-based One-Time Password (TOTP) i generowanie kodów QR do aplikacji uwierzytelniających (Google Authenticator, Microsoft Authenticator).
- **Flask-WTF & WTForms**: bezpieczne formularze z walidacją typów danych i automatyczną ochroną CSRF.
- **Flask-Limiter**: mechanizm ochrony przed atakami typu Denial of Service (DoS) i brute-force na wrażliwych endpointach.
- **Bleach**: sanityzacja wprowadzanych w CMS treści teoretycznych (ochrona przed atakami XSS - Cross-Site Scripting).
- **Werkzeug Security**: bezpieczne haszowanie haseł użytkowników (algorytm Scrypt/PBKDF2).

### Zapewnienie Jakości (QA) & Testy
- **Pytest (9.x) & pytest-cov**: framework do automatyzacji testów jednostkowych, integracyjnych i badania pokrycia kodu.

---

## 3. Architektura i Struktura Projektu

Aplikacja została zaprojektowana w modularnej architekturze warstwowej:

```text
mathematics-e-learning-platform/
│
├── app/                            # Główny pakiet aplikacji Flask
│   ├── blueprints/                 # Warstwa kontrolerów i tras (Routing)
│   │   ├── admin/                  # Panel CMS, zarządzanie sylabusem i kontami użytkowników (`routes.py`, `content_routes.py`, `user_routes.py`)
│   │   ├── auth/                   # Logowanie, rejestracja, reset hasła, obsługa 2FA TOTP (`routes.py`)
│   │   ├── dashboard/              # Pulpit ucznia, statystyki, historia, ustawienia profilu (`routes.py`, `settings_routes.py`)
│   │   ├── exam/                   # Moduł próbnego egzaminu (arkusz 20 zadań) i podsumowanie (`routes.py`)
│   │   └── learning/               # Pulpit nauki, trening zadań, API AJAX, wykresy funkcji (`routes.py`, `api_routes.py`)
│   │
│   ├── forms/                      # Formularze WTForms z walidatorami danych
│   │   └── auth_forms.py           # Formularze autoryzacji, ustawień konta i panelu administratora
│   │
│   ├── services/                   # Warstwa serwisowa (Czysta logika biznesowa)
│   │   ├── answer_service.py       # Deterministyczny silnik weryfikacji odpowiedzi ABCD
│   │   ├── llm_service.py          # Integracja z Google Gemini API (OpenAI SDK) + fallback offline
│   │   ├── progress_service.py     # Algorytm adaptacji trudności i logika odblokowywania odznak
│   │   ├── sanitizer_service.py    # Oczyszczanie kodu HTML teorii (Bleach) i LaTeX
│   │   ├── theory_renderer_service.py # Parser Extended Markdown i kontenerów dydaktycznych
│   │   ├── timezone_service.py     # Konwersje stref czasowych UTC <-> Europe/Warsaw
│   │   ├── totp_service.py         # Obsługa 2FA TOTP (PyOTP) i ochrona przed powtórzeniem kodu
│   │   └── ...                     # Pozostałe serwisy (achievements_catalog, admin_service, dashboard_service, email_service, history_service, preset_task_service, user_service)
│   │
│   ├── static/                     # Zasoby statyczne (CSS, JS, uploadowane awatary)
│   │   ├── css/                    # Style globalne (main.css), motywy (themes/), komponenty i moduły
│   │   └── js/                     # Skrypty główne (app.js, scratchpad.js) oraz graph/, admin/, core/, dashboard/, exam/, learning/
│   │
│   ├── templates/                  # Szablony widoków Jinja2 (HTML)
│   │   ├── admin/                  # Szablony panelu administracyjnego i CMS
│   │   ├── auth/                   # Widoki logowania, rejestracji i 2FA
│   │   ├── components/             # Reużywalne komponenty (brudnopis, modalne, paginacja)
│   │   ├── dashboard/              # Widoki panelu ucznia, wyników i historii
│   │   ├── emails/                 # Szablony wiadomości e-mail (reset hasła HTML i TXT)
│   │   ├── errors/                 # Dedykowane strony błędów HTTP (403, 404, 429, 500)
│   │   ├── exam/                   # Widoki lobby egzaminu, sesji arkusza i podsumowania
│   │   ├── learning/               # Widok laboratorium teorii, formularz zadań i eksplorator wykresów
│   │   └── base.html               # Główny szkielet aplikacji
│   │
│   ├── __init__.py                 # Fabryka aplikacji (Application Factory Pattern)
│   ├── models.py                   # Relacyjny model danych SQLAlchemy (9 encji)
│   └── utils.py                    # Funkcje narzędziowe (transakcje safe_db_commit, odpowiedzi AJAX/JSON, weryfikacja unikalności)
│
├── content/                        # Materiały dydaktyczne i baza wiedzy
│   ├── syllabus.json               # Struktura 13 kategorii i 77 tematów
│   ├── preset_tasks.json           # Bank predefiniowanych zadań egzaminacyjnych i ćwiczeniowych
│   └── theory/                     # 77 autorskich artykułów Markdown z teorią w 13 kategoriach tematycznych
├── docker/                         # Skrypty startowe i inicjalizacja bazy danych dla kontenera
│   ├── entrypoint.sh               # Uruchomienie inicjalizacji DB i serwera WSGI Gunicorn
│   └── init_db.py                  # Automatyczne tworzenie/migracja schematu i opcjonalny seed
├── instance/                       # Dane lokalne aplikacji (SQLite `app.db`)
├── migrations/                     # Historia migracji schematu bazy danych Alembic
├── tests/                          # Pakiet testów automatycznych (73 testy, 85% pokrycia kodu)
├── .dockerignore                   # Wykluczenia kontekstu budowania obrazu Docker
├── .env.example                    # Wzorzec konfiguracji zmiennych środowiskowych
├── config.py                       # Klasy konfiguracji aplikacji (Development, Testing, Production, Docker)
├── Dockerfile                      # Definicja obrazu kontenera aplikacji (Python 3.13 + Gunicorn)
├── docker-compose.yml              # Orkiestracja kontenera z trwałymi wolumenami danych
├── requirements.txt                # Zależności biblioteczne środowiska Python
├── run.py                          # Punkt wejściowy do uruchomienia serwera deweloperskiego
├── seed.py                         # Seeder bazy danych (kategorie, tematy z teorią Markdown i katalog odznak)
└── seed_demo.py                    # Generator kont demonstracyjnych, historii prób i egzaminów do prezentacji
```

---

## 4. Wymagania Systemowe

- **System operacyjny:** Windows 10/11, Linux (Ubuntu, Debian, Fedora) lub macOS (lub dowolny host z Dockerem).
- **Python:** Wersja `3.11`, `3.12` lub `3.13` (zalecana: `3.13.1`).
- **Menedżer pakietów:** `pip` (zintegrowany z Pythonem).
- **Połączenie sieciowe:** Wymagane do instalacji bibliotek, ładowania zewnętrznych zasobów frontendowych z CDN (Bootstrap, Bootstrap Icons, MathJax 3, Chart.js, czcionka OpenDyslexic) oraz opcjonalnego korzystania z zewnętrznego API Google Gemini. Moduł generowania zadań i wskazówek posiada lokalny tryb awaryjny (*offline fallback*) oparty na banku zadań (`content/preset_tasks.json`), dzięki czemu logika edukacyjna aplikacji działa poprawnie bez klucza API.

---

## 5. Instrukcja Instalacji i Pierwszego Uruchomienia

Poniższe kroki pozwalają na uruchomienie w pełni skonfigurowanego środowiska od zera.

### Krok 1: Sklonowanie repozytorium
```bash
git clone https://github.com/KrzychG/mathematics-e-learning-platform.git
cd mathematics-e-learning-platform
```

### Krok 2: Utworzenie i aktywacja wirtualnego środowiska (`venv`)

- **W systemie Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

- **W systemie Linux / macOS (Bash):**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Krok 3: Instalacja zależności bibliotecznych
Upewnij się, że wirtualne środowisko jest aktywne, a następnie zainstaluj wymagane pakiety:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Krok 4: Konfiguracja zmiennych środowiskowych (`.env`)
Skopiuj wzorcowy plik konfiguracyjny do pliku `.env`:

- **Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
- **Linux / macOS:**
  ```bash
  cp .env.example .env
  ```

Otwórz plik `.env` w edytorze tekstu. Jeśli posiadasz klucz API Google Gemini (Google AI Studio), wprowadź go w polu `GEMINI_API_KEY`. W przeciwnym razie pozostaw wartość przykładową – platforma automatycznie uruchomi lokalny symulator offline.

### Krok 5: Inicjalizacja bazy danych i załadowanie materiałów dydaktycznych
Wykonaj skrypt seedujący, który utworzy brakujące tabele w bazie danych SQLite (`instance/app.db`), zsynchronizuje główne kategorie i tematy matematyczne wraz z treścią artykułów Markdown z katalogu `content/theory/` oraz zainicjalizuje katalog odznak grywalizacji:

```bash
python seed.py
```

> **Wskazówka:** Standardowe polecenie `python seed.py` inicjalizuje samą bazę wiedzy i odznaki (nie tworzy kont użytkowników).

### Krok 6: Zasilenie danymi demonstracyjnymi i konto administratora
Aby zasilić bazę kompletnym zestawem użytkowników demonstracyjnych (Administrator, Uczeń Prymus, Uczeń Średni, Uczeń Początkujący, Uczeń Zablokowany) wraz z bogatą historią prób, egzaminami próbnymi i odznakami pod prezentację projektu, uruchom:

```bash
python seed.py --demo
# lub bezpośrednio:
python seed_demo.py
```

Po wykonaniu seedowania demo dostępne jest prekonfigurowane konto administratora:
- **Adres e-mail:** `admin@axioma.pl`
- **Hasło:** `Admin123!`

Możesz również zarejestrować nowe konto bezpośrednio w formularzu rejestracyjnym (`/register`) i w razie potrzeby nadać mu uprawnienia administratora w panelu (`/admin/users`) lub bezpośrednio w bazie danych.

### Krok 7: Uruchomienie aplikacji
Uruchom serwer deweloperski poleceniem:
```bash
python run.py
```
Aplikacja jest dostępna w przeglądarce pod adresem: **`http://127.0.0.1:5000`**

---

## 6. Opis Zmiennych Środowiskowych (`.env`)

| Zmienna | Wartość domyślna | Opis |
| :--- | :--- | :--- |
| `FLASK_APP` | `run.py` | Plik wejściowy uruchamiający aplikację. |
| `FLASK_DEBUG` | `1` | Tryb debugowania Flask (`1` dla środowiska deweloperskiego, `0` dla produkcji). |
| `FLASK_CONFIG` | `development` | Profil konfiguracji z `config.py` (`development`, `testing`, `production`, `docker`). |
| `SECRET_KEY` | *(ciąg losowy)* | Podstawowy klucz kryptograficzny do podpisywania sesji HTTP i weryfikacji tokenów CSRF. |
| `APP_BASE_URL` | *(pusty)* | Opcjonalny bezwzględny adres bazowy domeny (np. `http://127.0.0.1:5000`), wykorzystywany do generowania pełnych odnośników w e-mailach resetowania hasła. |
| `RATELIMIT_STORAGE_URI` | `memory://` | Magazyn dla mechanizmu limitowania zapytań Flask-Limiter (`memory://` dla środowiska lokalnego/pojedynczego kontenera lub URI do instancji Redis). |
| `DATABASE_URL` | `sqlite:///app.db` | URI połączenia z bazą danych (wspiera SQLite, PostgreSQL, MySQL). |
| `GEMINI_API_KEY` | *(opcjonalny)* | Klucz dostępowy do Google Gemini API (Google AI Studio). W przypadku braku lub wpisania wartości zastępczej, platforma automatycznie przełącza się w lokalny tryb symulacji offline. |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Identyfikator modelu Google Gemini wykorzystywanego do generowania zadań i wskazówek. |
| `USE_PROXY_FIX` | `true` | Aktywacja middleware `werkzeug.middleware.proxy_fix` dla bezpiecznego odczytu nagłówków `X-Forwarded-*` (konfigurowalne przez `PROXY_FIX_X_FOR`, `PROXY_FIX_X_PROTO`, `PROXY_FIX_X_HOST`, `PROXY_FIX_X_PREFIX`, domyślnie `1`). |
| `SESSION_COOKIE_SECURE` | `false` / `true` | Wymuszenie flagi `Secure` dla ciasteczka sesji (w profilu `production` zawsze `true`, w `docker` sterowane zmienną środowiskową, domyślnie `false`). |
| `FORCE_HSTS` | `false` | Wymuszenie polityki bezpieczeństwa HTTP Strict Transport Security (zalecane dla HTTPS na produkcji; w profilu `production` zawsze `true`). |
| `PLATFORM_TIMEZONE` | `Europe/Warsaw` | Docelowa strefa czasowa IANA używana przy konwersji znaczników czasu UTC do czasu lokalnego w interfejsie. |
| `MAIL_SERVER` | *(brak)* | Adres serwera SMTP do wysyłki e-maili resetu hasła (w razie braku linki logowane są w konsoli). |
| `MAIL_PORT` | `587` | Port serwera SMTP (`587` dla STARTTLS, `465` dla SSL). |
| `MAIL_USE_TLS` | `true` | Włączenie szyfrowania STARTTLS przy połączeniu z serwerem SMTP. |
| `MAIL_USE_SSL` | `false` | Włączenie bezpośredniego połączenia SSL/TLS ze serwerem SMTP. |
| `MAIL_USERNAME` | *(brak)* | Nazwa użytkownika (login) konta SMTP. |
| `MAIL_PASSWORD` | *(brak)* | Hasło lub hasło aplikacji (*App Password*) dla konta SMTP. |
| `MAIL_DEFAULT_SENDER` | `no-reply@axioma.pl` | Domyślny adres nadawcy wiadomości e-mail (jeśli brak, używa `MAIL_USERNAME` lub wartości domyślnej). |
| `MAIL_SENDER_NAME` | `Axioma - Platforma Edukacyjna` | Wyświetlana nazwa nadawcy w nagłówku `From`. |
| `MAIL_TIMEOUT` | `10` | Limit czasu połączenia SMTP (w sekundach). |
| `AUTO_SEED` | `auto` | Tryb automatycznej inicjalizacji danych w kontenerze Docker (`auto` – tylko na pustej bazie, `always` – przy każdym starcie, `false` – wyłączony). |
| `APP_PORT` | `5000` | Zewnętrzny port hosta mapowany na port `5000` kontenera w `docker-compose.yml`. |
| `DOCKER_FLASK_CONFIG` | `docker` | Profil konfiguracji przekazywany do kontenera przez `docker-compose.yml`. |

---

## 7. Uruchomienie w Kontenerze Docker (Wariant Minimalny)

Projekt zawiera gotową konfigurację Docker (`Dockerfile`, `docker-compose.yml`, `.dockerignore`, `docker/entrypoint.sh`, `docker/init_db.py`) pozwalającą uruchomić aplikację jednym poleceniem:

```bash
docker compose up --build
```

Po uruchomieniu aplikacja jest dostępna pod adresem: **`http://127.0.0.1:5000`**.

### Najważniejsze cechy konfiguracji Docker:
- **Serwer WSGI:** `gunicorn` uruchamiany w trybie 1 workera i 4 wątków (`--workers 1 --threads 4 --timeout 120`), dzięki czemu limitowanie żądań w pamięci (`memory://`), ochrona przed powtórzeniem kodów 2FA oraz zapis do SQLite (WAL) działają spójnie w ramach jednego procesu.
- **Trwałość danych (Wolumeny):**
  - `axioma_instance` → `/app/instance` (baza `app.db` wraz z plikami WAL/SHM oraz automatycznie wygenerowany klucz `.secret_key`, jeśli `SECRET_KEY` nie podano w `.env`),
  - `axioma_avatars` → `/app/app/static/uploads/avatars` (uploadowane awatary użytkowników).
- **Automatyczna inicjalizacja bazy:** Przy pierwszym starcie na pustym wolumenie `docker/init_db.py` tworzy schemat, oznacza rewizję Alembic (`stamp head`) i jednorazowo ładuje sylabus oraz katalog odznak (`seed.py`). Przy kolejnych restartach nie nadpisuje zmian wprowadzonych w panelu CMS.
- **Healthcheck:** Kontener udostępnia endpoint `/healthz` weryfikujący działanie aplikacji oraz bazy danych.

### Inicjalizacja konta administratora i danych demo w kontenerze:
Przy pierwszym starcie kontener ładuje czystą strukturę programu nauczania. Aby zasilić bazę kontem administratora i danymi demonstracyjnymi w uruchomionym kontenerze, wykonaj polecenie:

```bash
docker compose exec web python seed_demo.py
```

Po załadowaniu danych demonstracyjnych dostępne są dane logowania:
- **E-mail:** `admin@axioma.pl`
- **Hasło:** `Admin123!`

---

## 8. Testy Automatyczne i Weryfikacja Jakości

Projekt posiada zestaw **73 testów automatycznych** (`pytest`) w 100% zakończonych sukcesem (przy całościowym pokryciu kodu aplikacji na poziomie **85%**), obejmujących testy jednostkowe, integracyjne, bezpieczeństwa (CSRF, XSS, 2FA TOTP, rate limiting), spójności bazy danych oraz modułów edukacyjnych i wykresów funkcyjnych.

Aby uruchomić pełny zestaw testów z aktywnego środowiska wirtualnego:

```bash
python -m pytest -v
```

Lub bezpośrednio w systemie Windows (PowerShell):

```powershell
.\venv\Scripts\python.exe -m pytest -v
```

Uruchomienie testów z generowaniem szczegółowego raportu pokrycia kodu:

```powershell
.\venv\Scripts\python.exe -m pytest --cov=app --cov-report=term-missing
```

---
