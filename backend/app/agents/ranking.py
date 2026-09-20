"""News Ranking Agent (§16).

Combines several transparent components into an internal 0..1 score used only
for ordering, then maps it to an honest coarse tier (HIGH/MEDIUM/LOW). We never
expose fake precision like "93.27% important" (§16).
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.agents.state import WorkingEvent
from app.core.logging import get_logger
from app.domains import (
    Domain,
    FinanceRelevanceTier,
    relevance_tier_from_score,
)

logger = get_logger(__name__)

# Component weights (sum ~1.0). Tunable and intentionally explainable.
_W_RECENCY = 0.25
_W_SOURCES = 0.15
_W_PORTFOLIO = 0.35
_W_SEARCH = 0.15
_W_DOMAIN = 0.10

_DOMAIN_IMPORTANCE: dict[Domain, float] = {
    Domain.FINANCE: 1.0,
    Domain.TECHNOLOGY: 0.8,
    Domain.INTERNATIONAL: 0.8,
    Domain.INDIA: 0.75,
    Domain.BUSINESS: 0.7,
    Domain.SCIENCE: 0.65,
    Domain.EDUCATION: 0.5,
    Domain.SPORTS: 0.5,
    Domain.ENTERTAINMENT: 0.45,
    Domain.GENERAL: 0.5,
}

_FINANCE_TIER_WEIGHT: dict[FinanceRelevanceTier, float] = {
    FinanceRelevanceTier.DIRECT_HOLDING: 1.0,
    FinanceRelevanceTier.SECTOR: 0.7,
    FinanceRelevanceTier.MACRO: 0.5,
    FinanceRelevanceTier.GENERAL: 0.3,
}


def _recency_score(event_time: datetime | None) -> float:
    if not event_time:
        return 0.4
    now = datetime.now(UTC)
    if event_time.tzinfo is None:
        event_time = event_time.replace(tzinfo=UTC)
    hours = max(0.0, (now - event_time).total_seconds() / 3600.0)
    # 1.0 at 0h decaying to ~0 by 48h.
    return max(0.0, 1.0 - (hours / 48.0))


def _source_score(count: int, reliability: float) -> float:
    # More independent sources + higher reliability => higher confidence (§15).
    breadth = min(1.0, count / 3.0)
    return 0.5 * breadth + 0.5 * reliability


class NewsRankingAgent:
    """Scores and orders events (§16)."""

    name = "ranking"

    def rank(self, events: list[WorkingEvent]) -> list[WorkingEvent]:
        """Compute scores/tiers and return events sorted high→low."""
        for event in events:
            event.relevance_score = self._score(event)
            event.relevance_tier = relevance_tier_from_score(event.relevance_score)
        events.sort(key=lambda e: e.relevance_score, reverse=True)
        logger.info("ranking_complete", events=len(events))
        return events

    @staticmethod
    def _score(event: WorkingEvent) -> float:
        recency = _recency_score(event.event_time)

        avg_reliability = 0.7
        if event.articles:
            avg_reliability = sum(
                _SOURCE_RELIABILITY.get(a.raw.source_name, 0.7) for a in event.articles
            ) / len(event.articles)
        sources = _source_score(event.source_count, avg_reliability)

        if event.finance_tier is not None:
            portfolio = _FINANCE_TIER_WEIGHT.get(event.finance_tier, 0.3)
        else:
            portfolio = 0.2  # non-finance events have low direct portfolio link

        search = 0.0
        if event.articles:
            search = max(a.raw.score for a in event.articles)
            search = max(0.0, min(1.0, search))

        domain = _DOMAIN_IMPORTANCE.get(event.domain, 0.5)

        return (
            _W_RECENCY * recency
            + _W_SOURCES * sources
            + _W_PORTFOLIO * portfolio
            + _W_SEARCH * search
            + _W_DOMAIN * domain
        )


# Curated source reliability priors (§16). Unknown sources default to 0.7.
_SOURCE_RELIABILITY: dict[str, float] = {
    "reuters.com": 0.95,
    "bloomberg.com": 0.93,
    "ft.com": 0.92,
    "cnbc.com": 0.85,
    "livemint.com": 0.82,
    "economictimes.indiatimes.com": 0.8,
    "thehindu.com": 0.85,
    "moneycontrol.com": 0.8,
}
