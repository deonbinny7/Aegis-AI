# System Design — Altair AI

This document outlines the core design patterns, reliability features, retry hooks, and execution guardrails implemented in Altair AI.

---

## 🛠️ Design Patterns

1. **Repository Pattern**: Data access is abstracted via repositories (`UserRepository`, `SessionRepository`, `MessageRepository`, `PromptRepository`) to decouple database queries from business services.
2. **Factory Pattern**: The LLM Client Factory (`app/ai/providers/factory.py`) dynamically creates model providers (OpenAI, Anthropic, Gemini, Groq, Cerebras) using configuration structures.
3. **Dependency Injection**: FastAPI `Depends` is used to inject services, database connections, and authentication contexts, facilitating testability.
4. **State Machine (LangGraph)**: The request pipeline is modeled as an explicit state machine, enforcing execution orders.

---

## 🛡️ Guardrails Execution Flow

To ensure compliance and safety, guardrails are evaluated at two stages:

```
[Incoming Request] 
      ↓
(Input Guardrails)
   ├─ PII Masking (Regular expressions for emails, phone numbers)
   ├─ SQL/Prompt Injection Sanitizer
   └─ Parameter Bounds Checks (temperature [0,2], max_tokens > 0)
      ↓
[LLM Execution]
      ↓
(Output Guardrails)
   ├─ JSON Schema Conformity Validator
   ├─ Hallucination and Content Flags
   └─ Token Cost Calculation
```

If the LLM output violates JSON schemas, the output node forwards the error payload to the **Retry Node**, triggering up to `MAX_RETRIES` corrections before returning a structured error.

---

## 🧠 Memory and State Management

- **Short-Term Memory**: Stored in a sliding window in Redis. We retrieve the last $N$ messages (configured by `MEMORY_WINDOW_SIZE`) to serve as context for the current completion request.
- **Long-Term Persistence**: Persisted in PostgreSQL. Conversations are written using SQLAlchemy async engines, ensuring complete session history is preserved.

// Code style format review — 2026-06-23T13:40:18
