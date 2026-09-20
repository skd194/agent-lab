"""News Summarization Agent (§10).

Produces concise event summaries and a short "why it matters" line. Uses the
LLM when available; otherwise falls back to a deterministic extractive summary
so the pipeline runs offline (§38).
"""

from __future__ import annotations

import re

from app.agents.llm import get_chat_model
from app.agents.state import WorkingEvent
from app.core.logging import get_logger
from app.domains import DOMAIN_LABELS

logger = get_logger(__name__)

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_MAX_LLM_EVENTS = 24  # cost guardrail per run


def _extractive_summary(event: WorkingEvent, max_sentences: int = 2) -> str:
    """Deterministic fallback: first informative sentences from best article."""
    if not event.articles:
        return event.title
    content = event.articles[0].raw.content or event.title
    sentences = [s.strip() for s in _SENTENCE_RE.split(content) if s.strip()]
    if not sentences:
        return event.title
    return " ".join(sentences[:max_sentences])


def _fallback_why(event: WorkingEvent) -> str:
    label = DOMAIN_LABELS.get(event.domain, "General")
    if event.source_count > 1:
        return f"Reported by {event.source_count} sources across {label}."
    return f"A notable development in {label}."


class NewsSummarizationAgent:
    """Summarises events into readable cards (§13)."""

    name = "summarization"

    def __init__(self) -> None:
        self._llm = get_chat_model()

    async def summarize(self, events: list[WorkingEvent]) -> list[WorkingEvent]:
        """Fill ``summary`` and ``why_it_matters`` for each event."""
        for event in events:
            if not event.summary:
                event.summary = _extractive_summary(event)
            if not event.why_it_matters:
                event.why_it_matters = _fallback_why(event)

        if self._llm is not None:
            await self._llm_enrich(events[:_MAX_LLM_EVENTS])

        return events

    async def _llm_enrich(self, events: list[WorkingEvent]) -> None:
        """Best-effort LLM refinement; failures keep the fallback text."""
        from langchain_core.messages import HumanMessage, SystemMessage

        system = SystemMessage(
            content=(
                "You are AOEN, a precise intelligence analyst. Summarise the "
                "news item in 2 concise factual sentences, then a one-line "
                "'why it matters'. Do not speculate or give investment advice. "
                "Respond as: SUMMARY: <...>\nWHY: <...>"
            )
        )
        for event in events:
            source = event.articles[0].raw if event.articles else None
            body = source.content if source else event.title
            try:
                resp = await self._llm.ainvoke(
                    [system, HumanMessage(content=f"{event.title}\n\n{body}")]
                )
                summary, why = self._parse(str(resp.content))
                if summary:
                    event.summary = summary
                if why:
                    event.why_it_matters = why
            except Exception as exc:  # noqa: BLE001 - keep fallback
                logger.warning("summarize_llm_failed", error=str(exc))

    @staticmethod
    def _parse(text: str) -> tuple[str | None, str | None]:
        summary = why = None
        for line in text.splitlines():
            if line.upper().startswith("SUMMARY:"):
                summary = line.split(":", 1)[1].strip()
            elif line.upper().startswith("WHY:"):
                why = line.split(":", 1)[1].strip()
        return summary, why
