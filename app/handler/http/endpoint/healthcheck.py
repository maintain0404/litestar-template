from __future__ import annotations

from typing import Literal

from litestar import get

from app.core.schema import BaseSchema


class HealthcheckSchema(BaseSchema):
    status: Literal["ok"] = "ok"


@get("/health")
async def healthcheck() -> HealthcheckSchema:
    return HealthcheckSchema()
