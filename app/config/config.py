from __future__ import annotations

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Config"]


class DatabaseConfig(BaseModel):
    uri: str = "sqlite+aiosqlite:///data/db/app.sqlite3"


class Config(BaseSettings):
    model_config = SettingsConfigDict()
    debug: bool = True
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
