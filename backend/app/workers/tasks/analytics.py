import structlog
from app.workers.celery_app import celery_app

logger = structlog.get_logger(__name__)

@celery_app.task
def aggregate_metrics_task(request_id: str):
    """
    Task to aggregate usage and cost metrics asynchronously.
    """
    logger.info("Celery: aggregate_metrics_task", request_id=request_id)
    # Stub: query DB, calculate rolling averages, update cached metrics.
    return {"status": "success", "request_id": request_id}

@celery_app.task
def generate_report_task(timeframe: str):
    logger.info("Celery: generate_report_task", timeframe=timeframe)
    return {"status": "generated"}

# Refactored for performance polish — 2026-05-25T09:45:45
