"""
app/ai/memory.py — Redis Sliding-Window + PostgreSQL Persistent Memory Manager
"""
import json
import uuid
from typing import Optional
from datetime import datetime

import structlog
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.config.settings import settings
from app.models.messages import Message
from app.models.sessions import Session

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Redis helpers
# ---------------------------------------------------------------------------

def _window_key(session_id: str) -> str:
    return f"memory:session:{session_id}:window"


async def get_redis() -> Redis:
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

async def load_memory(session_id: str, db: AsyncSession) -> list[dict]:
    """
    Returns conversation history for a session.
    1. Check Redis sliding-window (fast path).
    2. Fall back to PostgreSQL if Redis is cold.
    """
    try:
        redis = await get_redis()
        raw = await redis.lrange(_window_key(session_id), 0, -1)
        await redis.aclose()
        if raw:
            return [json.loads(m) for m in raw]
    except Exception as e:
        logger.warning("Redis memory read failed, falling back to DB", error=str(e))

    # Cold path — load from PostgreSQL
    result = await db.execute(
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(desc(Message.metadata_["created_at"].as_string()))
        .limit(settings.MEMORY_WINDOW_SIZE)
    )
    messages = result.scalars().all()
    history = [{"role": m.role, "content": m.content} for m in reversed(messages)]
    # Warm Redis
    await save_memory_bulk(session_id, history)
    return history


async def save_message(
    session_id: str,
    role: str,
    content: str,
    db: AsyncSession,
    metadata: Optional[dict] = None,
) -> Message:
    """Persist a single message to PostgreSQL and push to Redis sliding window."""
    msg = Message(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role=role,
        content=content,
        metadata_=metadata or {},
    )
    db.add(msg)
    await db.flush()

    # Push to Redis window
    try:
        redis = await get_redis()
        key = _window_key(session_id)
        payload = json.dumps({"role": role, "content": content})
        await redis.rpush(key, payload)
        # Trim to window size (keep last N messages)
        await redis.ltrim(key, -settings.MEMORY_WINDOW_SIZE, -1)
        await redis.aclose()
    except Exception as e:
        logger.warning("Redis memory write failed", error=str(e))

    return msg


async def save_memory_bulk(session_id: str, messages: list[dict]) -> None:
    """Overwrite the Redis window with a fresh message list."""
    try:
        redis = await get_redis()
        key = _window_key(session_id)
        await redis.delete(key)
        for m in messages[-settings.MEMORY_WINDOW_SIZE :]:
            await redis.rpush(key, json.dumps(m))
        await redis.aclose()
    except Exception as e:
        logger.warning("Redis bulk memory write failed", error=str(e))


async def trim_context(messages: list[dict], max_tokens: int = 3000) -> list[dict]:
    """
    Heuristic context trimmer — keeps the system message (if present) and
    as many recent exchanges as fit within the estimated token budget.
    (Rough estimate: 1 token ≈ 4 chars.)
    """
    if not messages:
        return []

    system = [m for m in messages if m["role"] == "system"]
    non_system = [m for m in messages if m["role"] != "system"]

    budget = max_tokens * 4  # chars budget
    used = sum(len(m["content"]) for m in system)
    trimmed = []

    for m in reversed(non_system):
        used += len(m["content"])
        if used > budget:
            break
        trimmed.insert(0, m)

    return system + trimmed


async def get_or_create_session(
    session_id: Optional[str], user_id: str, db: AsyncSession
) -> str:
    """Return existing session or create a new one."""
    if session_id:
        result = await db.execute(
            select(Session).where(Session.id == session_id, Session.user_id == user_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return session_id

    new_session = Session(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title="New Conversation",
    )
    db.add(new_session)
    await db.flush()
    return new_session.id
