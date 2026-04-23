"""
app/graph/nodes/retry.py — Retry Logic node

Responsibilities:
  1. Increment retry_count.
  2. Build a corrective message explaining what failed.
  3. Inject the corrective prompt into messages so the LLM can fix its output.
  4. If max retries exceeded, set error and stop.
"""
import json
import structlog
from app.graph.state import ChatState
from app.config.settings import settings

logger = structlog.get_logger(__name__)


def retry_node(state: ChatState) -> ChatState:
    """Synchronous retry node — prepares corrective prompt for next LLM attempt."""
    retry_count = state.get("retry_count", 0)
    validation_errors = state.get("validation_errors", [])
    output_schema = state.get("output_schema")

    new_count = retry_count + 1
    logger.info(
        "Graph: retry_node",
        attempt=new_count,
        max=settings.MAX_RETRIES,
        errors=validation_errors,
    )

    if new_count > settings.MAX_RETRIES:
        logger.error("Graph: max retries exceeded")
        return {
            **state,
            "retry_count": new_count,
            "error": (
                f"Maximum retries ({settings.MAX_RETRIES}) exceeded. "
                f"Validation errors: {'; '.join(validation_errors)}"
            ),
        }

    # Build corrective instruction
    corrective_parts = [
        "Your previous response did not meet the required format. Please correct the following issues:",
    ]
    for err in validation_errors:
        corrective_parts.append(f"  - {err}")

    if output_schema:
        corrective_parts.append(
            f"\nYou MUST respond with valid JSON matching this schema:\n"
            f"{json.dumps(output_schema, indent=2)}\n"
            f"Do not include any text outside the JSON object."
        )

    corrective_msg = "\n".join(corrective_parts)

    # Inject corrective message into conversation
    messages = list(state.get("messages", []))
    if state.get("llm_response_raw"):
        messages.append({"role": "assistant", "content": state["llm_response_raw"]})
    messages.append({"role": "user", "content": corrective_msg})

    return {
        **state,
        "retry_count": new_count,
        "messages": messages,
        "validation_errors": [],
        "error": None,
    }
