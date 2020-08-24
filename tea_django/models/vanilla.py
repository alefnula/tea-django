from tea_console.table import RichTableMixin
from django.utils.functional import classproperty


class VanillaModel(RichTableMixin):
    @classproperty
    def class_name(cls):
        return cls.__name__

    def to_dict(self) -> dict:
        return {}
