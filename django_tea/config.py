import io
import os
from dataclasses import dataclass
from configparser import ConfigParser
from typing import List, Dict, Type, Optional, Callable, Any


from django_tea.table import Column, RichTableMixin


@dataclass
class ConfigField:
    section: str
    option: str
    type: Type = str
    to_value: Optional[Callable[[Any], Any]] = None
    to_string: Optional[Callable[[Any], str]] = None


@dataclass()
class ConfigEntry(RichTableMixin):
    HEADERS = [
        Column(title="Key", path="key"),
        Column(title="Value", path="value"),
    ]
    key: str
    value: Any


class Config:
    ENTRIES: Dict[str, ConfigField] = {}

    def __init__(self, config_file):
        self._config_file = config_file

    @property
    def entries(self) -> List[ConfigEntry]:
        return [
            ConfigEntry(key=field, value=getattr(self, field))
            for field in self.ENTRIES
        ]

    def set(self, field, value):
        if field not in self.ENTRIES:
            raise ValueError(f"Invalid configuration key: {field}")

        entry = self.ENTRIES[field]
        if entry.type == bool:
            if value.lower() in ("true", "false", "on", "off"):
                value = value.lower() in ("true", "on")
            else:
                raise ValueError(f"Invalid boolean value: {value}")
        elif entry.type == int:
            value = int(value, 10)
        elif entry.type == float:
            value = float(value)

        if entry.to_value:
            value = entry.to_value(value)

        setattr(self, field, value)

    def load(self):
        """Load configuration."""
        if not os.path.isfile(self._config_file):
            return

        cp = ConfigParser()
        cp.read(self._config_file)

        for field, entry in self.ENTRIES.items():
            try:
                if cp.has_option(entry.section, entry.option):
                    self.set(field, cp.get(entry.section, entry.option))
            except Exception as e:
                raise ValueError(
                    f"Failed to load: {entry.section}.{entry.option}. "
                    f"Error: {e}"
                )

    def save(self):
        # Create if it doesn't exist
        os.makedirs(os.path.dirname(self._config_file), exist_ok=True)
        cp = ConfigParser()
        # If it already exists read the values
        if os.path.isfile(self._config_file):
            cp.read(self._config_file)

        for field, entry in self.ENTRIES.items():
            if not cp.has_section(entry.section):
                cp.add_section(entry.section)

            value = getattr(self, field)
            value = (
                entry.to_string(value)
                if entry.to_string is not None
                else str(value)
            )

            cp.set(entry.section, entry.option, value)

        with io.open(self._config_file, "w") as f:
            cp.write(f)
