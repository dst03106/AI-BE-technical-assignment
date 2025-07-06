from typing_extensions import TYPE_CHECKING

from tiktoken import encoding_for_model, get_encoding

from config.settings.env_settings import settings

if TYPE_CHECKING:
    from tiktoken import Encoding


class TokenEncoder:
    _encoder_instance = None
    _model = None

    @classmethod
    def get_token_encoder(cls) -> "Encoding":
        model = settings.llm_model
        if cls._encoder_instance is None or model != cls._model:
            cls._model = model
            cls._encoder_instance = (
                encoding_for_model(cls._model) if "gpt" in cls._model else get_encoding("o200k_base")
            )
        return cls._encoder_instance


class TokenHandler:
    def __init__(self):
        self.encoder = TokenEncoder.get_token_encoder()

    def encode(self, text: str) -> list[int]:
        return self.encoder.encode(text)

    def decode_tokens(self, tokens: list[int]) -> str:
        return self.encoder.decode(tokens)
