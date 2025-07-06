from typing import TYPE_CHECKING

from config.settings.prompt_settings import settings
from core.infra.llm.vector_store import Embedding
from core.infra.llm.prompt_template import PromptTemplate

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from core.infra.llm.ai_handler import BaseAIHandler
    from core.infra.llm.vector_store import BaseVectorStore
    from core.infra.llm.embedding_preprocesser import BaseEmbeddingPreprocessor
    from core.infra.llm.retriever import BaseVectorRetriever
    from core.infra.llm.output_parser import BaseOutputParser
    from core.models import Company


def get_talent_experiences(
    input_data: dict,
    embedding_preprocessor: "BaseEmbeddingPreprocessor",
    retriever: "BaseVectorRetriever",
    ai_handler: "BaseAIHandler",
    output_parser: "BaseOutputParser",
):
    user_prompt_variable = {"talent": input_data, "retrieved_docs": []}
    prompt_template = PromptTemplate(settings.talent_experience_prompt)

    text_chunks = embedding_preprocessor.preprocess(input_data)
    for text_chunk in text_chunks:
        embedding_vector = ai_handler.get_embedding(text_chunk)
        retrieved_docs = retriever.retrieve_documents_by_vector_similarity(embedding_vector)
        user_prompt_variable["retrieved_docs"] += retrieved_docs

    messages = prompt_template.format(user_prompt_variable)
    prediction = ai_handler.chat_completions(messages)
    result = output_parser.parse(prediction)
    return result


def embed_companies(
    companies: "QuerySet['Company']",
    embedding_preprocessor: "BaseEmbeddingPreprocessor",
    ai_handler: "BaseAIHandler",
    vector_store: "BaseVectorStore",
):
    embeddings = []
    for company in companies:
        data = company.data | {"company_news": list(company.company_news.values("title", "news_date"))}
        text_chunks = embedding_preprocessor.preprocess(data)
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
