from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.settings.env_settings import settings as env_settings
from core import service_layer
from core.infra.llm import (
    TokenTextSplitter,
    YamlEmbeddingPreprocessor,
    OpenAIHandler,
    PgVectorStoreRetriever,
    YAMLDictOutputParser,
    SemanticNormalizer,
    PostprocessStep,
)


@api_view(["POST"])
def get_talent_experiences(request):
    result = service_layer.get_talent_experiences(
        input_data=request.data,
        embedding_preprocessor=YamlEmbeddingPreprocessor(splitter=TokenTextSplitter()),
        retriever=PgVectorStoreRetriever(),
        ai_handler=OpenAIHandler(),
        output_parser=YAMLDictOutputParser(
            postprocess_steps=[
                PostprocessStep(
                    input_key="attribute",
                    output_key="attribute",
                    func=SemanticNormalizer(
                        standard_values=env_settings.experience_standard_values,
                        alias_mapping=env_settings.experience_alias_mapping,
                    ).normalize,
                )
            ]
        ),
    )
    return Response({"message": result})
