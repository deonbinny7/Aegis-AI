from typing import AsyncGenerator, Annotated, Any
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
import structlog
from app.db.session import get_db
from app.config.settings import Settings, settings
from app.auth.dependencies import get_current_user
from app.schemas.auth import TokenData

def get_settings() -> Settings:
    return settings

def get_logger(request: Request):
    return structlog.get_logger(__name__).bind(
        request_id=request.headers.get("X-Request-ID")
    )

async def get_redis() -> AsyncGenerator[Redis, None]:
    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.aclose()

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
CurrentUserDep = Annotated[TokenData, Depends(get_current_user)]
LoggerDep = Annotated[structlog.BoundLogger, Depends(get_logger)]
RedisDep = Annotated[Redis, Depends(get_redis)]

# Refactored for performance polish — 2026-06-15T16:08:27
