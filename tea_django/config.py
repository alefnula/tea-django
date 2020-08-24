import base64
from typing import Dict
from random import SystemRandom

from tea_console.config import ConfigField, Config as ConsoleConfig

from tea_django import consts


def to_value(v: str) -> str:
    return base64.b64decode(v.encode("utf-8")).decode("utf-8")


def to_string(v: str) -> str:
    return base64.b64encode(v.encode("utf-8")).decode("utf-8")


class Config(ConsoleConfig):

    ENTRIES: Dict[str, ConfigField] = {
        **ConsoleConfig.ENTRIES,
        "secret_key": ConfigField(
            section="django",
            option="secret_key",
            to_value=to_value,
            to_string=to_string,
        ),
    }

    def __init__(self, config_file):
        self.secret_key = "".join(
            SystemRandom().choice(consts.SECRETE_KEY_ALLOWED_CHARS)
            for _ in range(50)
        )
        super().__init__(config_file=config_file)
