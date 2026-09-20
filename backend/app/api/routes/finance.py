"""Finance & portfolio endpoints (§4, §6, §25, §33)."""

from fastapi import APIRouter, HTTPException

from app.domains import Domain
from app.schemas.news import EventOut
from app.schemas.portfolio import (
    HoldingCreate,
    HoldingOut,
    HoldingUpdate,
    PortfolioOut,
)
from app.services import demo_data
from app.services.demo_store import demo_store
from app.services.portfolio_service import build_portfolio

router = APIRouter(prefix="/finance", tags=["finance"])


def _news_counts() -> dict[str, int]:
    """Count demo finance events referencing each holding symbol."""
    counts: dict[str, int] = {}
    for event in demo_data.DEMO_EVENTS:
        insight = event.get("insight") or {}
        for impact in insight.get("impacts", []):
            sym = impact.get("holding_symbol")
            if sym:
                counts[sym] = counts.get(sym, 0) + 1
    return counts


@router.get("/portfolio", response_model=PortfolioOut)
async def get_portfolio() -> PortfolioOut:
    """Return the portfolio with computed intelligence metrics (§6)."""
    return build_portfolio(demo_store.list_holdings(), news_counts=_news_counts())


@router.post("/portfolio", response_model=HoldingOut, status_code=201)
async def add_holding(payload: HoldingCreate) -> HoldingOut:
    """Add a holding (§25). Stocks are never hard-coded (§4)."""
    holding = demo_store.add_holding(payload.model_dump())
    from app.services.portfolio_service import compute_holding

    return compute_holding(holding)


@router.put("/portfolio/{holding_id}", response_model=HoldingOut)
async def update_holding(holding_id: str, payload: HoldingUpdate) -> HoldingOut:
    """Edit a holding (§25)."""
    updated = demo_store.update_holding(
        holding_id, payload.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Holding not found")
    from app.services.portfolio_service import compute_holding

    return compute_holding(updated)


@router.delete("/portfolio/{holding_id}", status_code=204)
async def delete_holding(holding_id: str) -> None:
    """Delete a holding (§25)."""
    if not demo_store.delete_holding(holding_id):
        raise HTTPException(status_code=404, detail="Holding not found")


@router.get("/news", response_model=list[EventOut])
async def finance_news() -> list[EventOut]:
    """Finance news ranked by portfolio relevance (§5)."""
    events = [
        EventOut.model_validate(e)
        for e in demo_data.DEMO_EVENTS
        if e["category"] == Domain.FINANCE.value
    ]
    tier_order = {"direct_holding": 0, "sector": 1, "macro": 2, "general": 3}
    events.sort(
        key=lambda e: tier_order.get(
            (
                e.insight.finance_tier.value
                if e.insight and e.insight.finance_tier
                else "general"
            ),
            3,
        )
    )
    return events
