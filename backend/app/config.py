import os
from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "Photophinder"
    api_prefix: str = "/"
    database_url: str = Field(
        default="postgresql+psycopg2://photophinder:photophinder@db:5432/photophinder",
        env="DATABASE_URL",
    )

    storage_endpoint: str = Field(default="http://minio:9000", env="STORAGE_ENDPOINT")
    storage_bucket: str = Field(default="photophinder", env="STORAGE_BUCKET")
    storage_access_key: str = Field(default="minioadmin", env="STORAGE_ACCESS_KEY")
    storage_secret_key: str = Field(default="minioadmin", env="STORAGE_SECRET_KEY")
    storage_use_ssl: bool = Field(default=False, env="STORAGE_USE_SSL")

    celery_broker_url: str = Field(default="redis://redis:6379/0", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://redis:6379/1", env="CELERY_RESULT_BACKEND")

    embeddings_dimension: int = Field(default=512, env="EMBEDDINGS_DIMENSION")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
