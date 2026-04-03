from celery import Celery
import os
from app.config.settings import settings

celery_app = Celery(
    "ai_gateway_workers",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.workers.tasks.analytics",
        "app.workers.tasks.benchmarking",
        "app.workers.tasks.webhooks"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)
