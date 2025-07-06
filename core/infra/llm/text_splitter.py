from typing import Callable
from abc import ABC, abstractmethod

from core.infra.llm.token_handler import TokenHandler


class BaseTextSplitter(ABC):
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 64,
        length_function: Callable[[str], int] | None = None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function or (lambda x: len(x))

    @abstractmethod
    def split_text(self, text: str) -> list[str]:
        """텍스트를 청크 리스트로 분리"""
        pass


class TokenTextSplitter(BaseTextSplitter):
    def __init__(self, token_handler: TokenHandler | None = None, **kwargs):
        super().__init__(**kwargs)
        self.token_handler = token_handler or TokenHandler()

    def split_text(self, text):
        tokens = self.token_handler.encode(text)
        text_list = []

        start = 0
        while start < self.length_function(tokens):
            end = start + self.chunk_size
            chunk = tokens[start:end]
            decoded = self.token_handler.decode_tokens(chunk)
            text_list.append(decoded)
            start += self.chunk_size - self.chunk_overlap
        return text_list
