"""Daily briefing models (§12, §26)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DailyBriefing(Base):
    """A generated briefing covering a time window (§11, §12)."""

    __tablename__ = "daily_briefings"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    greeting: Mapped[str] = mapped_column(String(120), default="Good morning")
    headline: Mapped[str | None] = mapped_column(Text, nullable=True)
    window_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    window_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    total_events: Mapped[int] = mapped_column(Integer, default=0)
    portfolio_events: Mapped[int] = mapped_column(Integer, default=0)

    items: Mapped[list[BriefingItem]] = relationship(
        back_populates="briefing", cascade="all, delete-orphan"
    )


class BriefingItem(Base):
    """One item within a briefing, linking to an event and its section (§12)."""

    __tablename__ = "briefing_items"

    briefing_id: Mapped[str] = mapped_column(
        ForeignKey("daily_briefings.id", ondelete="CASCADE")
    )
    event_id: Mapped[str | None] = mapped_column(
        ForeignKey("news_events.id", ondelete="SET NULL"), nullable=True
    )
    # Section: top_priority / finance / <domain> (§12)
    section: Mapped[str] = mapped_column(String(32), default="general")
    rank: Mapped[int] = mapped_column(Integer, default=0)

    briefing: Mapped[DailyBriefing] = relationship(back_populates="items")
