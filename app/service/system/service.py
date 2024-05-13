from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import SystemHealth


@dataclass
class SystemService:
    db_session: AsyncSession

    async def healthcheck(self) -> SystemHealth:
        try:
            await self.db_session.execute(text("select 1"))
        except ConnectionRefusedError:
            database = False
        else:
            database = True

        return SystemHealth(is_database_online=database)
