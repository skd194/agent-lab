"""Daily briefing API schemas (§11, §12, §30)."""

from datetime import datetime

from pydantic import BaseModel

from app.schemas.news import DomainSection, EventOut


class TimeWindow(BaseModel):
    """The coverage window for a briefing (§11)."""

    start: datetime
    end: datetime
    label: str = "Last 24 hours"


class AgentStep(BaseModel):
    """One line in the AOEN activity panel (§30)."""

    agent: str
    message: str
    status: str = "ok"
    duration_ms: int | None = None
    item_count: int | None = None


class BriefingStats(BaseModel):
    """Headline counts shown in the intro (§2, §12)."""

    total_events: int = 0
    portfolio_events: int = 0
    domain_counts: dict[str, int] = {}


class DailyBriefingOut(BaseModel):
    """The complete daily briefing (§12)."""

    id: str | None = None
    greeting: str = "Good morning"
    headline: str | None = None
    generated_at: datetime
    last_briefing_at: datetime | None = None
    window: TimeWindow
    stats: BriefingStats
    top_priorities: list[EventOut] = []
    finance: list[EventOut] = []
    sections: list[DomainSection] = []
    activity: list[AgentStep] = []
    provider: str = "demo"
    degraded: bool = False  # true when some sources failed (§39)
    notice: str | None = None
