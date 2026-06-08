from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any, Optional

class ProviderName(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    GROQ = "groq"
    OPENROUTER = "openrouter"
    CEREBRAS = "cerebras"

class ModelConfig(BaseModel):
    provider: ProviderName
    model_name: str
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    streaming: bool = False
    additional_kwargs: Dict[str, Any] = {}
# Refactored for performance polish — 2026-06-08T15:37:41
