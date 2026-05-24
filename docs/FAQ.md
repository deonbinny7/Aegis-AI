# FAQ — Altair AI

Frequently Asked Questions regarding the architecture, operation, and roadmap of Altair AI.

---

## ❓ General Questions

### Why did you choose LangGraph for orchestration?
LangGraph provides a stateful, cyclic graph executor that is ideal for handling LLM request pipelines. It natively supports structured retries, conditional edge routing (e.g. dynamically changing models on provider failure), and incremental state retention, which is difficult to model in simple linear pipelines.

### How do I integrate a new LLM provider?
To add a new provider:
1. Open `backend/app/ai/providers/factory.py`.
2. Add your provider class (implementing the standard generation interface).
3. Update the `get_provider` switch matching to instantiate your client.
4. Define any necessary environment variables in `.env.example` and load them into `app/config/settings.py`.

### How does the streaming endpoint calculate pricing?
The Server-Sent Events (SSE) stream (`/api/v1/stream`) tracks completion tokens as they arrive. Upon completion, the last message block carries an event containing the exact usage metrics (prompt and completion tokens). The Cost Calculator then multiplies these metrics by the provider's token rates to log the total request cost.

### Can I run this in production without Docker?
Yes. You can host the components on separate VMs or managed instances (e.g. AWS RDS for Postgres, ElastiCache for Redis, and ECS/VMs for FastAPI and Celery). Simply override the environment variables in your release configuration to point to these endpoints.

// Code style format review — 2026-05-24T21:48:21
