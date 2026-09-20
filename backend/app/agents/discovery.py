"""News Discovery Agent (§10).

Executes the planned queries against the active :class:`NewsSearchProvider`
and returns enriched working articles. Query failures are tolerated and surface
as a ``degraded`` flag rather than aborting the briefing (§39).
"""

from __future__ import annotations

from app.agents.state import PlannedQuery, WorkingArticle
from app.core.logging import get_logger
from app.providers.base import NewsSearchProvider

logger = get_logger(__name__)


class NewsDiscoveryAgent:
    """Finds relevant current information via the search provider."""

    name = "discovery"

    def __init__(self, provider: NewsSearchProvider) -> None:
        self._provider = provider

    async def discover(
        self,
        queries: list[PlannedQuery],
        *,
        max_results: int = 5,
        time_range: str | None = None,
    ) -> tuple[list[WorkingArticle], bool]:
        """Run all searches; return (articles, degraded)."""
        query_strings = [pq.query for pq in queries]
        results = await self._provider.search_many(
            query_strings, max_results=max_results, time_range=time_range
        )
        by_query = {pq.query: pq for pq in queries}

        articles: list[WorkingArticle] = []
        failures = 0
        for result in results:
            if not result.ok:
                failures += 1
                continue
            planned = by_query.get(result.query)
            domain = planned.domain if planned else None
            for raw in result.articles:
                articles.append(
                    WorkingArticle(
                        raw=raw,
                        domain=domain or WorkingArticle(raw=raw).domain,
                    )
                )

        degraded = failures > 0
        logger.info(
            "discovery_complete",
            queries=len(queries),
            articles=len(articles),
            failures=failures,
        )
        return articles, degraded
