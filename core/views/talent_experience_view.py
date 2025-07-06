from rest_framework.decorators import api_view
from rest_framework.response import Response

from core import service_layer
from core.infra.llm import (
    TokenTextSplitter,
    YamlEmbeddingPreprocessor,
    OpenAIHandler,
    PgVectorStoreRetriever,
    YAMLDictOutputParser,
)


@api_view(["POST"])
def get_talent_experiences(request):
    result = service_layer.get_talent_experiences(
        input_data=request.data,
        embedding_preprocessor=YamlEmbeddingPreprocessor(splitter=TokenTextSplitter()),
        retriever=PgVectorStoreRetriever(),
        ai_handler=OpenAIHandler(),
        output_parser=YAMLDictOutputParser(),
    )
    return Response({"message": result})
