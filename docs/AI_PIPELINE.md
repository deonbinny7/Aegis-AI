# AI Pipeline Guide — Altair AI

This guide details the AI workflow processing steps inside Altair AI, focusing on prompt rendering, input sanitization, and output guardrails.

---

## 📝 Dynamic Prompt Rendering

The prompt engine retrieves, compiles, and versions prompt templates at runtime.

### How it works:
1. When a client requests `/api/v1/chat` with a `prompt_name` (e.g., `translate_text`) and `prompt_variables` (e.g., `{"target_lang": "Spanish"}`):
2. The `prompt_render` node fetches the active template from the database:
   * Template content: `Translate the following text into {{target_lang}}: {{text}}`
3. Variables are bound using a custom renderer, and the resulting message list is passed downstream.

---

## 🛡️ Guardrails Configuration

Guardrails check requests before execution to protect against exploits and leaking data.

### Input Guardrails:
* **PII Redaction**: Regex engines scan incoming strings for email patterns (`[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+`) and phone number configurations, replacing them with generic `[REDACTED_EMAIL]` / `[REDACTED_PHONE]` placeholders.
* **Injection Detection**: Simple heuristic and pattern matchers block commands attempting to overwrite instructions (e.g. "Ignore previous commands...").

### Output Guardrails:
* **JSON Schema Enforcement**: If the request specifies an `output_schema`, the gateway parses model completions using `pydantic.TypeAdapter.validate_json`. If parsing fails, it submits the error back to a retry queue.

// Code style format review — 2026-06-23T21:07:56
