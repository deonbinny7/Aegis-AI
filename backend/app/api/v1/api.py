from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, chat, stream, analytics, experiments, providers, webhooks

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# Master Prompt 3 Endpoints
api_router.include_router(stream.router, prefix="/chat/stream", tags=["stream"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])

