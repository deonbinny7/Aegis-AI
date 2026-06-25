import json
import structlog
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.db.session import get_db
from app.core.dependencies import CurrentUserDep
from app.schemas.chat import ChatRequest
from app.graph.state import ChatState
from app.graph.workflow import build_graph
from app.ai.memory import get_or_create_session
from app.config.settings import settings
import uuid
import time
from structlog.contextvars import bind_contextvars

router = APIRouter()
logger = structlog.get_logger(__name__)

async def _event_generator(request: ChatRequest, current_user: str, db: AsyncSession) -> AsyncGenerator[str, None]:
    request_id = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())
    
    bind_contextvars(
        request_id=request_id, 
        trace_id=trace_id, 
        correlation_id=correlation_id,
        user_id=current_user
    )
    
    logger.info("Chat stream request received")
    start_time = time.time()
    
    try:
        session_id = await get_or_create_session(
            session_id=request.session_id,
            user_id=current_user,
            db=db,
        )
    except Exception as e:
        yield f"data: {json.dumps({'error': 'Session resolution failed'})}\n\n"
        return

    initial_state: ChatState = {
        "request_id": request_id,
        "trace_id": trace_id,
        "correlation_id": correlation_id,
        "user_id": current_user,
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

    graph = build_graph(db)
    
    try:
        # We use astream_events to get granular token streams if the underlying LLM supports it
        async for event in graph.astream_events(initial_state, version="v1"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield f"data: {json.dumps({'token': content})}\n\n"
            elif kind == "on_chain_end" and event["name"] == "LangGraph":
                # Send the final state
                final_state = event["data"]["output"]
                meta = {
                    **final_state.get('metadata', {}),
                    "trace_id": trace_id,
                    "correlation_id": correlation_id,
                    "execution_duration": time.time() - start_time
                }
                yield f"data: {json.dumps({'status': 'completed', 'metadata': meta})}\n\n"
    except Exception as e:
        logger.error("Graph streaming failed", error=str(e))
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@router.post("")
async def chat_stream(
    request: ChatRequest,
    current_user: CurrentUserDep,
    db: AsyncSession = Depends(get_db)
):
    """Stream a chat response using Server-Sent Events (SSE)."""
    return StreamingResponse(
        _event_generator(request, current_user.username, db),
        media_type="text/event-stream"
    )
