"""Ask AOEN chat service (§23).

Answers questions using retrieved news context. Reuses already-retrieved
events (§28) rather than searching again. Uses the LLM when available, else a
deterministic context-grounded response so demo mode still answers.
"""

from __future__ import annotations

from app.agents.llm import get_chat_model
from app.core.logging import get_logger
from app.schemas.ai import ChatRequest, ChatResponse
from app.schemas.news import ArticleOut, EventOut
from app.services import demo_data

logger = get_logger(__name__)


def _find_event(event_id: str | None) -> dict | None:
    if not event_id:
        return None
    return next((e for e in demo_data.DEMO_EVENTS if e["id"] == event_id), None)


def _context_sources(event: dict | None) -> list[ArticleOut]:
    if not event:
        return []
    return [ArticleOut.model_validate(s) for s in event.get("sources", [])]


class ChatService:
    """Handles Ask AOEN queries (§23)."""

    def __init__(self) -> None:
        self._llm = get_chat_model()

    async def ask(self, request: ChatRequest) -> ChatResponse:
        """Answer a question, grounded in event context when available."""
        event = _find_event(request.event_id)
        sources = _context_sources(event)

        if self._llm is not None:
            answer = await self._llm_answer(request, event)
        else:
            answer = self._demo_answer(request, event)

        return ChatResponse(answer=answer, sources=sources, used_web_search=False)

    async def _llm_answer(self, request: ChatRequest, event: dict | None) -> str:
        from langchain_core.messages import HumanMessage, SystemMessage

        context = ""
        if event:
            ev = EventOut.model_validate(event)
            context = (
                f"CONTEXT EVENT: {ev.title}\nSUMMARY: {ev.summary}\n"
                f"WHY IT MATTERS: {ev.why_it_matters}\n"
            )
        system = SystemMessage(
            content=(
                "You are AOEN, a personal intelligence officer. Answer concisely "
                "and factually using the provided context. Separate fact from "
                "interpretation. Never give buy/sell/hold investment advice."
            )
        )
        try:
            resp = await self._llm.ainvoke(
                [
                    system,
                    HumanMessage(content=f"{context}\nQUESTION: {request.message}"),
                ]
            )
            return str(resp.content).strip()
        except Exception as exc:  # noqa: BLE001 - fall back to demo answer
            logger.warning("chat_llm_failed", error=str(exc))
            return self._demo_answer(request, event)

    @staticmethod
    def _demo_answer(request: ChatRequest, event: dict | None) -> str:
        if event:
            ev = EventOut.model_validate(event)
            parts = [f"Here's what I have on “{ev.title}”.", ""]
            if ev.summary:
                parts.append(f"FACT: {ev.summary}")
            if ev.insight and ev.insight.ai_analysis:
                parts.append(f"AI ANALYSIS: {ev.insight.ai_analysis}")
            if ev.insight and ev.insight.portfolio_relevance:
                parts.append(f"PORTFOLIO RELEVANCE: {ev.insight.portfolio_relevance}")
            parts.append("")
            parts.append(
                "(Demo mode: connect an LLM key for free-form answers. This is "
                "informational only, not investment advice.)"
            )
            return "\n".join(parts)
        return (
            "I'm running in demo mode without a connected language model, so I "
            "can only summarise the curated briefing. Ask me about a specific "
            "story and I'll pull up its facts, analysis and portfolio relevance. "
            "This is informational only, not investment advice."
        )


chat_service = ChatService()
