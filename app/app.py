from __future__ import annotations

from click import Group
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    EngineConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from litestar.plugins import CLIPluginProtocol

from app.config import Config, config
from app.handler.http import router


class ApplicationPlugin(CLIPluginProtocol):
    def on_cli_init(self, cli: Group) -> None:
        from app.handler.cmd.system import healthcheck

        cli.add_command(healthcheck)


def create_sqla_config(config: Config) -> SQLAlchemyAsyncConfig:
    return SQLAlchemyAsyncConfig(
        connection_string=config.db.uri,
        session_config=AsyncSessionConfig(expire_on_commit=False),
        engine_config=EngineConfig(echo=config.debug),
    )


def create_app(config: Config) -> Litestar:
    return Litestar(
        debug=config.debug,
        route_handlers=[router],
        plugins=[
            SQLAlchemyInitPlugin(config=create_sqla_config(config)),
            ApplicationPlugin(),
        ],
    )


app = create_app(config)
