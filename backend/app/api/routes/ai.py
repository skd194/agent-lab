"""Ask AOEN chat endpoint (§23, §33)."""

from fastapi import APIRouter

from app.schemas.ai import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    """Answer a question using retrieved news context (§23)."""
    return await chat_service.ask(payload)
