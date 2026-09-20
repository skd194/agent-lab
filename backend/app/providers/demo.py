"""Demo news provider (§38).

Serves deterministic mock search hits so the entire app works with no API keys.
The richer curated briefing fixtures live in ``app.services.demo_data``; this
provider returns raw-article-shaped hits for any query so the *workflow itself*
can run end-to-end offline.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta

from app.providers.base import NewsSearchProvider, RawArticle, SearchResult

_DEMO_SOURCES = ["reuters.com", "bloomberg.com", "cnbc.com", "ft.com", "livemint.com"]


def _stable_int(text: str, mod: int) -> int:
    digest = hashlib.sha256(text.encode()).hexdigest()
    return int(digest[:8], 16) % mod


class DemoNewsProvider(NewsSearchProvider):
    """Offline provider returning plausible synthetic hits."""

    name = "demo"

    async def search(
        self,
        query: str,
        *,
        max_results: int = 5,
        time_range: str | None = None,
        **kwargs,
    ) -> SearchResult:
        now = datetime.now(UTC)
        count = min(max_results, 4)
        articles: list[RawArticle] = []
        for i in range(count):
            seed = f"{query}-{i}"
            source = _DEMO_SOURCES[_stable_int(seed, len(_DEMO_SOURCES))]
            hours_ago = _stable_int(seed, 23) + 1
            slug = query.lower().replace(" ", "-")[:48]
            articles.append(
                RawArticle(
                    title=f"{query.title()} — development {i + 1}",
                    url=f"https://{source}/news/{slug}-{i}",
                    content=(
                        f"[DEMO] Simulated coverage related to '{query}'. This "
                        "placeholder text stands in for real reporting so AOEN "
                        "can be explored without external API keys."
                    ),
                    source_name=source,
                    query=query,
                    score=1.0 - (i * 0.15),
                    published_at=now - timedelta(hours=hours_ago),
                    raw={"demo": True},
                )
            )
        return SearchResult(query=query, articles=articles, provider=self.name)
