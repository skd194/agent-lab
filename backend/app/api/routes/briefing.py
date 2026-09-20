"""Daily briefing endpoints (§12, §33)."""

from fastapi import APIRouter, Query

from app.schemas.briefing import DailyBriefingOut
from app.services.briefing_service import briefing_service
from app.services.demo_store import demo_store

router = APIRouter(prefix="/briefing", tags=["briefing"])


@router.get("/today", response_model=DailyBriefingOut)
async def briefing_today(
    window_hours: int = Query(default=24, ge=1, le=168),
    refresh: bool = Query(default=False),
) -> DailyBriefingOut:
    """Return today's briefing (§12), covering the selected window (§11)."""
    prefs = demo_store.get_preferences()
    holdings = demo_store.list_holdings()
    return await briefing_service.get_today(
        preferences=prefs,
        holdings=holdings,
        window_hours=window_hours,
        stories_per_domain=prefs.get("stories_per_domain", 5),
        force_refresh=refresh,
    )


@router.get("/history", response_model=list[DailyBriefingOut])
async def briefing_history() -> list[DailyBriefingOut]:
    """Return recent briefings (demo returns the current one)."""
    prefs = demo_store.get_preferences()
    holdings = demo_store.list_holdings()
    current = await briefing_service.get_today(preferences=prefs, holdings=holdings)
    return [current]
