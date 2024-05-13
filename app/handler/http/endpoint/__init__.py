from __future__ import annotations

from litestar import Router

from .system import SystemController

__all__ = ["router"]

router = Router(path="/api/v0.1.0", route_handlers=[SystemController])
