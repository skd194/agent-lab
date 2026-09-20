"""Portfolio API schemas (§4, §6, §25)."""

from typing import Literal

from pydantic import BaseModel, Field

Priority = Literal["HIGH", "MEDIUM", "LOW"]


class HoldingBase(BaseModel):
    """Common holding fields."""

    symbol: str = Field(..., min_length=1, max_length=32)
    name: str = Field(..., min_length=1, max_length=160)
    exchange: str = Field(default="NSE", max_length=16)
    sector: str | None = None
    quantity: float = Field(..., ge=0)
    average_price: float = Field(..., ge=0)
    priority: Priority = "MEDIUM"
    news_monitoring: bool = True


class HoldingCreate(HoldingBase):
    """Payload to add a holding (§25)."""


class HoldingUpdate(BaseModel):
    """Partial update for a holding."""

    symbol: str | None = None
    name: str | None = None
    exchange: str | None = None
    sector: str | None = None
    quantity: float | None = Field(default=None, ge=0)
    average_price: float | None = Field(default=None, ge=0)
    priority: Priority | None = None
    news_monitoring: bool | None = None


class HoldingOut(HoldingBase):
    """Holding with computed intelligence-terminal metrics (§6)."""

    id: str
    last_price: float | None = None
    day_change_pct: float | None = None
    invested_value: float = 0.0
    current_value: float = 0.0
    unrealized_pl: float = 0.0
    unrealized_pl_pct: float = 0.0
    day_change_value: float = 0.0
    news_count: int = 0

    model_config = {"from_attributes": True}


class PortfolioOverview(BaseModel):
    """Aggregate portfolio metrics (§6)."""

    total_invested: float = 0.0
    current_value: float = 0.0
    day_change_value: float = 0.0
    day_change_pct: float = 0.0
    overall_pl: float = 0.0
    overall_pl_pct: float = 0.0
    base_currency: str = "INR"
    holdings_count: int = 0


class PortfolioOut(BaseModel):
    """Full portfolio response (§6)."""

    id: str
    name: str
    base_currency: str
    overview: PortfolioOverview
    holdings: list[HoldingOut]
