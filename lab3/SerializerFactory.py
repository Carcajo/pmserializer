from lab3.constants import JSON, YAML, TOML
from lab3 import Json
from lab3 import Toml
from lab3 import Yaml


class Serializer:

    @staticmethod
    def create_serializer(t):
        if t == JSON:
            return Json

        elif t == YAML:
            return Yaml

        elif t == TOML:
            return Toml

        else:
            raise ValueError
