"""Model-provider-agnostic LLM access (§45).

Business logic never imports a specific provider directly. It calls
:func:`get_chat_model`, which returns a LangChain chat model when a key is
configured, or ``None`` in demo mode. Every agent must therefore provide a
deterministic non-LLM fallback so the whole system runs offline (§38).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache
def get_chat_model(temperature: float | None = None) -> Any | None:
    """Return a LangChain chat model, or ``None`` when no LLM is available.

    Provider is selected from settings so a local model (e.g. Ollama) can be
    swapped in later without touching agents (§45).
    """
    if not settings.has_live_llm:
        return None

    temp = settings.llm_temperature if temperature is None else temperature
    provider = settings.llm_provider.lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.llm_model,
            temperature=temp,
            api_key=settings.effective_llm_key,
        )

    # Future: "ollama", "anthropic", etc. Fall back to no-LLM behaviour.
    logger.warning("llm_provider_unsupported", provider=provider)
    return None


def llm_available() -> bool:
    """Whether a live LLM is configured."""
    return get_chat_model() is not None
