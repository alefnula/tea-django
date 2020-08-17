__all__ = [
    "ColoredMixin",
    "UniqueSlugMixin",
    "NonUniqueSlugMixin",
    "TimerMixin",
    "TimestampedMixin",
]

from django_tea.models.mixins.colored import ColoredMixin
from django_tea.models.mixins.slug import UniqueSlugMixin, NonUniqueSlugMixin
from django_tea.models.mixins.timer import TimerMixin
from django_tea.models.mixins.timestamped import TimestampedMixin
