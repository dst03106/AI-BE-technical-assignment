import re
import yaml
from abc import ABC, abstractmethod
from typing import Any, Callable


class PostprocessStep:
    def __init__(self, input_key: str, output_key: str, func: Callable[[Any], Any]):
        self.input_key = input_key
        self.output_key = output_key
        self.func = func

    def run(self, data: list[dict]) -> dict:
        processed = []
        for item in data:
            if self.input_key not in item:
                raise KeyError(f"Missing key: {self.input_key} in {item}")
            new_item = item.copy()
            new_item[self.output_key] = self.func(item[self.input_key])
            processed.append(new_item)
        return processed


class BaseOutputParser(ABC):
    def __init__(self, postprocess_steps: list[PostprocessStep] = None):
        self.postprocess_steps = postprocess_steps or []

    def run_postprocesses(self, text: Any) -> dict:
        data = self._parse(text)
        for step in self.postprocess_steps:
            data = step.run(data)
        return data

    @abstractmethod
    def _parse(self, text: Any) -> dict:
        pass


class YAMLDictOutputParser(BaseOutputParser):
    def _parse(self, text: str) -> dict | None:
        match = re.search(r"```yaml\n(.*?)```", text, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
