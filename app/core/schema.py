from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict as SchemaConfig
from pydantic import Field as field

__all__ = [
    "BaseModel",
    "field",
]


class BaseSchema(BaseModel):
    model_config = SchemaConfig(extra="ignore", from_attributes=True)
