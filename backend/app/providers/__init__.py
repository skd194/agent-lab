"""Search provider package: abstraction + concrete implementations (§8)."""

from functools import lru_cache

from app.core.config import settings
from app.core.logging import get_logger
from app.providers.base import (
    NewsSearchProvider,
    RawArticle,
    SearchResult,
)
from app.providers.demo import DemoNewsProvider

logger = get_logger(__name__)

__all__ = [
    "NewsSearchProvider",
    "RawArticle",
    "SearchResult",
    "DemoNewsProvider",
    "get_news_provider",
]


@lru_cache
def get_news_provider() -> NewsSearchProvider:
    """Return the active news provider based on configuration (§38).

    Uses the live Tavily provider only when not in demo mode and a key is set;
    otherwise falls back to the offline demo provider.
    """
    if settings.has_live_search:
        # Imported lazily so demo mode never needs Tavily/LangChain installed keys.
        from app.providers.tavily import TavilyNewsProvider

        logger.info("news_provider_selected", provider="tavily")
        return TavilyNewsProvider()

    logger.info(
        "news_provider_selected",
        provider="demo",
        reason="demo_mode" if settings.demo_mode else "no_tavily_key",
    )
    return DemoNewsProvider()
