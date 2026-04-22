"""
app/graph/nodes/persist.py — Conversation Persistence node

Responsibilities:
  1. Save the user turn and assistant turn to PostgreSQL.
  2. Update Redis sliding-window memory.
  3. Write UsageLog record for analytics.
"""
import uuid
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.graph.state import ChatState
from app.ai import memory as mem
from app.models.usage_logs import UsageLog
from app.models.messages import Message

logger = structlog.get_logger(__name__)


async def persist_node(state: ChatState, db: AsyncSession) -> ChatState:
    """Async persistence node — commits conversation to DB and Redis."""
    session_id = state.get("session_id", "")
    user_id = state.get("user_id", "")

    if not session_id:
        logger.warning("Graph: persist_node skipped — no session_id")
        return state

    logger.info("Graph: persist_node", session_id=session_id)

    try:
        # --- Find last user message ---
        original_messages = state.get("messages", [])
        user_msgs = [m for m in original_messages if m["role"] == "user"]
        assistant_response = state.get("final_response", "")

        # Persist last user message
        if user_msgs:
            last_user = user_msgs[-1]
            await mem.save_message(
                session_id=session_id,
                role="user",
                content=last_user["content"],
                db=db,
                metadata={
                    "request_id": state.get("request_id"),
                    "prompt_version_id": state.get("prompt_version_id"),
                },
            )

        # Persist assistant response
        if assistant_response:
            await mem.save_message(
                session_id=session_id,
                role="assistant",
                content=assistant_response,
                db=db,
                metadata={
                    "request_id": state.get("request_id"),
                    "model": state.get("metadata", {}).get("actual_model"),
                    "prompt_version_id": state.get("prompt_version_id"),
                    "retry_count": state.get("retry_count", 0),
                },
            )

        # --- Write usage log ---
        usage = state.get("usage", {})
        model_meta = state.get("metadata", {})
        usage_log = UsageLog(
            id=str(uuid.uuid4()),
            user_id=user_id or None,
            session_id=session_id,
            model=model_meta.get("actual_model", state.get("selected_model_id", "unknown")),
            provider=state.get("routing_strategy", "explicit"),
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            cost_usd=0.0,  # Pricing calculation can be added later
            latency_ms=model_meta.get("latency_ms", 0),
        )
        db.add(usage_log)
        await db.commit()

        logger.info("Graph: persist_node complete", session_id=session_id)
    except Exception as e:
        logger.error("Graph: persist_node failed", error=str(e))
        await db.rollback()

    return state
