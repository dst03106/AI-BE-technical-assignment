from abc import ABC, abstractmethod
from typing import Any


class AbstractLLMService(ABC):
    @abstractmethod
    def chat_completions(self, input_data: Any) -> Any:
        pass
