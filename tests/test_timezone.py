from datetime import datetime, timezone, timedelta
from app.services.timezone_service import (
    to_local_time,
    get_local_now,
    get_today_start_utc,
    format_local_datetime,
    to_utc_iso,
)


def test_to_local_time():
    assert to_local_time(None) is None
    # Czas zimowy (UTC+1)
    w = to_local_time(datetime(2026, 11, 2, 12, 30, tzinfo=timezone.utc))
    assert w.hour == 13
    assert w.minute == 30
    assert w.utcoffset() == timedelta(hours=1)

    # Czas letni (UTC+2)
    s = to_local_time(datetime(2026, 7, 15, 12, 30, tzinfo=timezone.utc))
    assert s.hour == 14
    assert s.minute == 30
    assert s.utcoffset() == timedelta(hours=2)


def test_timezone_utilities():
    now_local = get_local_now()
    assert now_local.tzinfo is not None
    assert now_local.utcoffset() in (timedelta(hours=1), timedelta(hours=2))

    today_start = get_today_start_utc()
    assert today_start.tzinfo is None

    assert format_local_datetime(None) == '-'
    dt_utc = datetime(2026, 11, 2, 10, 5, tzinfo=timezone.utc)
    assert format_local_datetime(dt_utc) == '2026-11-02 11:05'
    assert format_local_datetime(dt_utc, '%H:%M') == '11:05'

    assert to_utc_iso(None) is None
    assert to_utc_iso(datetime(2026, 11, 2, 10, 30)) == '2026-11-02T10:30:00Z'
    assert to_utc_iso(datetime(2026, 11, 2, 11, 30, tzinfo=timezone(timedelta(hours=1)))) == '2026-11-02T10:30:00Z'
