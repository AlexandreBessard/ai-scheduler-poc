from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env relative to this file so it works regardless of CWD
_ENV_FILE = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    # override via .env file
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"
    cors_origins: list[str] = ["http://localhost:4200", "http://localhost:4201"]
    database_url: str = "postgresql+asyncpg://scheduler:scheduler@localhost:5433/scheduler"
    env: str = "development"

    model_config = SettingsConfigDict(env_file=_ENV_FILE, env_file_encoding="utf-8")

# (caches) functions results so it does not recompute them every time.
@lru_cache
def get_settings() -> Settings:
    return Settings()
