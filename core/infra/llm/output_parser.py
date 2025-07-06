import re
import yaml
from abc import ABC, abstractmethod


class BaseOutputParser(ABC):
    @abstractmethod
    def parse(self, text: str) -> dict:
        pass


class YAMLDictOutputParser(BaseOutputParser):
    def parse(self, text: str) -> dict | None:
        match = re.search(r"```yaml\n(.*?)```", text, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
