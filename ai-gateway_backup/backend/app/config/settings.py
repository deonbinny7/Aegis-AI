import os
import shutil
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Dynamically resolve the absolute path to the project root
# settings.py is in backend/app/config/ -> parents[3] is project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

ENV_FILE_PATH = PROJECT_ROOT / ".env"
ENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"

# Automatically generate .env from .env.example if it doesn't exist
if not ENV_FILE_PATH.exists() and ENV_EXAMPLE_PATH.exists():
    shutil.copy(ENV_EXAMPLE_PATH, ENV_FILE_PATH)

class Settings(BaseSettings):
    # Base
    APP_NAME: str = "Enterprise AI Gateway"
    DEBUG: bool = False
    LOGGING_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security (JWT)
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    TOKEN_EXPIRY: int = 1440 # 24 hours in minutes
    
    # API Keys for providers (optional, loaded from env)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    CEREBRAS_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # AI Core configuration
    DEFAULT_MODEL: str = "llama3-70b-8192"
    DEFAULT_ROUTING_STRATEGY: str = "explicit"
    MAX_RETRIES: int = 3
    MEMORY_WINDOW_SIZE: int = 20  # messages kept in Redis sliding window
    PROMPT_CACHE_TTL: int = 3600  # seconds
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def update_env_variables(self, updates: dict[str, Optional[str]]) -> None:
        update_env_file(updates)
        for key, value in updates.items():
            setattr(self, key, value)
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _serialize_env_value(value: Optional[str]) -> str:
    if value is None:
        return ""
    if "\n" in value:
        raise ValueError("Multiline environment values are not supported.")
    if any(ch in value for ch in [' ', '"', "'"]):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return value


def update_env_file(changes: dict[str, Optional[str]]) -> None:
    """Update the backend .env file with the provided key/value pairs."""
    if not ENV_FILE_PATH.exists():
        ENV_FILE_PATH.write_text("\n", encoding="utf-8")

    lines = ENV_FILE_PATH.read_text(encoding="utf-8").splitlines()
    remaining = set(changes.keys())
    output_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            output_lines.append(line)
            continue

        key, _ = line.split("=", 1)
        if key in changes:
            output_lines.append(f"{key}={_serialize_env_value(changes[key])}")
            remaining.discard(key)
        else:
            output_lines.append(line)

    for key in remaining:
        output_lines.append(f"{key}={_serialize_env_value(changes[key])}")
