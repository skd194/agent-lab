"""Application configuration.

All settings are read from environment variables (or a .env file) so that no
user-specific values or secrets are hard-coded into application logic (§24, §37).
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central AOEN configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Application ---
    app_name: str = "AOEN"
    app_tagline: str = "Personal Intelligence System"
    environment: Literal["development", "production", "test"] = "development"
    debug: bool = True
    api_prefix: str = "/api"

    # --- Demo mode (§38): entire app must work without API keys ---
    demo_mode: bool = Field(
        default=True,
        description="When true, AOEN serves mock news/portfolio/AI without external APIs.",
    )

    # --- Secrets (server-side only, never exposed to the browser §37) ---
    tavily_api_key: str | None = None
    llm_api_key: str | None = None  # e.g. OpenAI key
    openai_api_key: str | None = None  # honoured for backwards compatibility

    # --- LLM (model-provider agnostic §45) ---
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    llm_temperature: float = 0.0

    # --- Database (§35) ---
    database_url: str = "postgresql+asyncpg://aoen:aoen@localhost:5432/aoen"

    # --- Redis (§36) ---
    redis_url: str = "redis://localhost:6379/0"

    # --- CORS ---
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # --- Briefing defaults (§11, §24) ---
    default_news_window_hours: int = 24
    default_stories_per_domain: int = 5

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_cors(cls, value: object) -> object:
        """Allow CORS origins as a comma-separated string in env."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def effective_llm_key(self) -> str | None:
        """The LLM API key, honouring either LLM_API_KEY or OPENAI_API_KEY."""
        return self.llm_api_key or self.openai_api_key

    @property
    def has_live_search(self) -> bool:
        """Whether live Tavily search is possible."""
        return not self.demo_mode and bool(self.tavily_api_key)

    @property
    def has_live_llm(self) -> bool:
        """Whether a live LLM is configured."""
        return not self.demo_mode and bool(self.effective_llm_key)


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
