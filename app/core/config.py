"""
Application configuration.

Reads all settings from environment variables (or a .env file) using
Pydantic BaseSettings.  This is the single source of truth for runtime
configuration.  No other module should read os.environ directly.

Usage:
    from app.core.config import settings

    api_key = settings.openai_api_key
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All runtime-configurable parameters.

    Fields are grouped by concern.  Every field documents its purpose and
    default value so the .env.example file can be generated from this class.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    app_name: str = Field(default="foundation-ai", description="Human-readable service name.")
    app_version: str = Field(default="0.1.0", description="Semantic version of the service.")
    environment: str = Field(
        default="development",
        description="Runtime environment: development | staging | production.",
    )
    debug: bool = Field(
        default=False,
        description="Enable verbose debug output.  Never True in production.",
    )

    # -------------------------------------------------------------------------
    # Server
    # -------------------------------------------------------------------------
    host: str = Field(default="0.0.0.0", description="Bind address for uvicorn.")
    port: int = Field(default=8000, description="Bind port for uvicorn.")
    workers: int = Field(
        default=1,
        description="Number of uvicorn worker processes.  Use 1 during development.",
    )

    # -------------------------------------------------------------------------
    # OpenAI provider
    # -------------------------------------------------------------------------
    openai_api_key: str = Field(
        description="OpenAI API key.  Required.  Never commit this value.",
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        description="Default model identifier sent to the OpenAI Chat Completions API.",
    )
    openai_timeout_seconds: int = Field(
        default=30,
        description="Hard timeout for OpenAI API calls in seconds.",
    )
    openai_max_retries: int = Field(
        default=2,
        description="Number of automatic retries on transient OpenAI errors.",
    )

    # -------------------------------------------------------------------------
    # Generation defaults
    # -------------------------------------------------------------------------
    default_temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature sent to the model.",
    )
    default_max_tokens: int = Field(
        default=1024,
        gt=0,
        description="Maximum tokens the model may generate per response.",
    )

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    log_level: str = Field(
        default="INFO",
        description="Python logging level: DEBUG | INFO | WARNING | ERROR | CRITICAL.",
    )
    log_json: bool = Field(
        default=False,
        description="Emit logs as JSON.  Set True in staging/production for log aggregators.",
    )

    # FUTURE UPGRADE:
    # Add database_url, redis_url, and vector_store_url fields here when those
    # infrastructure components are introduced.  Keeping them in Settings from
    # the start means zero restructuring is required — just uncomment and deploy.


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the singleton Settings instance.

    lru_cache ensures the .env file is parsed once per process lifetime.
    In tests, call get_settings.cache_clear() before patching env vars.
    """
    return Settings()


# Module-level convenience alias used throughout the application.
settings: Settings = get_settings()
