"""News models (§26, §27).

Article and Event are deliberately separate (§27): many articles from different
publishers can describe the same real-world event, which powers deduplication
and multi-source display (§15).
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class NewsSource(Base):
    """A publisher/source (e.g. Reuters)."""

    __tablename__ = "news_sources"

    name: Mapped[str] = mapped_column(String(120), unique=True)
    domain: Mapped[str | None] = mapped_column(String(160), nullable=True)
    reliability: Mapped[float] = mapped_column(Float, default=0.7)  # 0..1 (§16)

    articles: Mapped[list[NewsArticle]] = relationship(back_populates="source")


class NewsCategory(Base):
    """A news domain/category (§3). Mirrors the Domain enum values."""

    __tablename__ = "news_categories"

    key: Mapped[str] = mapped_column(String(32), unique=True)
    label: Mapped[str] = mapped_column(String(80))


class NewsEvent(Base):
    """A real-world event, aggregating one or more articles (§15, §27)."""

    __tablename__ = "news_events"

    title: Mapped[str] = mapped_column(String(400))
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(32), default="general")
    # Coarse, honest relevance tier shown in UI (§16)
    relevance_tier: Mapped[str] = mapped_column(String(8), default="medium")
    # Internal numeric score used only for ranking (§16)
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0)
    why_it_matters: Mapped[str | None] = mapped_column(Text, nullable=True)
    entities: Mapped[list[str]] = mapped_column(JSON, default=list)
    verified: Mapped[bool] = mapped_column(default=True)  # §14 UNVERIFIED labelling
    event_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    articles: Mapped[list[NewsArticle]] = relationship(back_populates="event")
    insight: Mapped[NewsInsight | None] = relationship(
        back_populates="event", uselist=False, cascade="all, delete-orphan"
    )


class NewsArticle(Base):
    """A single article, preserving full source transparency (§14)."""

    __tablename__ = "news_articles"

    event_id: Mapped[str | None] = mapped_column(
        ForeignKey("news_events.id", ondelete="SET NULL"), nullable=True
    )
    source_id: Mapped[str | None] = mapped_column(
        ForeignKey("news_sources.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(400))
    url: Mapped[str] = mapped_column(String(1000))
    source_name: Mapped[str] = mapped_column(String(120))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(32), default="general")
    search_query: Mapped[str | None] = mapped_column(String(400), nullable=True)
    search_score: Mapped[float] = mapped_column(Float, default=0.0)
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    retrieved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    event: Mapped[NewsEvent | None] = relationship(back_populates="articles")
    source: Mapped[NewsSource | None] = relationship(back_populates="articles")


class NewsInsight(Base):
    """AI analysis for an event (§7): fact vs analysis vs portfolio relevance."""

    __tablename__ = "news_insights"

    event_id: Mapped[str] = mapped_column(
        ForeignKey("news_events.id", ondelete="CASCADE")
    )
    what_happened: Mapped[str | None] = mapped_column(Text, nullable=True)  # FACT
    ai_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)  # AI ANALYSIS
    portfolio_relevance: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Finance priority tier: direct_holding / sector / macro / general (§5)
    finance_tier: Mapped[str | None] = mapped_column(String(16), nullable=True)

    event: Mapped[NewsEvent] = relationship(back_populates="insight")
    impacts: Mapped[list[NewsImpact]] = relationship(
        back_populates="insight", cascade="all, delete-orphan"
    )


class NewsImpact(Base):
    """Informational impact on a specific holding (§7). NOT investment advice."""

    __tablename__ = "news_impacts"

    insight_id: Mapped[str] = mapped_column(
        ForeignKey("news_insights.id", ondelete="CASCADE")
    )
    holding_symbol: Mapped[str] = mapped_column(String(32))
    # positive / negative / neutral / mixed / watch (§7)
    impact_type: Mapped[str] = mapped_column(String(8), default="watch")
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)

    insight: Mapped[NewsInsight] = relationship(back_populates="impacts")
