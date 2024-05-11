from __future__ import annotations

from litestar import Router

from .healthcheck import healthcheck

__all__ = ["router"]

router = Router(path="/api/v0.1.0", route_handlers=[healthcheck])
