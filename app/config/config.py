from __future__ import annotations

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Config", "get_config"]


_CONFIG_CACHE = None


class DatabaseConfig(BaseModel):
    uri: str = "sqlite+aiosqlite:///data/db/app.sqlite3"


class Config(BaseSettings):
    model_config = SettingsConfigDict()
    debug: bool = True
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)


def get_config() -> Config:
    """Get a :class:`Config` instance"""
    global _CONFIG_CACHE
    if not _CONFIG_CACHE:
        _CONFIG_CACHE = Config()
    return _CONFIG_CACHE
