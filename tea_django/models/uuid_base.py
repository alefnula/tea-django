import uuid
from typing import Dict, Any

from django.db import models
from django.utils.functional import classproperty
from tea import timestamp as ts
from tea_console.table import RichTableMixin


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

    @classmethod
    def from_dict(cls, d: dict):
        model_d = {}
        for field in cls._meta.fields:
            if isinstance(field, models.DateTimeField):
                field.auto_now = False
                field.auto_now_add = False
                model_d[field.name] = ts.from_utc_str(d[field.name])
            elif isinstance(field, models.DateField):
                field.auto_now = False
                field.auto_now_add = False
                model_d[field.name] = ts.from_utc_str(d[field.name]).date()
            elif isinstance(field, models.ForeignKey):
                key = f"{field.name}_id"
                model_d[key] = uuid.UUID(d[key])
            else:
                model_d[field.name] = d[field.name]
        return cls(**model_d)

    def __str__(self):
        return f"{self.class_name}({self.id})"

    __repr__ = __str__

    class Meta:
        app_label = "tea_django"
        abstract = True
