"""
app/graph/nodes/input.py — Input Validation & Input Guardrail node

Responsibilities:
  1. Validate required fields are present.
  2. Run input guardrail checks (PII, injection, toxicity).
  3. Set defaults (retry_count, metadata, etc).
"""
import uuid
import structlog
from app.graph.state import ChatState
from app.ai.guardrails import check_input

logger = structlog.get_logger(__name__)


def input_validation_node(state: ChatState) -> ChatState:
    """Synchronous node — validates input and runs guardrails."""
    logger.info("Graph: input_validation_node", request_id=state.get("request_id"))

    # Initialise tracking fields
    updates: dict = {
        "retry_count": state.get("retry_count", 0),
        "guardrail_violations": [],
        "validation_errors": [],
        "metadata": state.get("metadata", {}),
        "error": None,
        "prompt_variables": state.get("prompt_variables", {}),
        "output_schema": state.get("output_schema"),
        "usage": {},
        "structured_output": None,
    }

    # --- Basic validation ---
    messages = state.get("messages", [])
    if not messages:
        updates["error"] = "No messages provided in request."
        return {**state, **updates}

    # Every message must have role + content
    for i, m in enumerate(messages):
        if not isinstance(m, dict) or "role" not in m or "content" not in m:
            updates["error"] = f"Message at index {i} is missing 'role' or 'content'."
            return {**state, **updates}

    # --- Guardrail check on user messages ---
    user_text = " ".join(m["content"] for m in messages if m["role"] == "user")
    result = check_input(user_text)
    if not result.passed:
        updates["guardrail_violations"] = result.violations
        updates["error"] = f"Input guardrail blocked request: {', '.join(result.violations)}"
        return {**state, **updates}

    logger.info("Graph: input_validation_node passed", request_id=state.get("request_id"))
    return {**state, **updates}
