from typing import Optional

from django.db import models


class ColoredMixin(models.Model):
    color = models.CharField(
        max_length=7, default="#000000", null=False, blank=False
    )

    def rich(self, s: Optional[str] = None) -> str:
        """Return a rich markup for the provided string or color hex."""
        return f"[{self.color}]{s or self.color}[/{self.color}]"

    class Meta:
        app_label = "django_tea"
        abstract = True
