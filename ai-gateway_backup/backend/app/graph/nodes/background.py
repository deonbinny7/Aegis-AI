import structlog
from app.graph.state import ChatState
from app.workers.tasks.analytics import aggregate_metrics_task

logger = structlog.get_logger(__name__)

def celery_trigger_node(state: ChatState) -> ChatState:
    """Sync node - Dispatches background tasks via Celery."""
    logger.info("Graph: celery_trigger_node", request_id=state.get("request_id"))
    
    # Trigger async analytics task
    request_id = state.get("request_id")
    if request_id:
        aggregate_metrics_task.delay(request_id)
    
    return state
