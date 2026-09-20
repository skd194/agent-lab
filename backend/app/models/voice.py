"""Voice session model (§20, §26)."""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class VoiceSession(Base):
    """A voice interaction session (§20)."""

    __tablename__ = "voice_sessions"

    user_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    # idle / listening / thinking / speaking / error (§19)
    state: Mapped[str] = mapped_column(String(16), default="idle")
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    response: Mapped[str | None] = mapped_column(Text, nullable=True)
