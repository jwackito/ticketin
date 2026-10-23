from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from the environment.

    ``database_url`` is required: a baked-in default hides misconfiguration and
    works on a host but fails inside a container.
    """

    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    database_url: PostgresDsn


@lru_cache
def get_settings() -> Settings:
    return Settings()
