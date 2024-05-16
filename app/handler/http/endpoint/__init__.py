from __future__ import annotations

from litestar import Router

from .auth import router as oidc_router
from .system import SystemController

__all__ = ["router"]

router = Router(path="/api/v0.1.0", route_handlers=[SystemController, oidc_router])
