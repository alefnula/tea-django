import json
import uuid
from typing import Type

from django.db import models
from django_tea import timestamp as ts


class DjangoTeaEncoder(json.JSONEncoder):
    """Django Tea JSON Encoder.

    It knows how to serialize:

        1. All objects that have a custom `to_dict` method
        2. Decimal numbers
        3. DateTime and Date objects
        4. UUIDs
    """

    to_float = frozenset(("decimal.Decimal",))
    to_datetime = frozenset(("datetime.datetime", "datetime.date"))
    to_list = frozenset(
        (
            "__builtin__.set",
            "builtins.set",
            "builtins.dict_keys",
            "builtins.dict_values",
        )
    )
    to_str = frozenset(("uuid.UUID",))

    def default(self, o):
        try:
            return super(DjangoTeaEncoder, self).default(o)
        except TypeError:
            # First see if there is a __json__ method
            if hasattr(o, "to_dict"):
                return o.to_dict()
            # Then try out special classes
            cls = o.__class__
            path = "%s.%s" % (cls.__module__, cls.__name__)
            if path in self.to_float:
                return float(o)
            elif path in self.to_datetime:
                return ts.dt_to_utc_str(o)
            elif path in self.to_list:
                return list(o)
            elif path in self.to_str:
                return str(o)
            raise TypeError("%s is not JSON serializable" % o)


def json_dumps(obj, indent=4) -> str:
    """Wrap `json.dumps` using the `TraktorEncoder`."""
    return json.dumps(
        obj,
        cls=DjangoTeaEncoder,
        ensure_ascii=False,
        allow_nan=False,
        indent=indent,
        separators=(",", ":"),
    )


def json_dict_to_model(model: Type[models.Model], d: dict) -> models.Model:
    model_d = {}
    for field in model._meta.fields:
        if isinstance(field, models.DateTimeField):
            model_d[field.name] = ts.dt_from_utc_str(d[field.name])
        elif isinstance(field, models.DateField):
            model_d[field.name] = ts.dt_from_utc_str(d[field.name]).date()
        elif isinstance(field, models.ForeignKey):
            key = f"{field.name}_id"
            model_d[key] = uuid.UUID(d[key])
        else:
            model_d[field.name] = d[field.name]
    return model(**model_d)
