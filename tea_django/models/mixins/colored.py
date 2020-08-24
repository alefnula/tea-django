from typing import Optional

from django.db import models
from django.forms.widgets import TextInput
from django.core.validators import RegexValidator
from django.utils.html import mark_safe, SafeString
from django.utils.translation import gettext_lazy as _

from tea_django.consts import COLOR_RE


color_validator = RegexValidator(
    COLOR_RE, _("Enter a valid color."), "invalid color"
)


class ColorField(models.CharField):
    default_validators = [color_validator]

    def __init__(self, *args, **kwargs):
        # It should always be 7
        kwargs["max_length"] = 7
        kwargs.setdefault("default", "#FFFFFF")
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = TextInput(attrs={"type": "color"})
        return super(ColorField, self).formfield(**kwargs)


class ColoredMixin(models.Model):
    color = ColorField(null=False, blank=False)

    def rich(self, s: Optional[str] = None) -> str:
        """Return a rich colored markup for the provided string."""
        return f"[{self.color}]{s or self.color}[/{self.color}]"

    def html(self, s: str) -> SafeString:
        """Return a django safe string in current color."""
        return mark_safe(f'<span style="color: {self.color}">{s}</span>')

    class Meta:
        app_label = "tea_django"
        abstract = True
