"""
app/graph/workflow.py — LangGraph Execution Pipeline

Complete workflow:

  input_validation
       ↓ (blocked → END)
  prompt_render
       ↓
  router
       ↓
  llm_call
       ↓
  output_validation
       ↓ (validation errors → retry_node → llm_call)
       ↓ (max retries exceeded → END with error)
  persist
       ↓
  END

All async nodes receive a db: AsyncSession injected at compile time via
functools.partial. This keeps the graph stateless and testable.
"""
import functools
import structlog
from typing import Literal

from langgraph.graph import StateGraph, END
from sqlalchemy.ext.asyncio import AsyncSession

from app.graph.state import ChatState
from app.graph.nodes.input import input_validation_node
from app.graph.nodes.prompt import prompt_render_node
from app.graph.nodes.router import router_node
from app.graph.nodes.llm import llm_node
from app.graph.nodes.output import output_validation_node
from app.graph.nodes.retry import retry_node
from app.graph.nodes.persist import persist_node
from app.graph.nodes.analytics import token_tracking_node, usage_analytics_node
from app.graph.nodes.experiments import experiment_logging_node
from app.graph.nodes.audit import audit_logging_node
from app.graph.nodes.background import celery_trigger_node

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Conditional edge functions
# ---------------------------------------------------------------------------

def _after_input(state: ChatState) -> Literal["prompt_render", "end_error"]:
    if state.get("error"):
        logger.info("Graph: routing to end_error after input", error=state["error"])
        return "end_error"
    return "prompt_render"


def _after_output(state: ChatState) -> Literal["persist", "retry", "end_error"]:
    if state.get("error"):
        return "end_error"
    if state.get("validation_errors"):
        return "retry"
    return "persist"


def _after_retry(state: ChatState) -> Literal["llm_call", "end_error"]:
    if state.get("error"):
        return "end_error"
    return "llm_call"


def _after_llm(state: ChatState) -> Literal["output_validation", "end_error"]:
    if state.get("error"):
        return "end_error"
    return "output_validation"


# ---------------------------------------------------------------------------
# Graph factory — called once per request with bound db session
# ---------------------------------------------------------------------------

def build_graph(db: AsyncSession):
    """
    Compile and return a runnable LangGraph for one request lifecycle.
    Async nodes are wrapped with functools.partial to inject the db session.
    """
    graph = StateGraph(ChatState)

    # Register nodes (async nodes use partial to bind db)
    graph.add_node("input_validation", input_validation_node)
    graph.add_node("prompt_render", functools.partial(prompt_render_node, db=db))
    graph.add_node("router", router_node)
    graph.add_node("llm_call", llm_node)
    graph.add_node("output_validation", output_validation_node)
    graph.add_node("retry", retry_node)
    graph.add_node("persist", functools.partial(persist_node, db=db))
    graph.add_node("token_tracking", functools.partial(token_tracking_node, db=db))
    graph.add_node("usage_analytics", usage_analytics_node)
    graph.add_node("experiment_logging", experiment_logging_node)
    graph.add_node("audit_logging", functools.partial(audit_logging_node, db=db))
    graph.add_node("celery_trigger", celery_trigger_node)

    # Entry point
    graph.set_entry_point("input_validation")

    # Edges
    graph.add_conditional_edges("input_validation", _after_input)
    graph.add_edge("prompt_render", "router")
    graph.add_edge("router", "llm_call")
    graph.add_conditional_edges("llm_call", _after_llm)
    graph.add_conditional_edges("output_validation", _after_output)
    graph.add_conditional_edges("retry", _after_retry)
    graph.add_edge("persist", "token_tracking")
    graph.add_edge("token_tracking", "usage_analytics")
    graph.add_edge("usage_analytics", "experiment_logging")
    graph.add_edge("experiment_logging", "audit_logging")
    graph.add_edge("audit_logging", "celery_trigger")
    graph.add_edge("celery_trigger", END)

    # Error terminal
    graph.add_node("end_error", lambda s: s)  # pass-through; caller reads state.error
    graph.add_edge("end_error", END)

    return graph.compile()


# ---------------------------------------------------------------------------
# Convenience executor
# ---------------------------------------------------------------------------

async def run_chat_graph(initial_state: ChatState, db: AsyncSession) -> ChatState:
    """Execute the full LangGraph pipeline and return final state."""
    compiled = build_graph(db)
    final = await compiled.ainvoke(initial_state)
    return final
