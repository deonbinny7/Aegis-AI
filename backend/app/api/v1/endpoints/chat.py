"""
app/api/v1/endpoints/chat.py — /api/v1/chat non-streaming endpoint

Orchestrates the complete LangGraph pipeline:
  1. Parse and validate the request.
  2. Resolve or create the session.
  3. Build the initial ChatState.
  4. Run the LangGraph pipeline.
  5. Persist conversation (handled inside the graph).
  6. Return structured ChatResponse or ChatErrorResponse.
"""
import uuid
import time
import structlog
from structlog.contextvars import bind_contextvars
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ChatErrorResponse, UsageInfo
from app.graph.state import ChatState
from app.graph.workflow import run_chat_graph
from app.ai.memory import get_or_create_session
from app.config.settings import settings
from app.core.dependencies import OptionalCurrentUserDep

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        400: {"model": ChatErrorResponse},
        422: {"model": ChatErrorResponse},
        500: {"model": ChatErrorResponse},
    },
    summary="Chat Completion",
    description=(
        "Submit a conversation to the AI Gateway. The request is routed through the "
        "full LangGraph pipeline: validation → prompt rendering → memory → "
        "model routing → LLM call → output validation → persistence."
    ),
)
async def chat(
    request: ChatRequest,
    current_user: OptionalCurrentUserDep,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    request_id = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())
    
    current_user_id = current_user.username if current_user.username and current_user.username != "anonymous" else None

    bind_contextvars(
        request_id=request_id,
        trace_id=trace_id,
        correlation_id=correlation_id,
        user_id=current_user.username or "anonymous"
    )
    
    log = logger.bind()
    log.info("Chat request received", model=request.model, strategy=request.routing_strategy)
    
    start_time = time.time()

    # --- Resolve/create session ---
    try:
        session_id = await get_or_create_session(
            session_id=request.session_id,
            user_id=current_user_id,
            db=db,
        )
    except Exception as e:
        log.error("Session resolution failed", error=str(e))
        raise HTTPException(status_code=500, detail="Session resolution failed")

    # --- Build initial graph state ---
    initial_state: ChatState = {
        "request_id": request_id,
        "trace_id": trace_id,
        "correlation_id": correlation_id,
        "user_id": current_user.username or "anonymous",
        "session_id": session_id,
        "messages": [m.model_dump() for m in request.messages],
        "model_id": request.model or settings.DEFAULT_MODEL,
        "routing_strategy": request.routing_strategy,
        "prompt_name": request.prompt_name,
        "prompt_variables": request.prompt_variables,
        "output_schema": request.output_schema,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "retry_count": 0,
        "metadata": {"request_id": request_id},
    }

    # --- Execute graph ---
    try:
        final_state = await run_chat_graph(initial_state, db)
    except Exception as e:
        log.error("Graph execution failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Graph execution error: {e}")

    # --- Handle error state ---
    if final_state.get("error"):
        error_msg = final_state["error"]
        log.warning("Graph returned error state", error=error_msg)
        raise HTTPException(
            status_code=400,
            detail=ChatErrorResponse(
                request_id=request_id,
                error=error_msg,
                guardrail_violations=final_state.get("guardrail_violations", []),
                validation_errors=final_state.get("validation_errors", []),
                retry_count=final_state.get("retry_count", 0),
            ).model_dump(),
        )

    # --- Build success response ---
    usage_data = final_state.get("usage", {})
    response = ChatResponse(
        request_id=request_id,
        session_id=session_id,
        message=final_state.get("final_response", ""),
        model=final_state.get("metadata", {}).get("actual_model", settings.DEFAULT_MODEL),
        routing_strategy=request.routing_strategy,
        retry_count=final_state.get("retry_count", 0),
        prompt_version_id=final_state.get("prompt_version_id") or None,
        structured_output=final_state.get("structured_output"),
        usage=UsageInfo(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0),
        ),
        metadata={
            **final_state.get("metadata", {}),
            "trace_id": trace_id,
            "correlation_id": correlation_id,
            "execution_duration": time.time() - start_time
        },
    )

    log.info(
        "Chat request complete",
        model=response.model,
        retries=response.retry_count,
        tokens=usage_data.get("total_tokens", 0),
    )
# Refactored for performance polish — 2026-05-26T18:14:33
