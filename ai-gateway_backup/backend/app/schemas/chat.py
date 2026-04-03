"""
app/schemas/chat.py — Request and Response models for /api/v1/chat
"""
from typing import Any, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content text")


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(
        ..., min_length=1, description="Conversation messages"
    )
    session_id: Optional[str] = Field(
        None, description="Existing session ID for memory continuity"
    )
    model: Optional[str] = Field(
        None,
        description="Explicit model ID (e.g. 'llama3-70b-8192'). "
        "If omitted, routing_strategy is used.",
    )
    routing_strategy: str = Field(
        "explicit",
        description="One of: explicit | cheapest | fastest | smart",
    )
    prompt_name: Optional[str] = Field(
        None, description="Named Jinja2 prompt template to use"
    )
    prompt_variables: dict[str, Any] = Field(
        default_factory=dict,
        description="Variables injected into the Jinja2 prompt template",
    )
    output_schema: Optional[dict[str, Any]] = Field(
        None, description="JSON schema the response must conform to"
    )
    temperature: float = Field(0.0, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0)


class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatResponse(BaseModel):
    request_id: str
    session_id: str
    message: str = Field(..., description="Assistant response text")
    model: str = Field(..., description="Model that produced the response")
    routing_strategy: str
    retry_count: int = 0
    prompt_version_id: Optional[str] = None
    structured_output: Optional[dict[str, Any]] = None
    usage: UsageInfo
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatErrorResponse(BaseModel):
    request_id: str
    error: str
    guardrail_violations: list[str] = []
    validation_errors: list[str] = []
    retry_count: int = 0
