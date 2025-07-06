from typing import TYPE_CHECKING

from core.infra.llm.vector_store import Embedding


if TYPE_CHECKING:
    from django.db.models import QuerySet

    from core.infra.llm.ai_handler import BaseAIHandler
    from core.infra.llm.vector_store import BaseVectorStore
    from core.infra.llm.embedding_preprocesser import BaseEmbeddingPreprocessor
    from core.models import Company


def embed_companies(
    companies: "QuerySet['Company']",
    embedding_preprocessor: "BaseEmbeddingPreprocessor",
    ai_handler: "BaseAIHandler",
    vector_store: "BaseVectorStore",
):
    embeddings = []
    for company in companies:
        text_chunks = embedding_preprocessor.preprocess(company.data)
        for text_chunk in text_chunks:  # TODO: asyncio.gather을 통해 병렬 요청 필요
            embedding_vector = ai_handler.get_embedding(text_chunk)
            embeddings.append(
                Embedding(
                    content=text_chunk,
                    embedding_vector=embedding_vector,
                    source_type=company._meta.db_table,
                    source_id=company.id,
                )
            )
    vector_store.add_embeddings(embeddings)
