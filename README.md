# AI Project Template Baseline

Reusable, production-ready baseline template for new AI-focused Python repositories.

## What This Template Includes

- Python packaging with `poetry`
- Linting with `ruff`
- Static typing with `mypy --strict`
- Testing with `pytest`
- Container support via `Dockerfile` and `docker-compose.yml`
- GitHub Actions CI/CD pipeline with required stages:
  - Lint, type-check, and test
  - Docker image build
  - Dependency vulnerability scan
  - Release workflow
- Standard developer commands:
  - `make lint`
  - `make test`
  - `make run`
  - `make run-docker`
- Structured logging conventions with:
  - `LOG_LEVEL`
  - `ENV`
  - `run_id` correlation field

## Baseline Developer Workflow

```bash
poetry install
make lint
make test
make run
make run-docker
```

## Logging Baseline

All runtime logs should include:

- `timestamp`
- `level`
- `message`
- `ENV`
- `run_id`

Environment variables:

- `ENV`: execution environment (`local`, `dev`, `staging`, `prod`)
- `LOG_LEVEL`: logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `RUN_ID` (optional): correlation ID for a run; generated automatically if missing

## OpenTelemetry Policy

- OpenTelemetry instrumentation is required in the codebase from day 1.
- Runtime exporting is disabled by default in local/dev unless explicitly enabled.
- Exporting is enabled only when telemetry environment configuration is provided (for example `OTEL_EXPORTER_OTLP_ENDPOINT`).
- Goal: keep first-commit CI simple while keeping production observability wiring ready.

## CI/CD Baseline (GitHub Actions)

The pipeline must include:

1. `poetry install`
2. `make lint`
3. `make test`
4. Docker image build validation
5. Dependency vulnerability scan
6. Release workflow (tag-driven or main-branch gated)

## Scalability and Production Readiness

This template is designed to support early-stage projects and scale into production by default:

- Strict static analysis and tests to keep quality high as code volume grows
- Containerized runtime for consistent local, CI, and production behavior
- CI/CD checks that enforce security and delivery discipline
- Correlated structured logs for operational debugging across environments

## Why This Baseline

- Consistent quality gates across repositories
- Fast onboarding for new projects
- Predictable local and CI behavior
- Scalable defaults suitable for production workloads
- Better observability via correlated logs
