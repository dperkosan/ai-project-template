from __future__ import annotations

import logging
import os
import uuid
from typing import Any

"""This file configures application logging for local, CI, and production runs.

Use `configure_logging()` once at application startup (for example in `main.py`)
before creating/using loggers in the rest of the code.

It standardizes log output and attaches shared context fields:
- `env` from ENV (local/dev/staging/prod)
- `run_id` from RUN_ID or auto-generated UUID when not provided
- log level from LOG_LEVEL with INFO as safe fallback
"""

# Default values used when environment variables are missing.
DEFAULT_ENV = "local"
DEFAULT_LOG_LEVEL = "INFO"

# Save Python's original log record factory so we can wrap it.
BASE_LOG_RECORD_FACTORY = logging.getLogRecordFactory()


def _get_env() -> str:
    """Read ENV from the environment, with a safe default."""
    # Example values: local, dev, staging, prod.
    env = os.getenv("ENV", DEFAULT_ENV).strip()
    return env or DEFAULT_ENV


def _get_log_level() -> int:
    """Convert LOG_LEVEL text (like 'INFO') into a logging level integer."""
    # Normalize input so values like "info" or " Info " still work.
    raw_level = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).strip().upper()

    # logging.INFO / logging.DEBUG / ... are integer constants on logging.
    # getattr returns None if the level name does not exist.
    level = getattr(logging, raw_level, None)

    # Fall back to INFO if the value is invalid.
    if isinstance(level, int):
        return level
    return logging.INFO


def _get_run_id() -> str:
    """Return RUN_ID from env, or generate one if missing.

    RUN_ID helps correlate many log lines that belong to one program run.
    """
    run_id = os.getenv("RUN_ID", "").strip()
    if run_id:
        return run_id
    return str(uuid.uuid4())


def configure_logging() -> str:
    """Configure global logging and return the active run_id.

    This function should be called once near application startup.
    """
    env = _get_env()
    run_id = _get_run_id()
    log_level = _get_log_level()

    def record_factory(*args: Any, **kwargs: Any) -> logging.LogRecord:
        """Create a log record and attach template-wide context fields."""
        record = BASE_LOG_RECORD_FACTORY(*args, **kwargs)

        # Add fields used by our log format string.
        # These become available as %(env)s and %(run_id)s.
        record.env = env
        record.run_id = run_id
        return record

    # Install our wrapped factory so all future records get env/run_id fields.
    logging.setLogRecordFactory(record_factory)

    # force=True replaces any previous root handlers/config.
    # This keeps behavior predictable across local runs and tests.
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s level=%(levelname)s env=%(env)s run_id=%(run_id)s msg=%(message)s",
        force=True,
    )

    return run_id


def log_exception(logger: logging.Logger, message: str) -> None:
    """Log an error with traceback information.

    Call this inside an `except` block so the current exception stack trace
    is included automatically.
    """
    logger.exception(message)
