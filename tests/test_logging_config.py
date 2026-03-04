from __future__ import annotations

import logging
import uuid

from app.logging_config import configure_logging, log_exception


def test_configure_logging_falls_back_to_info_for_invalid_log_level(monkeypatch) -> None:
    # Keep other inputs deterministic so this test isolates LOG_LEVEL behavior.
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("RUN_ID", "fixed-run-id")
    monkeypatch.setenv("LOG_LEVEL", "NOT_A_REAL_LEVEL")

    configure_logging()

    # Invalid level names should safely default to INFO.
    assert logging.getLogger().getEffectiveLevel() == logging.INFO


def test_configure_logging_generates_run_id_when_missing(monkeypatch) -> None:
    # Deliberately remove RUN_ID to exercise auto-generation path.
    monkeypatch.delenv("RUN_ID", raising=False)
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    run_id = configure_logging()

    # The returned value should be a valid UUID string.
    parsed = uuid.UUID(run_id)
    assert str(parsed) == run_id


def test_log_exception_includes_message_and_traceback(caplog) -> None:
    logger = logging.getLogger("tests.logging")

    # caplog captures records so we can assert logging behavior without stdout parsing.
    with caplog.at_level(logging.ERROR):
        try:
            raise ValueError("boom")
        except ValueError:
            log_exception(logger, "operation failed")

    assert "operation failed" in caplog.text
    assert "ValueError: boom" in caplog.text
