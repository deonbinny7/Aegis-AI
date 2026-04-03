from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from app.config.settings import settings
from app.ai.providers.base import ProviderName, ModelConfig
from app.ai.providers.registry import get_model_config

class ProviderFactory:
    """
    Factory to instantiate standard LangChain Chat Models.
    Abstracts away the provider-specific initialization logic.
    """
    
    @staticmethod
    def create(model_id: str, **kwargs) -> BaseChatModel:
        config = get_model_config(model_id)
        
        # Override config with any dynamically provided kwargs
        temperature = kwargs.get("temperature", config.temperature)
        max_tokens = kwargs.get("max_tokens", config.max_tokens)
        streaming = kwargs.get("streaming", config.streaming)
        
        if config.provider == ProviderName.OPENAI:
            return ChatOpenAI(
                model=config.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=streaming,
                api_key=settings.OPENAI_API_KEY,
                **config.additional_kwargs
            )
        elif config.provider == ProviderName.ANTHROPIC:
            return ChatAnthropic(
                model=config.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=streaming,
                api_key=settings.ANTHROPIC_API_KEY,
                **config.additional_kwargs
            )
        elif config.provider == ProviderName.GEMINI:
            return ChatGoogleGenerativeAI(
                model=config.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=streaming,
                google_api_key=settings.GEMINI_API_KEY,
                **config.additional_kwargs
            )
        elif config.provider == ProviderName.GROQ:
            return ChatGroq(
                model=config.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=streaming,
                api_key=settings.GROQ_API_KEY,
                **config.additional_kwargs
            )
        elif config.provider == ProviderName.OPENROUTER:
            return ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                model=config.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=streaming,
                api_key=settings.OPENROUTER_API_KEY,
                default_headers={
                    "HTTP-Referer": "https://ai-gateway.local",
                    "X-Title": settings.APP_NAME,
                },
                **config.additional_kwargs
            )
        elif config.provider == ProviderName.CEREBRAS:
            return ChatOpenAI(
                base_url="https://api.cerebras.ai/v1",
                model=config.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=streaming,
                api_key=settings.CEREBRAS_API_KEY,
                **config.additional_kwargs
            )
        else:
            raise ValueError(f"Provider {config.provider} is not implemented in factory.")
