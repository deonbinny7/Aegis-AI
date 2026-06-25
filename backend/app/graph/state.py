"""
app/graph/state.py — Canonical LangGraph State TypedDict

All graph nodes read from and write to this single state object.
"""
from typing import Any, Optional
from typing_extensions import TypedDict


class ChatState(TypedDict, total=False):
    # ── Input ─────────────────────────────────────────────────────────────
    request_id: str
    trace_id: str
    correlation_id: str
    user_id: str
    session_id: str
    messages: list[dict]          # [{"role": ..., "content": ...}]
    model_id: str                 # explicit model or empty for router to decide
    routing_strategy: str         # "explicit" | "cheapest" | "fastest" | "smart"
    prompt_name: Optional[str]    # optional prompt template name
    prompt_variables: dict        # variables injected into Jinja2 template
    output_schema: Optional[dict] # JSON schema the response must match
    temperature: float
    max_tokens: Optional[int]
    experiment_id: Optional[str]  # for A/B testing

    # ── Intermediate ──────────────────────────────────────────────────────
    rendered_prompt: str          # Jinja2-rendered system prompt
    prompt_version_id: str        # which PromptVersion was used
    memory_context: list[dict]    # conversation history from Redis/PG
    selected_model_id: str        # model chosen by router
    llm_response_raw: str         # raw LLM output text
    usage: dict                   # {prompt_tokens, completion_tokens, total_tokens}

    # ── Retry / Validation ────────────────────────────────────────────────
    retry_count: int
    validation_errors: list[str]
    structured_output: Optional[dict]  # parsed JSON if output_schema present

    # ── Output ────────────────────────────────────────────────────────────
    final_response: str
    guardrail_violations: list[str]
    error: Optional[str]
    metadata: dict                # routing decision, latency, etc.
    cost_usd: float               # cost calculated by analytics node
    audit_status: str             # status from audit node
    execution_duration: float     # overall execution duration
