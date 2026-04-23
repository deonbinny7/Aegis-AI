"""
app/graph/nodes/router.py — Model Router node

Responsibilities:
  1. Inspect routing_strategy from state.
  2. Select the optimal model (or list for fallback).
  3. Store selected_model_id in state.
"""
import structlog
from app.graph.state import ChatState
from app.ai.router import ModelRouter, RoutingStrategy
from app.config.settings import settings

logger = structlog.get_logger(__name__)


def router_node(state: ChatState) -> ChatState:
    """Synchronous routing node — selects the model to use."""
    logger.info("Graph: router_node", strategy=state.get("routing_strategy"))

    strategy_str = state.get("routing_strategy", settings.DEFAULT_ROUTING_STRATEGY)
    explicit_model = state.get("model_id") or settings.DEFAULT_MODEL

    try:
        strategy = RoutingStrategy(strategy_str)
    except ValueError:
        logger.warning("Unknown routing strategy, defaulting to EXPLICIT", strategy=strategy_str)
        strategy = RoutingStrategy.EXPLICIT

    # For explicit: use the requested model.
    # For other strategies: the router returns a priority list; pick the first.
    if strategy == RoutingStrategy.EXPLICIT:
        selected = explicit_model
    else:
        config_list = ModelRouter.route(strategy=strategy)
        selected = config_list[0].model_name if config_list else settings.DEFAULT_MODEL

    logger.info("Graph: router_node selected", model=selected, strategy=strategy_str)

    return {
        **state,
        "selected_model_id": selected,
        "metadata": {
            **state.get("metadata", {}),
            "routing_strategy": strategy_str,
            "selected_model": selected,
        },
    }
