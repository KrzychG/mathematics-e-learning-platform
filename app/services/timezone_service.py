import os
from datetime import date, datetime, timezone, timedelta

PLATFORM_TIMEZONE_NAME = os.environ.get('PLATFORM_TIMEZONE', 'Europe/Warsaw')

_ZONE_INFO = None
try:
    from zoneinfo import ZoneInfo
    _ZONE_INFO = ZoneInfo(PLATFORM_TIMEZONE_NAME)
except Exception:
    _ZONE_INFO = None
def _warsaw_fallback_dst_bounds_utc(year: int) -> tuple[datetime, datetime]:
    # granice czasu letniego w Polsce (gdy brak tzdata)
    mar_31 = datetime(year, 3, 31, 1, 0, tzinfo=timezone.utc)
    start_dst = mar_31 - timedelta(days=(mar_31.weekday() + 1) % 7)
    oct_31 = datetime(year, 10, 31, 1, 0, tzinfo=timezone.utc)
    end_dst = oct_31 - timedelta(days=(oct_31.weekday() + 1) % 7)
    return start_dst, end_dst


def ensure_utc(dt: datetime | None) -> datetime:
    if not dt:
        return datetime.min.replace(tzinfo=timezone.utc)
    if getattr(dt, 'tzinfo', None) is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_naive_utc(dt: datetime | None) -> datetime:
    return ensure_utc(dt).replace(tzinfo=None)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _resolve_warsaw_utc_offset_hours(ref_utc: datetime) -> int:
    start_dst, end_dst = _warsaw_fallback_dst_bounds_utc(ref_utc.year)
    return 2 if (start_dst <= ref_utc < end_dst) else 1


def to_local_time(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    dt_utc = ensure_utc(dt)
    if _ZONE_INFO is not None:
        return dt_utc.astimezone(_ZONE_INFO)
    offset_hours = _resolve_warsaw_utc_offset_hours(dt_utc)
    return dt_utc.astimezone(timezone(timedelta(hours=offset_hours)))


def local_date_to_utc_midnight(local_day: date) -> datetime:
    # Przelicza lokalną północ (Warszawa) na znacznik UTC naive pod filtrowanie w bazie danych:
    # Działa stabilnie również na Windowsie w razie braku systemowego pakietu tzdata
    if _ZONE_INFO is not None:
        local_dt = datetime(local_day.year, local_day.month, local_day.day, tzinfo=_ZONE_INFO)
        return local_dt.astimezone(timezone.utc).replace(tzinfo=None)
    naive_midnight = datetime(local_day.year, local_day.month, local_day.day, tzinfo=timezone.utc)
    offset_hours = _resolve_warsaw_utc_offset_hours(naive_midnight)
    return (naive_midnight - timedelta(hours=offset_hours)).replace(tzinfo=None)


def parse_local_date_range_to_utc(
    date_from_str: str | None,
    date_to_str: str | None,
) -> tuple[datetime | None, datetime | None]:
    # Konwertuje zakres dat z filtrów CMS (czas warszawski) na przedział UTC [start, end_exclusive):
    # Do date_to dodajemy 1 dzień, dzięki czemu zapytanie 'created_at < end_utc_exclusive' obejmuje cały wskazany dzień.
    start_utc = None
    end_utc_exclusive = None
    if date_from_str:
        try:
            start_day = date.fromisoformat(date_from_str.strip())
            start_utc = local_date_to_utc_midnight(start_day)
        except ValueError:
            start_utc = None
    if date_to_str:
        try:
            end_day = date.fromisoformat(date_to_str.strip())
            end_utc_exclusive = local_date_to_utc_midnight(end_day + timedelta(days=1))
        except ValueError:
            end_utc_exclusive = None
    return start_utc, end_utc_exclusive


def get_local_now() -> datetime:
    return to_local_time(utc_now())


def get_today_start_utc() -> datetime:
    # Początek dnia w UTC (naive pod zapytania SQL)
    return local_date_to_utc_midnight(get_local_now().date())
TIME_FORMAT_TEMPLATES = {
    'datetime': '{year}-{month}-{day} {time}',
    'time-date': '{time}, {day}.{month}.{year}',
    'date-time': '{day}.{month}.{year}, {time}',
    'date-only': '{day}.{month}.{year}',
}

# Domyślne formaty wyświetlania daty i czasu
LOCAL_DATETIME_FORMATS = {
    'datetime': '%Y-%m-%d %H:%M',
    'time-date': '%H:%M, %d.%m.%Y',
    'date-time': '%d.%m.%Y, %H:%M',
    'date-only': '%d.%m.%Y',
}

def format_duration_seconds(seconds: int | None) -> str:
    secs = max(0, int(seconds or 0))
    mins, remaining = divmod(secs, 60)
    return f"{mins} min {remaining} s" if mins > 0 else f"{remaining} s"


def format_local_datetime(dt: datetime | None, fmt: str = 'datetime') -> str:
    if not dt:
        return '-'
    local_dt = to_local_time(dt)
    resolved_fmt = LOCAL_DATETIME_FORMATS.get(fmt, fmt)
    return local_dt.strftime(resolved_fmt)


def format_activity_time(dt: datetime | None) -> str:
    if not dt:
        return "Brak daty"
    dt_local = to_local_time(dt)
    now_local = get_local_now()
    today = now_local.date()
    yesterday = today - timedelta(days=1)
    time_str = dt_local.strftime('%H:%M')
    if dt_local.date() == today:
        return f"Dzisiaj, {time_str}"
    elif dt_local.date() == yesterday:
        return f"Wczoraj, {time_str}"
    else:
        days_ago = (today - dt_local.date()).days
        if 0 < days_ago < 7:
            return f"{days_ago} dni temu, {time_str}"
        return dt_local.strftime('%d.%m.%Y, %H:%M')


def to_utc_iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return ensure_utc(dt).strftime('%Y-%m-%dT%H:%M:%SZ')
