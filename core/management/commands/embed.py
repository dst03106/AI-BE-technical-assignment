from django.core.management.base import BaseCommand

from core.service_layer.services import embed_companies
from core.infra.llm import (
    TokenTextSplitter,
    YamlEmbeddingPreprocessor,
    PgVectorStore,
    OpenAIHandler,
)
from core.models.company import Company


class Command(BaseCommand):
    help = "데이터를 벡터 임베딩하여 저장합니다."

    def handle(self, *_args, **_options):
        embed_companies(
            companies=Company.objects.all(),
            embedding_preprocessor=YamlEmbeddingPreprocessor(splitter=TokenTextSplitter()),
            ai_handler=OpenAIHandler(),
            vector_store=PgVectorStore(),
        )
