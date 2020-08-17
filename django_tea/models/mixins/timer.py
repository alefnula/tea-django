from django.db import models
from django.utils import timezone

from django_tea import timestamp as ts


class TimerMixin(models.Model):
    start_time = models.DateTimeField(
        auto_now_add=True, null=False, blank=False
    )
    end_time = models.DateTimeField(null=True, blank=True, default=None)
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
        self.duration = int((self.end_time - self.start_time).total_seconds())

    class Meta:
        app_label = "django_tea"
        abstract = True
