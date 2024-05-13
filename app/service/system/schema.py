from __future__ import annotations

from app.core.schema import BaseSchema


class SystemHealth(BaseSchema):
    is_database_online: bool
