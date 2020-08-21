import uuid
from typing import Dict, Any

from django.db import models
from django.utils.functional import classproperty

from django_tea.table import RichTableMixin


class UUIDBaseModel(models.Model, RichTableMixin):
    """Base model with UUID as a primary key."""

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    @classproperty
    def class_name(cls):
        return cls.__name__

    def column_dict(self) -> Dict[str, Any]:
        d = {}
        for field in self._meta.fields:
            if isinstance(field, models.ForeignKey):
                name = f"{field.name}_id"
            else:
                name = field.name
            d[name] = getattr(self, name)
        return d

    def to_dict(self):
        return self.column_dict()

    def __str__(self):
        return f"{self.class_name}({self.id})"

    __repr__ = __str__

    class Meta:
        app_label = "django_tea"
        abstract = True
