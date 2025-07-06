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

    def chat_completions(self, input_data: dict) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hi"},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"

    def get_embedding(self, input_text):
        response = self.client.embeddings.create(
            model=settings.embedding_model,
            input=input_text,
        )
        return response.data[0].embedding
