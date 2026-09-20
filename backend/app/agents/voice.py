"""Voice Briefing Agent (§10, §20).

Converts a structured briefing into natural, conversational speech text that a
TTS engine (or the browser's SpeechSynthesis in demo mode) can read aloud.
"""

from __future__ import annotations

from typing import Any

from app.agents.state import WorkingEvent


class VoiceBriefingAgent:
    """Turns the briefing into spoken narration (§20)."""

    name = "voice_briefing"

    def narrate_intro(self, briefing: dict[str, Any]) -> str:
        """Short spoken intro, e.g. the JARVIS-style greeting (§2, §20)."""
        stats = briefing.get("stats", {})
        total = stats.get("total_events", 0)
        portfolio = stats.get("portfolio_events", 0)
        greeting = briefing.get("greeting", "Hello")
        return (
            f"{greeting}. I've analysed the latest developments and found "
            f"{total} significant {self._plural('item', total)}. "
            f"{portfolio} {self._are(portfolio)} directly related to your "
            "portfolio. Would you like the full briefing?"
        )

    def narrate_section(
        self, title: str, events: list[WorkingEvent], limit: int = 3
    ) -> str:
        """Narrate a section, leading with the most significant items."""
        if not events:
            return f"There's nothing notable in {title} right now."
        lines = [f"Here's {title}."]
        for event in events[:limit]:
            lead = event.summary or event.title
            lines.append(f"{event.title}. {lead}")
        return " ".join(lines)

    @staticmethod
    def _plural(word: str, count: int) -> str:
        return word if count == 1 else f"{word}s"

    @staticmethod
    def _are(count: int) -> str:
        return "is" if count == 1 else "are"
