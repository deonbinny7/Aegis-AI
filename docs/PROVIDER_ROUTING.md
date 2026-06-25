# Provider Routing & Models — Altair AI

Altair AI integrates with multiple LLM API providers through a unified interface. This guide details supported models, routing strategies, and pricing metrics.

---

## 🔌 Supported Providers and Models

The gateway abstracts APIs into standard execution interfaces:

| Provider | Supported Models | Primary Use Case |
| --- | --- | --- |
| **Groq** | `llama3-8b-8192`, `llama3-70b-8192`, `mixtral-8x7b-32768` | Low-latency completions |
| **Cerebras** | `llama3.1-8b`, `llama3.1-70b` | High-throughput ultra-fast inference |
| **Google** | `gemini-1.5-flash`, `gemini-1.5-pro` | Multi-modal & large context processing |
| **OpenAI** | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` | Structured tasks & complex logic |
| **Anthropic** | `claude-3-5-sonnet`, `claude-3-haiku` | Reasoning & structured JSON parsing |
| **OpenRouter** | Any (via OpenRouter proxy pass) | Fallback models aggregation |

---

## 🔀 Routing Strategies

Configure how requests are distributed via the `routing_strategy` parameter:

1. **`explicit`**: Directs requests directly to the model specified in `model_id`. No failover occurs.
2. **`fallback`**: Attempts completion on `model_id`. If the provider fails (e.g. rate limit error or timeout), the router attempts recovery on secondary backups.
   * *Example*: `llama3-70b-8192` (Groq) fallback path → `gemini-1.5-flash` (Google) → `gpt-4o-mini` (OpenAI).
3. **`latency-optimized`**: Routes the query to the fastest active provider measured by recent experiment metrics.
4. **`cost-optimized`**: Routes the query to the lowest-priced provider matching the required context window.

---

## 💰 Cost Tracking Metrics

Pricing models are cached in `app/analytics/cost_calculator.py` to audit usage costs:

* **Llama3-8b (Groq)**: $0.05 per Million prompt tokens / $0.08 per Million completion tokens.
* **GPT-4o-mini (OpenAI)**: $0.150 per Million prompt tokens / $0.600 per Million completion tokens.
* **Gemini-1.5-Flash (Google)**: $0.075 per Million prompt tokens / $0.300 per Million completion tokens.
