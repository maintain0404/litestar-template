from __future__ import annotations

from click import command
from rich import get_console

from app.app import create_sqla_config
from app.config.config import config
from app.service.system.service import SystemService


@command
def healthcheck():
    """Check if system is healthy."""

    async def inner():
        async with create_sqla_config(config).get_session() as session:
            svc = SystemService(session)
            result = await svc.healthcheck()

        console = get_console()
        console.print_json(result.model_dump_json())

    import anyio

    anyio.run(inner)
