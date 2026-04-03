# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-06-25 (Enterprise Release)

### Added
- Complete integration of **LangGraph** orchestration for the entire requests lifecycle.
- SSE streaming backend endpoint `/api/v1/stream` with real-time token tracking.
- Output validation using custom JSON schema matching and automatic LLM retry hooks.
- OpenTelemetry instrumentation for endpoint latency and service invocation tracing.
- React-based dashboard UI featuring interactive model playgrounds, prompt versioning libraries, and live analytics.

### Changed
- Refactored user database schemas to use SQLAlchemy 2.0 async sessions.
- Enhanced API key management utilizing secure runtime configuration overrides.

---

## [0.8.0] - 2026-05-15 (Observability Phase)

### Added
- Structured logging configuration using `structlog` for backend nodes and routers.
- Prometheus exporter path `/metrics` with tracking for LLM token throughput, latency distribution, and request counts.
- Celery task tracking for async logging, cost auditing, and analytical updates.

### Fixed
- Handled concurrency constraints inside Redis sliding window memory checks.

---

## [0.5.0] - 2026-04-20 (AI Gateway Phase)

### Added
- Dynamic model factory supporting OpenAI, Anthropic, Gemini, Groq, and Cerebras APIs.
- Fallback and load-balancing routers with runtime configuration changes.
- Input guardrails including prompt injection sanitization and email/phone PII masking.
- Dynamic prompt template renderer with custom template engines.

---

## [0.1.0] - 2026-04-01 (Project Foundation)

### Added
- Monorepo folder layout (FastAPI backend and React frontend).
- Core database scaffold using PostgreSQL, SQLAlchemy, and Alembic migrations.
- Redis integration for token cache and message history storage.
- User management and JWT-based authentication schemas.
- Docker and Docker Compose environments for development and testing.
