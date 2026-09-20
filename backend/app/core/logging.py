"""Structured logging (§51).

Logs agent execution, search duration, result counts, latency and errors.
Never logs API keys, secrets or sensitive user information.
"""

import logging
import sys

import structlog

from app.core.config import settings

_SENSITIVE_KEYS = {
    "api_key",
    "tavily_api_key",
    "llm_api_key",
    "openai_api_key",
    "authorization",
    "password",
    "token",
    "secret",
}


def _redact_sensitive(_logger, _method, event_dict):
    """Redact any sensitive keys before they reach the log output."""
    for key in list(event_dict.keys()):
        if key.lower() in _SENSITIVE_KEYS:
            event_dict[key] = "***REDACTED***"
    return event_dict


def configure_logging() -> None:
    """Configure structlog + stdlib logging once at startup."""
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.debug else logging.INFO,
    )

    renderer = (
        structlog.dev.ConsoleRenderer()
        if settings.environment == "development"
        else structlog.processors.JSONRenderer()
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            _redact_sensitive,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if settings.debug else logging.INFO
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a bound structlog logger."""
    return structlog.get_logger(name)
