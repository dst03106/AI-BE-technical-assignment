from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    llm_model: str
    llm_api_key: str
    embedding_model: str
    embedding_model_dim: int

    # DB
    postgres_host: str = "localhost"
    postgres_user: str = "searchright"
    postgres_password: str = "searchright"
    postgres_port: int = 5432
    postgres_database: str = "searchright"
    postgres_uri: str = (
        f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_database}"
    )

    class Config:
        env_file = ".env"


settings = Settings()
