"""
app/graph/nodes/llm.py — LLM Invocation node

Responsibilities:
  1. Instantiate the chosen provider via ProviderFactory.
  2. Convert state messages to LangChain message objects.
  3. Invoke the model (with fallback handling).
  4. Extract usage metadata.
  5. Store raw response text in state.
"""
import time
import structlog
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage

from app.graph.state import ChatState
from app.ai.providers.factory import ProviderFactory
from app.ai.providers.registry import get_model_config
from app.ai.router import ModelRouter, RoutingStrategy
from app.config.settings import settings

logger = structlog.get_logger(__name__)


def _to_lc_messages(messages: list[dict]) -> list[BaseMessage]:
    """Convert plain dict messages to LangChain message objects."""
    result = []
    role_map = {
        "system": SystemMessage,
        "user": HumanMessage,
        "assistant": AIMessage,
    }
    for m in messages:
        cls = role_map.get(m["role"], HumanMessage)
        result.append(cls(content=m["content"]))
    return result


async def llm_node(state: ChatState) -> ChatState:
    """Async LLM invocation node with fallback support."""
    model_id = state.get("selected_model_id", settings.DEFAULT_MODEL)
    strategy_str = state.get("routing_strategy", settings.DEFAULT_ROUTING_STRATEGY)
    logger.info("Graph: llm_node", model=model_id)

    lc_messages = _to_lc_messages(state.get("messages", []))
    if not lc_messages:
        return {**state, "error": "No messages to send to model."}

    # Build fallback chain: primary model + tier fallbacks using ModelConfig list
    try:
        strategy = RoutingStrategy(strategy_str)
    except ValueError:
        strategy = RoutingStrategy.EXPLICIT

    if strategy == RoutingStrategy.EXPLICIT:
        configs = [get_model_config(model_id)]
    else:
        configs = ModelRouter.route(strategy=strategy)

    # Instantiate providers lazily from configs
    models_to_try = []
    for cfg in configs:
        try:
            models_to_try.append(ProviderFactory.create(cfg.model_name))
        except Exception:
            continue  # Skip providers with missing credentials gracefully

    if not models_to_try:
        return {**state, "error": "No providers available for selected routing strategy."}

    last_error = None
    t_start = time.perf_counter()

    for llm in models_to_try:
        try:
            response = await llm.ainvoke(lc_messages)
            latency_ms = int((time.perf_counter() - t_start) * 1000)

            # Extract usage
            usage = {}
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                um = response.usage_metadata
                usage = {
                    "prompt_tokens": getattr(um, "input_tokens", 0),
                    "completion_tokens": getattr(um, "output_tokens", 0),
                    "total_tokens": getattr(um, "total_tokens", 0),
                }

            # Identify which model actually ran
            actual_model = getattr(llm, "model_name", model_id) or model_id

            logger.info(
                "Graph: llm_node success",
                model=actual_model,
                latency_ms=latency_ms,
                **usage,
            )

            return {
                **state,
                "llm_response_raw": response.content,
                "usage": usage,
                "metadata": {
                    **state.get("metadata", {}),
                    "actual_model": actual_model,
                    "latency_ms": latency_ms,
                },
                "error": None,
            }
        except Exception as e:
            last_error = str(e)
            logger.warning("Graph: llm_node provider failed, trying next", error=last_error)
            continue

    # All providers failed
    logger.error("Graph: llm_node all providers exhausted", error=last_error)
    return {**state, "error": f"All providers failed: {last_error}"}
