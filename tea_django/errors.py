__all__ = [
    "DjangoTeaError",
    "InvalidConfiguration",
    "DatabaseError",
    "ObjectAlreadyExists",
    "ObjectNotFound",
    "MultipleObjectsFound",
]

from typing import Type, Optional
from tea_console.errors import ConsoleTeaError, InvalidConfiguration


class DjangoTeaError(ConsoleTeaError):
    pass


def query_to_string(query: Optional[dict]) -> str:
    if query is None or len(query) == 0:
        return ""
    else:
        return (
            "("
            + ", ".join(f"{key}={value}" for key, value in query.items())
            + ")"
        )


class DatabaseError(DjangoTeaError):
    pass


class ObjectAlreadyExists(DatabaseError):
    def __init__(self, model: Type, query: Optional[dict] = None):
        self.model = model
        self.query = query

        super().__init__(
            message=(
                f"{model.class_name}{query_to_string(self.query)} "
                f"already exists."
            )
        )


class ObjectNotFound(DatabaseError):
    def __init__(self, model: Type, query: Optional[dict] = None):
        """ObjectNotFound error.

        Args:
            model: Model class.
            query: Query dictionary.
        """
        self.model = model
        self.query = query

        super().__init__(
            message=(
                f"{model.class_name}{query_to_string(self.query)} not found."
            )
        )


class MultipleObjectsFound(DatabaseError):
    def __init__(self, model: Type, query: Optional[dict] = None):
        """MultipleObjectsFound error.

        Args:
            model: Model class.
            query: Query dictionary.
        """
        self.model = model
        self.query = query

        super().__init__(
            message=(
                f"{model.class_name}{query_to_string(self.query)} "
                f"multiple objects found."
            )
        )
