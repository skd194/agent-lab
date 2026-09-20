"""User preferences endpoints (§24)."""

from fastapi import APIRouter

from app.schemas.user import PreferencesOut, PreferencesUpdate
from app.services.demo_store import demo_store

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.get("", response_model=PreferencesOut)
async def get_preferences() -> PreferencesOut:
    """Return the current user's preferences."""
    return PreferencesOut(**demo_store.get_preferences())


@router.put("", response_model=PreferencesOut)
async def update_preferences(payload: PreferencesUpdate) -> PreferencesOut:
    """Update preferences (§24)."""
    updated = demo_store.update_preferences(payload.model_dump(exclude_unset=True))
    return PreferencesOut(**updated)
