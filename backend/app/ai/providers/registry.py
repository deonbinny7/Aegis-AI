from typing import Dict
from app.ai.providers.base import ProviderName, ModelConfig

# Standardized model definitions for our router
AVAILABLE_MODELS: Dict[str, ModelConfig] = {
    # OpenAI
    "gpt-4o": ModelConfig(provider=ProviderName.OPENAI, model_name="gpt-4o"),
    "gpt-4o-mini": ModelConfig(provider=ProviderName.OPENAI, model_name="gpt-4o-mini"),
    
    # Anthropic
    "claude-3-5-sonnet-latest": ModelConfig(provider=ProviderName.ANTHROPIC, model_name="claude-3-5-sonnet-latest"),
    "claude-3-haiku-20240307": ModelConfig(provider=ProviderName.ANTHROPIC, model_name="claude-3-haiku-20240307"),
    
    # Gemini
    "gemini-1.5-pro": ModelConfig(provider=ProviderName.GEMINI, model_name="gemini-1.5-pro-latest"),
    "gemini-1.5-flash": ModelConfig(provider=ProviderName.GEMINI, model_name="gemini-1.5-flash-latest"),
    
    # Groq
    "llama3-70b-8192": ModelConfig(provider=ProviderName.GROQ, model_name="llama3-70b-8192"),
    "llama3-8b-8192": ModelConfig(provider=ProviderName.GROQ, model_name="llama3-8b-8192"),
    "mixtral-8x7b-32768": ModelConfig(provider=ProviderName.GROQ, model_name="mixtral-8x7b-32768"),

    # OpenRouter
    "openrouter/auto": ModelConfig(provider=ProviderName.OPENROUTER, model_name="openrouter/auto"),
    
    # Cerebras
    "llama3.1-70b": ModelConfig(provider=ProviderName.CEREBRAS, model_name="llama3.1-70b"),
}

def get_model_config(model_id: str) -> ModelConfig:
    if model_id not in AVAILABLE_MODELS:
        raise ValueError(f"Model {model_id} is not supported in the registry.")
    return AVAILABLE_MODELS[model_id]