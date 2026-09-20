"""Converters between workflow working types and API schemas."""

from __future__ import annotations

from app.agents.state import WorkingEvent
from app.domains import DOMAIN_LABELS, Domain, RelevanceTier
from app.schemas.news import (
    ArticleOut,
    EventOut,
    ImpactOut,
    InsightOut,
)


def article_to_schema(article) -> ArticleOut:
    """Map a WorkingArticle to ArticleOut, preserving transparency (§14)."""
    raw = article.raw
    return ArticleOut(
        title=raw.title,
        url=raw.url,
        source_name=raw.source_name,
        ai_summary=article.summary,
        published_at=raw.published_at,
        retrieved_at=raw.retrieved_at,
        search_query=raw.query,
    )


def event_to_schema(event: WorkingEvent) -> EventOut:
    """Map a WorkingEvent to EventOut."""
    insight = None
    if event.what_happened or event.ai_analysis or event.impacts:
        insight = InsightOut(
            what_happened=event.what_happened,
            ai_analysis=event.ai_analysis,
            portfolio_relevance=event.portfolio_relevance,
            finance_tier=event.finance_tier,
            impacts=[
                ImpactOut(
                    holding_symbol=i.holding_symbol,
                    impact_type=i.impact_type,
                    rationale=i.rationale,
                )
                for i in event.impacts
            ],
        )
    return EventOut(
        title=event.title,
        summary=event.summary,
        category=event.domain.value,
        why_it_matters=event.why_it_matters,
        relevance_tier=RelevanceTier(event.relevance_tier),
        entities=event.entities,
        verified=event.verified,
        event_time=event.event_time,
        sources=[article_to_schema(a) for a in event.articles],
        insight=insight,
    )


def domain_label(domain_value: str) -> str:
    """Human label for a domain key."""
    try:
        return DOMAIN_LABELS[Domain(domain_value)]
    except (ValueError, KeyError):
        return domain_value.title()
