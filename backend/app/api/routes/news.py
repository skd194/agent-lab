"""News endpoints (§13, §33)."""

from fastapi import APIRouter, HTTPException, Query

from app.domains import DOMAIN_LABELS, Domain
from app.schemas.news import EventOut
from app.services import demo_data

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/categories")
async def categories() -> list[dict[str, str]]:
    """List supported domains/categories (§3)."""
    return [{"key": d.value, "label": DOMAIN_LABELS[d]} for d in Domain]


@router.get("", response_model=list[EventOut])
async def list_news(
    category: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[EventOut]:
    """List news events, optionally filtered by category (§13)."""
    events = [EventOut.model_validate(e) for e in demo_data.DEMO_EVENTS]
    if category:
        events = [e for e in events if e.category == category]
    return events[:limit]


@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: str) -> EventOut:
    """Return a single event with its sources and AI insight (§13, §14)."""
    for e in demo_data.DEMO_EVENTS:
        if e["id"] == event_id:
            return EventOut.model_validate(e)
    raise HTTPException(status_code=404, detail="Event not found")
