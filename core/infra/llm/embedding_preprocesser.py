from typing import Any, TYPE_CHECKING

from abc import ABC, abstractmethod

import yaml


if TYPE_CHECKING:
    from .text_splitter import BaseTextSplitter


class BaseEmbeddingPreprocessor(ABC):
    def __init__(self, splitter: "BaseTextSplitter"):
        self.splitter = splitter

    @abstractmethod
    def to_text(self, data: Any) -> str:
        """dict → 문자열 변환"""
        pass

    def preprocess(self, data: Any) -> list[str]:
        """변환된 문자열을 splitter를 사용해 청크 리스트로 분할"""
        return self.splitter.split_text(self.to_text(data))


class YamlEmbeddingPreprocessor(BaseEmbeddingPreprocessor):
    def to_text(self, data: Any) -> str:
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
