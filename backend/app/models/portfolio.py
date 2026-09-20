"""Portfolio and holdings models (§4, §25, §26).

Nothing about specific stocks is hard-coded (§4); the portfolio is fully
user-configurable.
"""

from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Portfolio(Base):
    """A named collection of holdings belonging to a user."""

    __tablename__ = "portfolios"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120), default="My Portfolio")
    base_currency: Mapped[str] = mapped_column(String(3), default="INR")

    user: Mapped[User] = relationship(back_populates="portfolios")  # noqa: F821
    holdings: Mapped[list[PortfolioHolding]] = relationship(
        back_populates="portfolio", cascade="all, delete-orphan"
    )


class PortfolioHolding(Base):
    """A single security position (§4)."""

    __tablename__ = "portfolio_holdings"

    portfolio_id: Mapped[str] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE")
    )
    symbol: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(160))
    exchange: Mapped[str] = mapped_column(String(16), default="NSE")
    sector: Mapped[str | None] = mapped_column(String(80), nullable=True)
    quantity: Mapped[float] = mapped_column(Float, default=0.0)
    average_price: Mapped[float] = mapped_column(Float, default=0.0)
    # Priority: HIGH / MEDIUM / LOW (news prioritisation §5)
    priority: Mapped[str] = mapped_column(String(8), default="MEDIUM")
    news_monitoring: Mapped[bool] = mapped_column(Boolean, default=True)
    # Optional live-ish price snapshot (demo mode fills this in)
    last_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    day_change_pct: Mapped[float | None] = mapped_column(Float, nullable=True)

    portfolio: Mapped[Portfolio] = relationship(back_populates="holdings")
