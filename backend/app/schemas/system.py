"""System-level API schemas."""

from pydantic import BaseModel


class SystemStatus(BaseModel):
    """AOEN system status and capabilities."""

    name: str
    tagline: str
    version: str
    environment: str
    demo_mode: bool
    live_search: bool
    live_llm: bool
    status: str
