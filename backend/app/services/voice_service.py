"""Voice command routing (§21).

Maps a transcript to an intent + arguments. The command system is extensible:
add a pattern to ``_ROUTES``. Actual STT/TTS runs client-side in the browser in
demo mode (§22); the server provides routing and optional server-side TTS.
"""

from __future__ import annotations

import re

from app.schemas.voice import VoiceCommandResult

# Ordered (regex, intent) rules (§21). First match wins.
_ROUTES: list[tuple[str, str]] = [
    (r"\bgood (morning|afternoon|evening)\b", "greeting"),
    (r"\bbrief me\b|\bbriefing\b|\bbrief\b", "full_briefing"),
    (r"\bfinance\b|\bportfolio\b", "finance_briefing"),
    (r"\btechnology\b|\btech\b", "domain_technology"),
    (r"\bindia\b", "domain_india"),
    (r"\bworld\b|\binternational\b", "domain_international"),
    (r"\btop (three|3)\b", "top_stories"),
    (r"\bexplain\b|\bwhy does this matter\b|\bwhy\b", "explain"),
    (r"\btell me more\b|\bmore\b", "more"),
    (r"\bskip\b", "skip"),
    (r"\bgo back\b|\bback\b", "back"),
    (r"\btwo minutes\b|\bsummari[sz]e everything\b", "summary_2min"),
    (r"\bwhat'?s happening with (.+)", "entity_query"),
]

_SPOKEN = {
    "greeting": "Good to see you. I found new developments since your last briefing.",
    "full_briefing": "Starting your briefing. Here are the top priorities.",
    "finance_briefing": "Here's your finance briefing, ranked by portfolio relevance.",
    "domain_technology": "Here's what changed in technology.",
    "domain_india": "Here's what changed in India.",
    "domain_international": "Here are the top international developments.",
    "top_stories": "Here are your top three stories.",
    "explain": "Here's the background and why it matters.",
    "more": "Here's more detail on that story.",
    "skip": "Skipping to the next item.",
    "back": "Going back to the previous item.",
    "summary_2min": "Here's everything in about two minutes.",
    "entity_query": "Here's the latest on that.",
    "unknown": "I didn't catch a command. Try 'brief me' or 'read my portfolio news'.",
}


class VoiceService:
    """Routes voice transcripts to intents (§21)."""

    def route(self, transcript: str) -> VoiceCommandResult:
        """Return the matched intent, args and a spoken response."""
        text = transcript.lower().strip()
        for pattern, intent in _ROUTES:
            match = re.search(pattern, text)
            if match:
                args = {}
                if intent == "entity_query" and match.groups():
                    args["entity"] = match.group(1).strip()
                return VoiceCommandResult(
                    intent=intent,
                    args=args,
                    spoken_response=_SPOKEN.get(intent, _SPOKEN["unknown"]),
                )
        return VoiceCommandResult(
            intent="unknown", args={}, spoken_response=_SPOKEN["unknown"]
        )


voice_service = VoiceService()
