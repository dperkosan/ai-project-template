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
  - `make type-check`
  - `make test`
  - `make audit`
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
make type-check
make test
make audit
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
3. `make type-check`
4. `make test`
5. `make audit` (dependency vulnerability scan)
6. Docker image build validation
7. Release workflow (tag-driven or main-branch gated)

## Artifact And Deployment Flow

- GitHub repository stores source code.
- CI workflow validates quality and builds a Docker image.
- GHCR (GitHub Container Registry) stores built Docker images with tags (for example `v0.1.0`).
- Deployment platforms pull images from GHCR and run them.

Why GHCR is used:

- It gives a central, versioned image registry tied to the repository.
- It supports a "build once, deploy many" release model.
- It makes rollbacks easier because older image tags remain available.

## Branch Protection Baseline

Configure branch protection for `main` in GitHub repository settings:

1. Require a pull request before merging
2. Require status checks to pass before merging
3. Select required check: `quality-and-build`
4. Require branches to be up to date before merging
5. Require conversation resolution before merging
6. Do not allow bypassing the above settings

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
