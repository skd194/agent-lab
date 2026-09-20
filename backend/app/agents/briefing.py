"""Daily Briefing Agent (§12).

Assembles ranked events into the final briefing structure: top priorities, a
dedicated finance section, and per-domain sections limited to the user's
configured stories-per-domain.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.agents.state import WorkingEvent
from app.core.logging import get_logger
from app.domains import DEFAULT_DOMAINS, DOMAIN_LABELS, Domain

logger = get_logger(__name__)


def _greeting(now: datetime) -> str:
    hour = now.hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


class DailyBriefingAgent:
    """Builds the final briefing payload (§12)."""

    name = "daily_briefing"

    def build(
        self,
        events: list[WorkingEvent],
        *,
        preferred_domains: list[str],
        stories_per_domain: int,
        now: datetime | None = None,
    ) -> dict[str, Any]:
        """Return a structured briefing dict consumed by the service layer."""
        now = now or datetime.now(UTC)
        domains = self._resolve_domains(preferred_domains)

        finance_events = [e for e in events if e.domain is Domain.FINANCE]
        # Top priorities: highest-scoring across ALL domains (§12).
        top_priorities = events[: min(5, len(events))]

        sections: list[dict[str, Any]] = []
        domain_counts: dict[str, int] = {}
        for domain in domains:
            if domain is Domain.FINANCE:
                continue  # finance has its own dedicated section
            domain_events = [e for e in events if e.domain is domain]
            domain_counts[domain.value] = len(domain_events)
            sections.append(
                {
                    "domain": domain.value,
                    "label": DOMAIN_LABELS[domain],
                    "events": domain_events[:stories_per_domain],
                    "total_available": len(domain_events),
                }
            )

        portfolio_events = sum(
            1
            for e in finance_events
            if e.finance_tier and e.finance_tier.value in ("direct_holding", "sector")
        )
        domain_counts[Domain.FINANCE.value] = len(finance_events)

        headline = (
            f"{len(events)} significant developments detected. "
            f"{portfolio_events} directly relevant to your portfolio."
        )

        logger.info(
            "briefing_built",
            total=len(events),
            finance=len(finance_events),
            portfolio=portfolio_events,
        )
        return {
            "greeting": _greeting(now),
            "headline": headline,
            "generated_at": now,
            "top_priorities": top_priorities,
            "finance": finance_events[: max(stories_per_domain, 5)],
            "sections": sections,
            "stats": {
                "total_events": len(events),
                "portfolio_events": portfolio_events,
                "domain_counts": domain_counts,
            },
        }

    @staticmethod
    def _resolve_domains(preferred: list[str]) -> list[Domain]:
        resolved: list[Domain] = []
        for key in preferred or []:
            try:
                resolved.append(Domain(key))
            except ValueError:
                continue
        # Ensure finance is always considered even if not in preferences.
        if Domain.FINANCE not in resolved:
            resolved.insert(0, Domain.FINANCE)
        return resolved or list(DEFAULT_DOMAINS)
