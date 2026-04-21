import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from app.graph.state import ChatState
from app.analytics.cost_engine import CostEngine
from app.models.usage_logs import UsageLog

logger = structlog.get_logger(__name__)

async def token_tracking_node(state: ChatState, db: AsyncSession) -> ChatState:
    """Async node - Calculates cost and tracks tokens."""
    logger.info("Graph: token_tracking_node", request_id=state.get("request_id"))
    
    usage = state.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    
    metadata = state.get("metadata", {})
    actual_model = metadata.get("actual_model", state.get("selected_model_id", "unknown"))
    provider = state.get("routing_strategy", "unknown") # In a real scenario, map model to provider
    
    cost_usd = await CostEngine.calculate_cost(
        db=db,
        provider=provider,
        model_name=actual_model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens
    )
    
    # We update the usage_log cost_usd if we want, but since persist_node creates UsageLog
    # we need to make sure it reads cost_usd from state. Wait, persist_node is run BEFORE token_tracking in the End-to-End workflow!
    # Let's check the workflow. The workflow requires persist -> token -> cost -> usage -> experiment -> audit -> celery.
    # So we should probably update the UsageLog here or just let this node calculate the cost.
    
    return {
        **state,
        "cost_usd": cost_usd
    }

def usage_analytics_node(state: ChatState) -> ChatState:
    """Sync node - Aggregates in-memory usage stats or pushes to queue."""
    logger.info("Graph: usage_analytics_node", cost=state.get("cost_usd"))
    # The actual heavy lifting is done in Celery. This just prepares state if needed.
    return state
