from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_model: str
    # db_url: str
    # debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
