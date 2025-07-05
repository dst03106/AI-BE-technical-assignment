import openai

from .llm_service_port import AbstractLLMService


API_KEY = ""
client = openai.OpenAI(api_key=API_KEY)


class LLMService(AbstractLLMService):
    def chat_completions(self, talent_data: dict) -> dict:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # 사용할 모델명
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hi"},
                ],
            )
            # 응답받은 메시지를 반환
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"
