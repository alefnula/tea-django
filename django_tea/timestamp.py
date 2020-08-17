from typing import Optional
from datetime import datetime

from django.utils import timezone


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
HOURS = 60 * 60
MINUTES = 60


def dt_to_utc_str(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to string."""
    if dt is None:
        return None

    if not timezone.is_aware(dt):
        dt = timezone.make_aware(dt, timezone=timezone.utc)
    return timezone.localtime(dt, timezone=timezone.utc).strftime(
        TIMESTAMP_FORMAT
    )


def time_to_local_str(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None

    if not timezone.is_aware(dt):
        dt = timezone.make_aware(dt, timezone=timezone.utc)
    return timezone.localtime(dt).strftime(TIME_FORMAT)


def dt_from_utc_str(s: Optional[str]) -> Optional[datetime]:
    """Convert string to timezone aware datetime."""
    if s is None:
        return None
    return timezone.make_aware(
        datetime.strptime(s, TIMESTAMP_FORMAT), timezone=timezone.utc,
    )


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
