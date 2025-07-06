from abc import ABC, abstractmethod
from typing import Any

import openai

from config.settings.env_settings import settings


class BaseAIHandler(ABC):
    @abstractmethod
    def chat_completions(self, input_data: Any) -> Any:
        pass

    @abstractmethod
    def get_embedding(self, input_text: str):
        pass


class OpenAIHandler(BaseAIHandler):
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.llm_api_key)

    # TODO : 비동기로 변환
    def chat_completions(self, messages: list[dict[str, str]]) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
            )
            return response.choices[0].message.content
        except openai.RateLimitError as e:
            print(f"Rate limit error during LLM inference: {e}")
            raise
        except openai.APIError as e:
            print(f"Error during LLM inference: {e}")
            raise
        except Exception as e:
            print(f"Unknown error during LLM inference: {e}")
            raise openai.APIError from e

    def get_embedding(self, input_text):
        response = self.client.embeddings.create(
            model=settings.embedding_model,
            input=input_text,
        )
        return response.data[0].embedding
