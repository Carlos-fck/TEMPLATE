try:
    # Prefer the standalone pydantic-settings package (Pydantic v2+)
    from pydantic_settings import BaseSettings  # type: ignore
except Exception:
    # Fallback to the legacy location (pydantic.BaseSettings)
    from pydantic import BaseSettings  # type: ignore

from pydantic import Field


class Settings(BaseSettings):
    env: str = Field("development", env="ENV")
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    celery_broker_url: str = Field("redis://localhost:6379/1", env="CELERY_BROKER_URL")
    secret_key: str = Field("changeme", env="SECRET_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
