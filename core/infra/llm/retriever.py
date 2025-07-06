from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.infra.llm import PgVectorStore

if TYPE_CHECKING:
    from core.infra.llm.vector_store import BaseVectorStore


class BaseVectorRetriever(ABC):
    """벡터 검색 기반 Retriever의 기본 클래스"""

    def __init__(
        self,
        vector_store: "BaseVectorStore",
        top_k: int = 5,
        *_args,
        **_kwargs,
    ):
        super().__init__(*_args, **_kwargs)
        self.vector_store = vector_store
        self.tok_k = top_k

    @abstractmethod
    def retrieve_documents_by_vector_similarity(
        self, query_vector: list[float], k: int = None
    ) -> list[tuple[int, float]]:
        """쿼리 벡터와 유사한 상위 k개의 문서를 반환합니다."""
        pass


class PgVectorStoreRetriever(BaseVectorRetriever):
    def __init__(
        self,
        # score_threshold: Optional[float] = None,
        **kwargs,
    ):
        super().__init__(vector_store=PgVectorStore(), **kwargs)

    def retrieve_documents_by_vector_similarity(
        self, query_vector: list[float], k: int = None
    ) -> list[tuple[int, float]]:
        top_k = k if k is not None else self.k
        results = self.vector_store.search_similar(query_vector, top_k=top_k)
        # [{'content': str}, ...] 형태로 데이터가 전달됨
        return results
