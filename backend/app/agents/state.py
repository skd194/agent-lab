"""Shared working types and LangGraph pipeline state (§9).

These in-memory structures carry data between agents during a workflow run.
They are richer than the persisted ORM models and are converted to API schemas
(or DB rows) once the pipeline completes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, TypedDict

from app.domains import (
    Domain,
    FinanceRelevanceTier,
    ImpactType,
    RelevanceTier,
)
from app.providers.base import RawArticle


@dataclass(slots=True)
class PlannedQuery:
    """A single planned search with the domain it targets (§10)."""

    query: str
    domain: Domain
    # For finance queries, the holding symbol this query was generated for.
    holding_symbol: str | None = None
    finance_tier: FinanceRelevanceTier | None = None


@dataclass(slots=True)
class WorkingArticle:
    """A raw article enriched with a domain classification and summary."""

    raw: RawArticle
    domain: Domain = Domain.GENERAL
    summary: str | None = None


@dataclass(slots=True)
class HoldingImpact:
    """Informational impact on a holding (§7). NOT investment advice."""

    holding_symbol: str
    impact_type: ImpactType = ImpactType.WATCH
    rationale: str | None = None


@dataclass(slots=True)
class WorkingEvent:
    """A deduplicated event aggregating one or more articles (§15, §27)."""

    title: str
    domain: Domain
    articles: list[WorkingArticle] = field(default_factory=list)
    summary: str | None = None
    why_it_matters: str | None = None
    entities: list[str] = field(default_factory=list)
    verified: bool = True
    event_time: datetime | None = None

    # Ranking (§16): internal score + coarse public tier.
    relevance_score: float = 0.0
    relevance_tier: RelevanceTier = RelevanceTier.MEDIUM

    # Finance intelligence (§5, §7).
    finance_tier: FinanceRelevanceTier | None = None
    what_happened: str | None = None
    ai_analysis: str | None = None
    portfolio_relevance: str | None = None
    impacts: list[HoldingImpact] = field(default_factory=list)

    @property
    def source_count(self) -> int:
        """Number of distinct articles/publishers for this event."""
        return len(self.articles)


class PipelineState(TypedDict, total=False):
    """LangGraph state threaded through the news workflow (§9)."""

    preferences: dict[str, Any]
    holdings: list[dict[str, Any]]
    window: dict[str, Any]
    queries: list[PlannedQuery]
    articles: list[WorkingArticle]
    events: list[WorkingEvent]
    briefing: dict[str, Any]
    activity: list[dict[str, Any]]
    degraded: bool
    provider: str
    stories_per_domain: int
    max_results: int
    time_range: str | None
