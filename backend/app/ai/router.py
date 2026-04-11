"""
app/ai/router.py — Model Router

Returns ordered lists of ModelConfig objects (lazy — no credentials needed).
The LLM node instantiates the actual provider at invocation time.
"""
from enum import Enum
from typing import List, Optional

from app.ai.providers.base import ModelConfig
from app.ai.providers.registry import AVAILABLE_MODELS, get_model_config
from app.config.settings import settings


class RoutingStrategy(str, Enum):
    EXPLICIT = "explicit"
    CHEAPEST = "cheapest"
    FASTEST = "fastest"
    SMART = "smart"


class ModelRouter:
    """
    Returns ordered ModelConfig lists. The first entry is primary, rest are fallbacks.
    Instantiation is deferred to the LLM node so credentials are only validated
    when a real API call is about to be made.
    """

    # Tiered routing: first = primary, rest = ordered fallbacks
    TIER_MAP = {
        RoutingStrategy.CHEAPEST: [
            "llama3-8b-8192",        # Groq — fastest + free tier
            "gemini-1.5-flash",      # Gemini flash — cheap
            "gpt-4o-mini",           # OpenAI mini
        ],
        RoutingStrategy.FASTEST: [
            "llama3-70b-8192",       # Groq — lowest latency
            "claude-3-haiku-20240307",
            "gemini-1.5-flash",
        ],
        RoutingStrategy.SMART: [
            "gpt-4o",
            "claude-3-5-sonnet-latest",
            "gemini-1.5-pro",
        ],
    }

    @classmethod
    def route(
        cls,
        strategy: RoutingStrategy = RoutingStrategy.EXPLICIT,
        explicit_model: Optional[str] = None,
    ) -> List[ModelConfig]:
        """Return an ordered list of ModelConfig for the given strategy."""
        if strategy == RoutingStrategy.EXPLICIT:
            if not explicit_model:
                raise ValueError("explicit_model must be provided for EXPLICIT routing")
            return [get_model_config(explicit_model)]

        model_ids = cls.TIER_MAP.get(strategy, [])
        if not model_ids:
            raise ValueError(f"Unknown routing strategy: {strategy}")

        configs = []
        for mid in model_ids:
            try:
                configs.append(get_model_config(mid))
            except ValueError:
                continue  # Skip unknown models gracefully
        return configs
