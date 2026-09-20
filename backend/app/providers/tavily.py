"""Tavily concrete news provider (§8).

Wraps the project's existing Tavily integration (``tavily_agent``) behind the
:class:`NewsSearchProvider` interface. Uses the raw ``TavilySearch`` tool for
structured hits (title/url/content/score/published date) which downstream
agents then normalize, deduplicate and summarize.
"""

from __future__ import annotations

import asyncio
from datetime import datetime

from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.logging import get_logger
from app.providers.base import NewsSearchProvider, RawArticle, SearchResult
from app.providers.tavily_agent import build_raw_tavily_tool

logger = get_logger(__name__)


def _parse_published(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        # Python 3.11+ parses a trailing "Z" natively.
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def _source_from_url(url: str) -> str:
    """Best-effort source name from a URL host."""
    try:
        host = url.split("//", 1)[-1].split("/", 1)[0]
        return host.replace("www.", "")
    except (IndexError, AttributeError):
        return "unknown"


class TavilyNewsProvider(NewsSearchProvider):
    """News provider backed by Tavily."""

    name = "tavily"

    def __init__(self, *, max_concurrency: int = 5) -> None:
        self._tool = None
        self._semaphore = asyncio.Semaphore(max_concurrency)

    def _get_tool(self):
        # Lazily build so importing never requires an API key.
        if self._tool is None:
            self._tool = build_raw_tavily_tool(topic="news")
        return self._tool

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        reraise=True,
    )
    async def _invoke(self, query: str, max_results: int, time_range: str | None):
        payload: dict = {"query": query, "max_results": max_results}
        if time_range:
            payload["time_range"] = time_range
        return await self._get_tool().ainvoke(payload)

    async def search(
        self,
        query: str,
        *,
        max_results: int = 5,
        time_range: str | None = None,
        **kwargs,
    ) -> SearchResult:
        async with self._semaphore:
            started = asyncio.get_event_loop().time()
            try:
                result = await self._invoke(query, max_results, time_range)
            except Exception as exc:  # noqa: BLE001 - surfaced as SearchResult error
                logger.warning("tavily_search_failed", query=query, error=str(exc))
                return SearchResult(
                    query=query, articles=[], provider=self.name, error=str(exc)
                )

            hits = result.get("results", []) if isinstance(result, dict) else []
            articles = [
                RawArticle(
                    title=hit.get("title", "").strip() or "Untitled",
                    url=hit.get("url", ""),
                    content=hit.get("content", ""),
                    source_name=_source_from_url(hit.get("url", "")),
                    query=query,
                    score=float(hit.get("score", 0.0) or 0.0),
                    published_at=_parse_published(hit.get("published_date")),
                    raw=hit,
                )
                for hit in hits
                if hit.get("url")
            ]
            duration_ms = int((asyncio.get_event_loop().time() - started) * 1000)
            logger.info(
                "tavily_search",
                query=query,
                results=len(articles),
                duration_ms=duration_ms,
            )
            return SearchResult(query=query, articles=articles, provider=self.name)

    async def search_many(
        self,
        queries: list[str],
        *,
        max_results: int = 5,
        time_range: str | None = None,
        **kwargs,
    ) -> list[SearchResult]:
        """Run searches concurrently (bounded by the semaphore)."""
        return await asyncio.gather(
            *(
                self.search(q, max_results=max_results, time_range=time_range, **kwargs)
                for q in queries
            )
        )
