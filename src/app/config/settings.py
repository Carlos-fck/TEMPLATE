from pydantic import BaseSettings, Field


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
