"""
Logging configuration.

Sets up structured, levelled logging for the entire application.
Call configure_logging() once at startup (in lifecycle.py) before any
other module emits log records.

Design decisions:
    - Standard-library logging is used directly to avoid adding a dependency
      on loguru or structlog in Module 1.
    - JSON output is enabled via log_json=True in settings so that log
      aggregators (Datadog, Loki, CloudWatch) can parse fields without regex.
    - The root logger is configured; individual modules obtain child loggers
      via logging.getLogger(__name__) as usual.

FUTURE UPGRADE:
    Replace the plain JSON formatter with structlog when structured,
    contextual logging (e.g. attaching request_id to every log line within
    a request) becomes a hard requirement.  Structlog integrates with the
    standard-library handler tree, so the switch is non-breaking.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any


class _JsonFormatter(logging.Formatter):
    """
    Emit each log record as a single-line JSON object.

    Fields: timestamp, level, logger, message, and any extra fields
    attached via LogRecord.__dict__.
    """

    _RESERVED: frozenset[str] = frozenset(
        {
            "args", "created", "exc_info", "exc_text", "filename", "funcName",
            "levelname", "levelno", "lineno", "message", "module", "msecs",
            "msg", "name", "pathname", "process", "processName", "relativeCreated",
            "stack_info", "taskName", "thread", "threadName",
        }
    )

    def format(self, record: logging.LogRecord) -> str:
        record.message = record.getMessage()

        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.message,
        }

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        # Attach any extra fields passed via logger.info("msg", extra={...})
        for key, value in record.__dict__.items():
            if key not in self._RESERVED:
                payload[key] = value

        return json.dumps(payload, default=str)


def configure_logging(level: str = "INFO", use_json: bool = False) -> None:
    """
    Configure the root logger.

    Args:
        level:    Python logging level string (e.g. "INFO", "DEBUG").
        use_json: When True, emit JSON-formatted records to stdout.
                  When False, emit human-readable records (development default).
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        _JsonFormatter() if use_json else logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )

    root = logging.getLogger()
    root.setLevel(level.upper())

    # Remove any handlers added by third-party libraries before ours.
    root.handlers.clear()
    root.addHandler(handler)

    # Suppress noisy third-party loggers.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
