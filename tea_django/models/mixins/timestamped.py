from django.db import models


class TimestampedMixin(models.Model):
    """Mixin for models with created_on and updated_on fields.

    Fields:
        created_on: DateTime field.
        updated_on: DateTime field.
    """

    created_on = models.DateTimeField(
        auto_now_add=True, blank=False, null=False, editable=False
    )
    updated_on = models.DateTimeField(
        auto_now=True, blank=False, null=False, editable=False
    )

    class Meta:
        app_label = "tea_django"
        abstract = True
