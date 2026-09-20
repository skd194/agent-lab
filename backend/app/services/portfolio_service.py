"""Portfolio computations (§6).

Pure functions that turn raw holdings (from demo data or the DB) into the
intelligence-terminal metrics shown on the finance dashboard.
"""

from __future__ import annotations

from typing import Any

from app.schemas.portfolio import (
    HoldingOut,
    PortfolioOut,
    PortfolioOverview,
)


def compute_holding(h: dict[str, Any], news_count: int = 0) -> HoldingOut:
    """Compute per-holding metrics (§6)."""
    qty = float(h.get("quantity", 0) or 0)
    avg = float(h.get("average_price", 0) or 0)
    last = h.get("last_price")
    last = float(last) if last is not None else avg
    day_pct = float(h.get("day_change_pct") or 0.0)

    invested = qty * avg
    current = qty * last
    unrealized = current - invested
    unrealized_pct = (unrealized / invested * 100) if invested else 0.0
    # Day change value derived from the day's percentage move.
    prev_close = last / (1 + day_pct / 100) if day_pct else last
    day_change_value = (last - prev_close) * qty

    return HoldingOut(
        id=h.get("id", h.get("symbol", "")),
        symbol=h["symbol"],
        name=h.get("name", h["symbol"]),
        exchange=h.get("exchange", "NSE"),
        sector=h.get("sector"),
        quantity=qty,
        average_price=avg,
        priority=h.get("priority", "MEDIUM"),
        news_monitoring=h.get("news_monitoring", True),
        last_price=last,
        day_change_pct=day_pct,
        invested_value=round(invested, 2),
        current_value=round(current, 2),
        unrealized_pl=round(unrealized, 2),
        unrealized_pl_pct=round(unrealized_pct, 2),
        day_change_value=round(day_change_value, 2),
        news_count=news_count,
    )


def build_portfolio(
    holdings: list[dict[str, Any]],
    *,
    portfolio_id: str = "demo-portfolio",
    name: str = "My Portfolio",
    base_currency: str = "INR",
    news_counts: dict[str, int] | None = None,
) -> PortfolioOut:
    """Assemble a full PortfolioOut with aggregate overview (§6)."""
    news_counts = news_counts or {}
    computed = [compute_holding(h, news_counts.get(h["symbol"], 0)) for h in holdings]

    total_invested = sum(h.invested_value for h in computed)
    current_value = sum(h.current_value for h in computed)
    day_change_value = sum(h.day_change_value for h in computed)
    overall_pl = current_value - total_invested
    prev_value = current_value - day_change_value

    overview = PortfolioOverview(
        total_invested=round(total_invested, 2),
        current_value=round(current_value, 2),
        day_change_value=round(day_change_value, 2),
        day_change_pct=round(
            (day_change_value / prev_value * 100) if prev_value else 0.0, 2
        ),
        overall_pl=round(overall_pl, 2),
        overall_pl_pct=round(
            (overall_pl / total_invested * 100) if total_invested else 0.0, 2
        ),
        base_currency=base_currency,
        holdings_count=len(computed),
    )
    return PortfolioOut(
        id=portfolio_id,
        name=name,
        base_currency=base_currency,
        overview=overview,
        holdings=computed,
    )
