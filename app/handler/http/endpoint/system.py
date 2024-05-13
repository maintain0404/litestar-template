from __future__ import annotations

from litestar import Controller, get
from litestar.di import Provide

from app.service.system.schema import SystemHealth
from app.service.system.service import SystemService


class SystemController(Controller):
    path = "/system"
    dependencies = {"system_service": Provide(SystemService, sync_to_thread=False)}

    @get("/health")
    async def full_healthcheck(self, system_service: SystemService) -> SystemHealth:
        return await system_service.healthcheck()
