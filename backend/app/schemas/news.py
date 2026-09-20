"""News API schemas (§13, §14, §15, §7)."""

from datetime import datetime

from pydantic import BaseModel

from app.domains import FinanceRelevanceTier, ImpactType, RelevanceTier


class ArticleOut(BaseModel):
    """A single source article with full transparency (§14)."""

    id: str | None = None
    title: str
    url: str
    source_name: str
    ai_summary: str | None = None
    published_at: datetime | None = None
    retrieved_at: datetime | None = None
    search_query: str | None = None

    model_config = {"from_attributes": True}


class ImpactOut(BaseModel):
    """Informational impact on a holding (§7). NOT investment advice."""

    holding_symbol: str
    impact_type: ImpactType
    rationale: str | None = None

    model_config = {"from_attributes": True}


class InsightOut(BaseModel):
    """AI analysis, clearly separating fact from interpretation (§7)."""

    what_happened: str | None = None  # FACT
    ai_analysis: str | None = None  # AI ANALYSIS
    portfolio_relevance: str | None = None  # PORTFOLIO RELEVANCE
    finance_tier: FinanceRelevanceTier | None = None
    impacts: list[ImpactOut] = []

    model_config = {"from_attributes": True}


class EventOut(BaseModel):
    """A deduplicated event with its sources and AI intelligence (§13, §15)."""

    id: str | None = None
    title: str
    summary: str | None = None
    category: str
    why_it_matters: str | None = None
    relevance_tier: RelevanceTier
    entities: list[str] = []
    verified: bool = True
    event_time: datetime | None = None
    sources: list[ArticleOut] = []
    insight: InsightOut | None = None

    @property
    def source_count(self) -> int:
        """Number of publishers reporting this event (§15)."""
        return len(self.sources)

    model_config = {"from_attributes": True}


class DomainSection(BaseModel):
    """A domain block with its events (§3, §12)."""

    domain: str
    label: str
    events: list[EventOut] = []
    total_available: int = 0
