from typing import Dict
from random import SystemRandom

from console_tea.config import ConfigField, Config as ConsoleConfig

from django_tea import consts


class Config(ConsoleConfig):

    ENTRIES: Dict[str, ConfigField] = {
        **ConsoleConfig.ENTRIES,
        "secret_key": ConfigField(section="django", option="secret_key"),
    }

    def __init__(self, config_file):
        self.secret_key = "".join(
            SystemRandom().choice(consts.SECRETE_KEY_ALLOWED_CHARS)
            for _ in range(50)
        )
        super().__init__(config_file=config_file)
