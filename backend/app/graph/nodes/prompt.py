"""
app/graph/nodes/prompt.py — Prompt Rendering & Memory Injection node

Responsibilities:
  1. Load conversation history from Redis/PostgreSQL (memory manager).
  2. Render the Jinja2 prompt template (if configured).
  3. Trim the context window to fit within model limits.
  4. Assemble the final messages list ready for LLM invocation.
"""
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.graph.state import ChatState
from app.ai import memory as mem
from app.ai import prompts as prompt_engine

logger = structlog.get_logger(__name__)


async def prompt_render_node(state: ChatState, db: AsyncSession) -> ChatState:
    """Async node — renders prompt and injects memory context."""
    logger.info("Graph: prompt_render_node", session_id=state.get("session_id"))

    session_id = state.get("session_id", "")
    messages = list(state.get("messages", []))

    # 1. Load memory
    history: list[dict] = []
    if session_id:
        try:
            history = await mem.load_memory(session_id, db)
        except Exception as e:
            logger.warning("Memory load failed, proceeding without history", error=str(e))

    # 2. Render system prompt via Jinja2 (if prompt_name configured)
    rendered_prompt = ""
    prompt_version_id = ""
    prompt_name = state.get("prompt_name")
    if prompt_name:
        variables = {
            **state.get("prompt_variables", {}),
            "user_message": messages[-1]["content"] if messages else "",
        }
        rendered_prompt, prompt_version_id = await prompt_engine.render_prompt(
            prompt_name, variables, db
        )

    # 3. Build full message list: system + history + current messages
    full_messages: list[dict] = []
    if rendered_prompt:
        full_messages.append({"role": "system", "content": rendered_prompt})
    full_messages.extend(history)
    full_messages.extend(messages)

    # 4. Context trimming (preserves recency)
    trimmed = await mem.trim_context(full_messages)

    logger.info(
        "Graph: prompt_render_node complete",
        history_msgs=len(history),
        total_msgs=len(trimmed),
    )

    return {
        **state,
        "memory_context": history,
        "rendered_prompt": rendered_prompt,
        "prompt_version_id": prompt_version_id,
        "messages": trimmed,
    }

# Refactored for performance polish — 2026-06-19T13:43:35
