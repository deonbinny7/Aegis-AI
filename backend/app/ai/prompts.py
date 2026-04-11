"""
app/ai/prompts.py — Jinja2 Prompt Versioning Engine with Redis caching
"""
import json
import uuid
from typing import Optional

import structlog
from jinja2 import Environment, BaseLoader, TemplateSyntaxError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.settings import settings
from app.models.prompt_versions import PromptVersion

logger = structlog.get_logger(__name__)

_jinja_env = Environment(loader=BaseLoader(), autoescape=False)


def _cache_key(prompt_name: str, version: Optional[str]) -> str:
    v = version or "active"
    return f"prompt:template:{prompt_name}:{v}"


async def _get_redis() -> Redis:
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


# ---------------------------------------------------------------------------
# Core rendering
# ---------------------------------------------------------------------------

async def render_prompt(
    prompt_name: str,
    variables: dict,
    db: AsyncSession,
    version: Optional[str] = None,
) -> tuple[str, str]:
    """
    Render a prompt template with Jinja2.
    Returns (rendered_text, prompt_version_id).
    Falls back to a simple no-op if no prompt is found.
    """
    cache_key = _cache_key(prompt_name, version)

    # --- Cache lookup ---
    template_data = None
    try:
        redis = await _get_redis()
        cached = await redis.get(cache_key)
        await redis.aclose()
        if cached:
            template_data = json.loads(cached)
            logger.debug("Prompt cache hit", prompt=prompt_name, version=version)
    except Exception as e:
        logger.warning("Redis prompt cache read failed", error=str(e))

    # --- DB lookup ---
    if not template_data:
        query = select(PromptVersion).where(PromptVersion.name == prompt_name)
        if version:
            query = query.where(PromptVersion.version == version)
        else:
            query = query.where(PromptVersion.is_active == True)
        query = query.order_by(PromptVersion.version.desc()).limit(1)

        result = await db.execute(query)
        pv = result.scalar_one_or_none()

        if pv:
            template_data = {"id": pv.id, "template": pv.template}
            # Warm cache
            try:
                redis = await _get_redis()
                await redis.setex(cache_key, settings.PROMPT_CACHE_TTL, json.dumps(template_data))
                await redis.aclose()
            except Exception as e:
                logger.warning("Redis prompt cache write failed", error=str(e))

    if not template_data:
        logger.warning("No prompt template found", prompt=prompt_name)
        # No template — return the raw user message as-is
        user_msg = variables.get("user_message", "")
        return user_msg, ""

    # --- Jinja2 render ---
    try:
        tmpl = _jinja_env.from_string(template_data["template"])
        rendered = tmpl.render(**variables)
    except TemplateSyntaxError as e:
        logger.error("Jinja2 template syntax error", prompt=prompt_name, error=str(e))
        rendered = variables.get("user_message", "")

    return rendered, template_data["id"]


# ---------------------------------------------------------------------------
# CRUD helpers
# ---------------------------------------------------------------------------

async def create_prompt(
    name: str,
    template: str,
    version: str,
    variables: Optional[list] = None,
    tags: Optional[list] = None,
    db: AsyncSession = None,
) -> PromptVersion:
    pv = PromptVersion(
        id=str(uuid.uuid4()),
        name=name,
        version=version,
        template=template,
        variables=variables or [],
        tags=tags or [],
        is_active=True,
    )
    db.add(pv)
    await db.flush()
    return pv


async def deactivate_old_versions(name: str, current_id: str, db: AsyncSession) -> None:
    """Set all versions of a prompt to inactive except the current one."""
    result = await db.execute(
        select(PromptVersion)
        .where(PromptVersion.name == name, PromptVersion.id != current_id)
    )
    for pv in result.scalars().all():
        pv.is_active = False
    await db.flush()


async def invalidate_prompt_cache(prompt_name: str) -> None:
    """Remove all cached versions of a prompt from Redis."""
    try:
        redis = await _get_redis()
        pattern = f"prompt:template:{prompt_name}:*"
        keys = await redis.keys(pattern)
        if keys:
            await redis.delete(*keys)
        await redis.aclose()
    except Exception as e:
        logger.warning("Redis prompt cache invalidation failed", error=str(e))
