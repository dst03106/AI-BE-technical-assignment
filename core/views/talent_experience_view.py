from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.service_layer import get_talent_experiences
from core.infra.llm import LLMService


@api_view(["POST"])
def get_talent_experience(request):
    llm_service = LLMService()
    result = get_talent_experiences(request.data, llm_service)
    return Response({"message": result})
