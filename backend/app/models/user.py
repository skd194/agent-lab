"""User and preference models (§26).

Architecture supports multi-user later, but v1 can run single-user (§37).
"""

from __future__ import annotations

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.domains import DEFAULT_DOMAINS


class User(Base):
    """An AOEN user."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(120), default="User")
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)

    preference: Mapped[UserPreference | None] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    portfolios: Mapped[list["Portfolio"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )


class UserPreference(Base):
    """Per-user preferences (§24). No user-specific values hard-coded in logic."""

    __tablename__ = "user_preferences"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata")
    briefing_time: Mapped[str] = mapped_column(String(5), default="08:00")
    news_window_hours: Mapped[int] = mapped_column(Integer, default=24)
    stories_per_domain: Mapped[int] = mapped_column(Integer, default=5)
    voice_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    preferred_domains: Mapped[list[str]] = mapped_column(
        JSON, default=lambda: [d.value for d in DEFAULT_DOMAINS]
    )

    user: Mapped[User] = relationship(back_populates="preference")
