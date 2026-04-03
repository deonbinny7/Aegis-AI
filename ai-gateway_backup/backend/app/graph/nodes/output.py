"""
app/graph/nodes/output.py — Output Guardrail + JSON Schema Validation node

Responsibilities:
  1. Run output guardrails on the LLM response.
  2. If an output_schema is set: parse the response as JSON and validate it.
  3. On validation failure: populate validation_errors to trigger retry.
  4. On success: populate final_response and structured_output.
"""
import json
import re
import structlog
from pydantic import ValidationError

from app.graph.state import ChatState
from app.ai.guardrails import check_output

logger = structlog.get_logger(__name__)

_JSON_FENCE = re.compile(r"```(?:json)?\s*([\s\S]+?)\s*```", re.I)


def _extract_json(text: str) -> str:
    """Try to extract JSON from markdown fences or bare text."""
    m = _JSON_FENCE.search(text)
    if m:
        return m.group(1).strip()
    # Try to find outermost {...} or [...]
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        end = text.rfind(end_char)
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]
    return text.strip()


def output_validation_node(state: ChatState) -> ChatState:
    """Synchronous output validation node."""
    response_text = state.get("llm_response_raw", "")
    logger.info("Graph: output_validation_node", chars=len(response_text))

    # --- Output guardrails ---
    guard_result = check_output(response_text)
    if not guard_result.passed:
        return {
            **state,
            "error": f"Output guardrail blocked response: {', '.join(guard_result.violations)}",
            "guardrail_violations": guard_result.violations,
        }

    # --- JSON schema validation (if required) ---
    output_schema = state.get("output_schema")
    if output_schema:
        json_str = _extract_json(response_text)
        try:
            parsed = json.loads(json_str)
        except (json.JSONDecodeError, ValueError) as e:
            errors = [f"JSON parse error: {e}. Raw response: {response_text[:200]}"]
            logger.warning("Graph: output_validation JSON parse failed", errors=errors)
            return {
                **state,
                "validation_errors": errors,
                "final_response": response_text,
                "structured_output": None,
            }

        # Validate required keys from schema
        required_keys = output_schema.get("required", [])
        missing = [k for k in required_keys if k not in parsed]
        if missing:
            errors = [f"Missing required fields in JSON output: {missing}"]
            logger.warning("Graph: output_validation schema mismatch", errors=errors)
            return {
                **state,
                "validation_errors": errors,
                "final_response": response_text,
                "structured_output": None,
            }

        logger.info("Graph: output_validation JSON passed")
        return {
            **state,
            "validation_errors": [],
            "structured_output": parsed,
            "final_response": json.dumps(parsed, ensure_ascii=False),
            "error": None,
        }

    # --- Free-form response ---
    return {
        **state,
        "validation_errors": [],
        "structured_output": None,
        "final_response": response_text,
        "error": None,
    }
