"""AI chat API schemas (§23)."""

from pydantic import BaseModel, Field

from app.schemas.news import ArticleOut


class ChatMessage(BaseModel):
    """A single chat turn."""

    role: str  # user / assistant
    content: str


class ChatRequest(BaseModel):
    """Ask AOEN a question, optionally scoped to an event (§23, §28)."""

    message: str = Field(..., min_length=1)
    history: list[ChatMessage] = []
    event_id: str | None = None  # reuse already-retrieved context (§28)


class ChatResponse(BaseModel):
    """AOEN's answer with clickable sources (§23)."""

    answer: str
    sources: list[ArticleOut] = []
    used_web_search: bool = False
