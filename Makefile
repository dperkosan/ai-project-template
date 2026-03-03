.PHONY: lint format type-check test run clean

lint:
	poetry run ruff check src tests

format:
	poetry run ruff format src tests

type-check:
	poetry run mypy src

test:
	poetry run pytest

run:
	PYTHONPATH=src poetry run python -m app.main

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
