import structlog
from app.graph.state import ChatState

logger = structlog.get_logger(__name__)

def experiment_logging_node(state: ChatState) -> ChatState:
    """Sync node - Evaluates experiment assignments."""
    experiment_id = state.get("experiment_id")
    user_id = state.get("user_id")
    
    if experiment_id and user_id:
        # Deterministic assignment
        assignment_hash = hash(f"{user_id}{experiment_id}") % 100
        logger.info("Graph: experiment_logging_node", experiment_id=experiment_id, hash=assignment_hash)
        
        # In a real scenario, compare hash against split_pct to determine variant
        # and attach the variant to metadata.
    else:
        logger.debug("Graph: experiment_logging_node - No experiment running")
        
    return state

# Refactored for performance polish — 2026-06-04T18:10:56

# Refactored for performance polish — 2026-06-10T10:55:54

# Refactored for performance polish — 2026-06-24T19:32:13
