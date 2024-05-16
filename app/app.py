from __future__ import annotations

import logging

import structlog
from click import Group
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from litestar.logging import LoggingConfig, StructLoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.plugins import CLIPluginProtocol
from litestar.plugins.structlog import StructlogConfig, StructlogPlugin

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
    )


def create_structlog_config(config: Config) -> StructlogConfig:
    request_log_fields = ["method", "path", "path_params", "query"]
    response_log_fields = ["status_code"]

    structlog_logging_config = StructLoggingConfig(
        log_exceptions="always",
        traceback_line_limit=4,
        standard_lib_logging_config=LoggingConfig(
            root={
                "level": logging.getLevelName(logging.INFO),
                "handlers": ["queue_listener"],
            },
            formatters={
                "standard": {  # override
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.dev.ConsoleRenderer(colors=True),
                    ],
                    "foreign_pre_chain": [
                        # Add the log level and a timestamp to the event_dict
                        # if the log entry is not from structlog.
                        structlog.stdlib.add_log_level,
                        structlog.stdlib.add_logger_name,
                        # Add extra attributes of LogRecord objects to the event dict
                        # so that values passed in the extra parameter of log methods
                        # pass through to log output.
                        structlog.stdlib.ExtraAdder(
                            response_log_fields + response_log_fields
                        ),
                        structlog.processors.TimeStamper(fmt="iso"),
                    ],
                }
            },
            loggers={
                "uvicorn.access": {
                    "propagate": False,
                    "level": logging.INFO,
                    "handlers": ["queue_listener"],
                },
                "uvicorn.error": {
                    "propagate": False,
                    "level": logging.INFO,
                    "handlers": ["queue_listener"],
                },
                "sqlalchemy.engine": {
                    "propagate": False,
                    "level": logging.INFO,
                    "handlers": ["queue_listener"],
                },
                "sqlalchemy.pool": {
                    "propagate": False,
                    "level": logging.INFO,
                    "handlers": ["queue_listener"],
                },
            },
        ),
    )
    middleware_logging_config = LoggingMiddlewareConfig(
        request_log_fields=request_log_fields,
        response_log_fields=response_log_fields,
    )
    return StructlogConfig(
        structlog_logging_config=structlog_logging_config,
        middleware_logging_config=middleware_logging_config,
    )


def create_app(config: Config) -> Litestar:
    return Litestar(
        debug=config.debug,
        route_handlers=[router],
        plugins=[
            SQLAlchemyInitPlugin(config=create_sqla_config(config)),
            StructlogPlugin(config=create_structlog_config(config)),
            ApplicationPlugin(),
        ],
    )


app = create_app(config)
