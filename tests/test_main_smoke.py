from __future__ import annotations

from app.main import main


def test_main_logs_env_and_run_id(monkeypatch, capsys) -> None:
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    monkeypatch.setenv("RUN_ID", "test-run-123")

    main()
    captured = capsys.readouterr()

    assert "env=test" in captured.err
    assert "run_id=test-run-123" in captured.err
    assert "Application started (run_id=test-run-123)" in captured.err
