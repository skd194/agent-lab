"""User preference API schemas (§24)."""

from pydantic import BaseModel, Field

from app.domains import DEFAULT_DOMAINS


class PreferencesBase(BaseModel):
    """Editable user preferences."""

    name: str = "User"
    timezone: str = "Asia/Kolkata"
    briefing_time: str = Field(default="08:00", pattern=r"^\d{2}:\d{2}$")
    news_window_hours: int = Field(default=24, ge=1, le=168)
    stories_per_domain: int = Field(default=5, ge=1, le=20)
    voice_enabled: bool = True
    preferred_domains: list[str] = Field(
        default_factory=lambda: [d.value for d in DEFAULT_DOMAINS]
    )


class PreferencesUpdate(PreferencesBase):
    """Payload to update preferences (all fields optional via defaults)."""


class PreferencesOut(PreferencesBase):
    """Preferences returned to the client."""

    model_config = {"from_attributes": True}
