# Backend Guide — Altair AI

Technical documentation for the FastAPI backend, settings, database layer, and Celery workers.

---

## 🏗️ Core Modules

- **FastAPI application (`app/main.py`)**: Entry point loading lifespan events, configuration validators, middleware, exception handlers, and API router.
- **Config & Settings (`app/config/settings.py`)**: Subclass of Pydantic `BaseSettings` which reads variables from `.env` and exports settings configuration. It automatically replicates `.env.example` if no active `.env` file is present.
- **Database & Session (`app/db/session.py`)**: Async SQLAlchemy session engine using `asyncpg` drivers and session dependencies (`get_db`) injected during endpoints.
- **Observability (`app/core/observability.py`)**: Orchestrates Prometheus client exporters (`/metrics`) and exports OpenTelemetry tracer pipelines.

---

## ⚙️ Middleware

1. **`StructlogMiddleware`**: Implements structured context-aware logging using unique trace/request IDs injected via context variables.
2. **`CORSMiddleware`**: Configures access permissions for cross-origin client apps.
3. **`TrustedHostMiddleware`**: Restricts requests to allowed hostname arrays for security.

---

## 👷 Celery Workers (`app/workers/`)

Celery handles out-of-band execution tasks to keep endpoints fast:
- **`celery_app.py`**: Configures Celery to route tasks to Redis queues.
- **`tasks.py`**:
  - `async_audit_log`: Inserts request trace records into database logs.
  - `calculate_usage_costs`: Updates analytical records based on token counts and custom pricing models.

// Code style format review — 2026-05-29T14:03:49
