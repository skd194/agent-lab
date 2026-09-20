"""Agent execution model (§26, §30, §51).

Records agent activity for the transparency panel and observability. Transient
agent state is not persisted permanently unless useful (§35).
"""

from __future__ import annotations

from sqlalchemy import JSON, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AgentExecution(Base):
    """A record of one agent/workflow step execution."""

    __tablename__ = "agent_executions"

    workflow: Mapped[str] = mapped_column(String(64), default="daily_briefing")
    agent: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(16), default="ok")  # ok / error
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)
