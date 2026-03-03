.PHONY: lint format type-check test audit run run-docker clean

lint:
	poetry run ruff check src tests

format:
	poetry run ruff format src tests

type-check:
	poetry run mypy src

test:
	poetry run pytest

audit:
	poetry run pip-audit --cache-dir .pip-audit-cache

run:
	PYTHONPATH=src poetry run python -m app.main

run-docker:
	docker compose run --build --rm app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
