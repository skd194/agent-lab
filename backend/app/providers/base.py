"""News search provider abstraction (§8, §45).

The rest of AOEN depends on :class:`NewsSearchProvider` rather than directly on
Tavily, so a different search backend (or a local model) can be swapped in later
without touching the workflow or API layers.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class RawArticle:
    """A single raw search hit, before normalization/dedup/summarization.

    Preserves full source transparency (§14): original title, URL, source,
    publication time, the query that found it, and when we retrieved it.
    """

    title: str
    url: str
    content: str
    source_name: str
    query: str
    score: float = 0.0
    published_at: datetime | None = None
    retrieved_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    raw: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """JSON-serialisable representation (used for caching §28)."""
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "source_name": self.source_name,
            "query": self.query,
            "score": self.score,
            "published_at": (
                self.published_at.isoformat() if self.published_at else None
            ),
            "retrieved_at": self.retrieved_at.isoformat(),
        }


@dataclass(slots=True)
class SearchResult:
    """The result of a single provider search call."""

    query: str
    articles: list[RawArticle]
    provider: str
    error: str | None = None

    @property
    def ok(self) -> bool:
        """Whether the search succeeded (may still be empty)."""
        return self.error is None


class NewsSearchProvider(abc.ABC):
    """Abstract news search provider.

    Concrete implementations: :class:`app.providers.tavily.TavilyNewsProvider`
    (wraps the existing Tavily agent) and
    :class:`app.providers.demo.DemoNewsProvider` (offline mock data §38).
    """

    name: str = "base"

    @abc.abstractmethod
    async def search(
        self,
        query: str,
        *,
        max_results: int = 5,
        time_range: str | None = None,
        **kwargs,
    ) -> SearchResult:
        """Search for news matching ``query`` and return normalized raw hits."""

    async def search_many(
        self,
        queries: list[str],
        *,
        max_results: int = 5,
        time_range: str | None = None,
        **kwargs,
    ) -> list[SearchResult]:
        """Run several searches. Concrete providers may override for concurrency."""
        results: list[SearchResult] = []
        for query in queries:
            results.append(
                await self.search(
                    query,
                    max_results=max_results,
                    time_range=time_range,
                    **kwargs,
                )
            )
        return results

    async def close(self) -> None:  # pragma: no cover - optional lifecycle hook
        """Release any resources held by the provider."""
