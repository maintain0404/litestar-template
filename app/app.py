from __future__ import annotations

from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    EngineConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

from app.config import Config, config
from app.handler.http import router


def create_sqla_plugin(config: Config) -> SQLAlchemyInitPlugin:
    return SQLAlchemyInitPlugin(
        config=SQLAlchemyAsyncConfig(
            connection_string=config.db.uri,
            session_config=AsyncSessionConfig(autobegin=False, expire_on_commit=False),
            engine_config=EngineConfig(echo=config.debug),
        )
    )


def create_app(config: Config, *plugin_builders) -> Litestar:
    return Litestar(
        debug=config.debug,
        route_handlers=[router],
        plugins=[plugin_builder(config) for plugin_builder in plugin_builders],
    )


app = create_app(config, create_sqla_plugin)
