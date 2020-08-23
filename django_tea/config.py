from typing import Dict
from random import SystemRandom

from console_tea.config import ConfigField, Config as ConsoleConfig

from django_tea import consts
from django_tea import errors


class Config(ConsoleConfig):

    ENTRIES: Dict[str, ConfigField] = {
        **ConsoleConfig.ENTRIES,
        "secret_key": ConfigField(section="general", option="secret_key"),
    }

    def __init__(self, config_file):
        super.__init__(config_file=config_file)
        self.secret_key = "".join(
            SystemRandom().choice(consts.SECRETE_KEY_ALLOWED_CHARS)
            for _ in range(50)
        )

    @classmethod
    def get_application_config(cls) -> "Config":
        subclasses = cls.__subclasses__()
        if len(subclasses) != 1:
            raise errors.InvalidConfiguration(
                "There should be only one subclass of Config."
            )
        return subclasses[0].instance
