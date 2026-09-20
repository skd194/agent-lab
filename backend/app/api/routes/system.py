"""System status endpoint (§33 GET /api/system/status)."""

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.system import SystemStatus

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status", response_model=SystemStatus)
async def system_status() -> SystemStatus:
    """Report AOEN system status and capability flags."""
    return SystemStatus(
        name=settings.app_name,
        tagline=settings.app_tagline,
        version="0.1.0",
        environment=settings.environment,
        demo_mode=settings.demo_mode,
        live_search=settings.has_live_search,
        live_llm=settings.has_live_llm,
        status="online",
    )
