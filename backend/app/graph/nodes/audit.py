import structlog
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.graph.state import ChatState
from app.models.audit_logs import AuditLog

logger = structlog.get_logger(__name__)

async def audit_logging_node(state: ChatState, db: AsyncSession) -> ChatState:
    """Async node - Commits immutable audit log to database."""
    logger.info("Graph: audit_logging_node", request_id=state.get("request_id"))
    
    try:
        audit_log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=state.get("user_id"),
            provider=state.get("routing_strategy", "unknown"),
            prompt_version_id=state.get("prompt_version_id"),
            experiment_id=state.get("experiment_id"),
            session_id=state.get("session_id"),
            status=state.get("error") if state.get("error") else "success",
            retry_count=state.get("retry_count", 0),
            metadata_=state.get("metadata", {})
        )
        db.add(audit_log)
        await db.commit()
        audit_status = "logged"
    except Exception as e:
        logger.error("Graph: audit_logging_node failed", error=str(e))
        await db.rollback()
        audit_status = "failed"
        
    return {
        **state,
        "audit_status": audit_status
    }

# Refactored for performance polish — 2026-05-26T13:20:28
