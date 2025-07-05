from core.infra.llm.llm_service_adapter import AbstractLLMService

from .dto import TalentInfo


def get_talent_experiences(talent_info: TalentInfo, llm_service: AbstractLLMService) -> list[str]:
    return llm_service.chat_completions(talent_info)
