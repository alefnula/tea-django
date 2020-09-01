from django.db import models
from tea import timestamp as ts


class TimerMixin(models.Model):
    start_time = models.DateTimeField(
        default=ts.now, null=False, blank=True, editable=True
    )
    end_time = models.DateTimeField(
        null=True, blank=True, default=None, editable=True
    )
    duration = models.BigIntegerField(null=False, blank=False, default=0)

    @property
    def running_duration(self) -> int:
        """Return the running duration in seconds.

        This will return result even if the song hasn't finsihed.
        """
        end_time = self.end_time or ts.now()
        return int((end_time - self.start_time).total_seconds())

    @property
    def running_time(self) -> str:
        return ts.humanize(self.running_duration)

    def start(self):
        self.start_time = ts.now()
        self.end_time = None
        self.duration = 0

    def stop(self):
        self.end_time = ts.now()

    def save(self, *args, **kwargs):
        if self.end_time is not None:
            self.duration = self.running_duration
        super().save(*args, **kwargs)

    class Meta:
        app_label = "tea_django"
        abstract = True
