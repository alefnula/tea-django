from django.db import models
from django.utils import timezone

from django_tea import timestamp as ts


class TimerMixin(models.Model):
    start_time = models.DateTimeField(
        default=ts.now, null=False, blank=True, editable=True
    )
    end_time = models.DateTimeField(
        null=True, blank=True, default=None, editable=True
    )
    duration = models.BigIntegerField(null=False, blank=False, default=0)

    @property
    def running_time(self) -> str:
        end_time = self.end_time or timezone.now()

        return ts.humanize(int((end_time - self.start_time).total_seconds()))

    def start(self):
        self.start_time = timezone.now()
        self.end_time = None
        self.duration = 0

    def stop(self):
        self.end_time = timezone.now()

    def save(self, *args, **kwargs):
        if self.end_time is not None:
            self.duration = int(
                (self.end_time - self.start_time).total_seconds()
            )
        super().save(*args, **kwargs)

    class Meta:
        app_label = "django_tea"
        abstract = True
