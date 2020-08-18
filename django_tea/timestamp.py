from typing import Optional
from datetime import datetime, date

from django.utils import timezone


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
HOURS = 60 * 60
MINUTES = 60


# Reuse so I don't need to import django.utils.timezone too
utc = timezone.utc
now = timezone.now
is_aware = timezone.is_aware
is_naive = timezone.is_naive
make_aware = timezone.make_aware
localtime = timezone.localtime


def dt_to_utc_str(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to string."""
    if dt is None:
        return None

    if not is_aware(dt):
        dt = make_aware(dt, timezone=utc)
    return localtime(dt, timezone=utc).strftime(TIMESTAMP_FORMAT)


def date_to_str(d: Optional[date]) -> Optional[str]:
    if d is None:
        return None

    return d.strftime(DATE_FORMAT)


def date_to_dt(d: Optional[date]) -> Optional[datetime]:
    if d is None:
        return None

    return make_aware(datetime.combine(d, datetime.min.time()))


def time_to_local_str(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None

    if not is_aware(dt):
        dt = make_aware(dt, timezone=utc)
    return localtime(dt).strftime(TIME_FORMAT)


def dt_from_utc_str(s: Optional[str]) -> Optional[datetime]:
    """Convert string to timezone aware datetime."""
    if s is None:
        return None
    return make_aware(datetime.strptime(s, TIMESTAMP_FORMAT), timezone=utc)


def humanize(duration: int) -> str:
    """Convert duration in seconds to human readable representation.

    Args:
        duration (int): Duration in seconds.
    """
    hours = duration // HOURS

    result = []
    if hours > 0:
        result.append(f"{hours}h")
        duration = duration - (HOURS * hours)

    minutes = duration // MINUTES
    if minutes > 0 or hours > 0:
        result.append(f"{minutes:02d}m")
        duration = duration - (MINUTES * minutes)

    result.append(f"{duration:02d}s")
    return " ".join(result)
