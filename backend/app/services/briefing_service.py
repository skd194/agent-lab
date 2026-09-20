"""Briefing service (§12, §28, §38).

Produces the daily briefing either from curated demo data (offline) or by
running the live LangGraph workflow, with Redis caching to avoid repeated
expensive searches (§28).
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from app.agents.state import PipelineState
from app.core.config import settings
from app.core.logging import get_logger
from app.core.redis import cache_get_json, cache_set_json
from app.domains import Domain
from app.providers import get_news_provider
from app.schemas.briefing import (
    AgentStep,
    BriefingStats,
    DailyBriefingOut,
    TimeWindow,
)
from app.schemas.news import DomainSection, EventOut
from app.services import demo_data
from app.services.mappers import domain_label, event_to_schema
from app.workflows.news_workflow import build_news_workflow

logger = get_logger(__name__)

_TIER_ORDER = {"high": 0, "medium": 1, "low": 2}
_WINDOW_LABELS = {
    6: "Last 6 hours",
    12: "Last 12 hours",
    24: "Last 24 hours",
    48: "Last 48 hours",
}
_CACHE_TTL = 600


def _greeting(now: datetime) -> str:
    hour = now.hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


def _window(hours: int, now: datetime) -> TimeWindow:
    from datetime import timedelta

    return TimeWindow(
        start=now - timedelta(hours=hours),
        end=now,
        label=_WINDOW_LABELS.get(hours, f"Last {hours} hours"),
    )


def _sort_key(event: EventOut):
    return (_TIER_ORDER.get(event.relevance_tier.value, 3),)


class BriefingService:
    """Builds daily briefings."""

    async def get_today(
        self,
        *,
        preferences: dict,
        holdings: list[dict],
        window_hours: int = 24,
        stories_per_domain: int = 5,
        force_refresh: bool = False,
    ) -> DailyBriefingOut:
        """Return today's briefing (demo or live), using cache when possible."""
        cache_key = self._cache_key(preferences, holdings, window_hours)
        if not force_refresh:
            cached = await cache_get_json(cache_key)
            if cached:
                logger.info("briefing_cache_hit", key=cache_key)
                return DailyBriefingOut.model_validate(cached)

        if settings.has_live_search:
            briefing = await self._build_live(
                preferences, holdings, window_hours, stories_per_domain
            )
        else:
            briefing = self._build_demo(
                preferences, holdings, window_hours, stories_per_domain
            )

        await cache_set_json(
            cache_key, briefing.model_dump(mode="json"), ttl_seconds=_CACHE_TTL
        )
        return briefing

    # -- Demo path -----------------------------------------------------------
    def _build_demo(
        self,
        preferences: dict,
        holdings: list[dict],
        window_hours: int,
        stories_per_domain: int,
    ) -> DailyBriefingOut:
        now = datetime.now(UTC)
        events = [EventOut.model_validate(e) for e in demo_data.DEMO_EVENTS]
        return self._assemble(
            events,
            preferences=preferences,
            now=now,
            window_hours=window_hours,
            stories_per_domain=stories_per_domain,
            provider="demo",
            degraded=False,
            activity=self._demo_activity(len(events)),
        )

    @staticmethod
    def _demo_activity(event_count: int) -> list[AgentStep]:
        return [
            AgentStep(agent="preferences", message="Loaded preferences"),
            AgentStep(agent="portfolio", message="Loaded portfolio"),
            AgentStep(agent="query_planning", message="Generated 28 search queries"),
            AgentStep(agent="discovery", message="Searched 31 sources", item_count=87),
            AgentStep(
                agent="deduplication",
                message=f"Deduplicated to {event_count} events",
                item_count=event_count,
            ),
            AgentStep(agent="summarization", message="Generated summaries"),
            AgentStep(
                agent="finance_relevance", message="Analysed portfolio relevance"
            ),
            AgentStep(agent="ranking", message="Ranked stories"),
            AgentStep(agent="daily_briefing", message="Generated briefing"),
        ]

    # -- Live path -----------------------------------------------------------
    async def _build_live(
        self,
        preferences: dict,
        holdings: list[dict],
        window_hours: int,
        stories_per_domain: int,
    ) -> DailyBriefingOut:
        provider = get_news_provider()
        run = build_news_workflow(provider)
        time_range = "day" if window_hours <= 24 else "week"
        initial: PipelineState = {
            "preferences": preferences,
            "holdings": holdings,
            "stories_per_domain": stories_per_domain,
            "max_results": max(3, stories_per_domain),
            "time_range": time_range,
            "activity": [],
        }
        final = await run(initial)
        events = [event_to_schema(e) for e in final.get("events", [])]
        activity = [
            AgentStep(
                agent=step["agent"],
                message=step["message"],
                status=step.get("status", "ok"),
                duration_ms=step.get("duration_ms"),
                item_count=step.get("item_count"),
            )
            for step in final.get("activity", [])
        ]
        now = datetime.now(UTC)
        return self._assemble(
            events,
            preferences=preferences,
            now=now,
            window_hours=window_hours,
            stories_per_domain=stories_per_domain,
            provider=final.get("provider", provider.name),
            degraded=final.get("degraded", False),
            activity=activity,
        )

    # -- Shared assembly -----------------------------------------------------
    def _assemble(
        self,
        events: list[EventOut],
        *,
        preferences: dict,
        now: datetime,
        window_hours: int,
        stories_per_domain: int,
        provider: str,
        degraded: bool,
        activity: list[AgentStep],
    ) -> DailyBriefingOut:
        ranked = sorted(events, key=_sort_key)
        finance = [e for e in ranked if e.category == Domain.FINANCE.value]

        preferred = preferences.get("preferred_domains", [])
        sections: list[DomainSection] = []
        domain_counts: dict[str, int] = {}
        for key in preferred:
            if key == Domain.FINANCE.value:
                continue
            domain_events = [e for e in ranked if e.category == key]
            domain_counts[key] = len(domain_events)
            sections.append(
                DomainSection(
                    domain=key,
                    label=domain_label(key),
                    events=domain_events[:stories_per_domain],
                    total_available=len(domain_events),
                )
            )
        domain_counts[Domain.FINANCE.value] = len(finance)

        portfolio_events = sum(
            1
            for e in finance
            if e.insight
            and e.insight.finance_tier
            and e.insight.finance_tier.value in ("direct_holding", "sector")
        )

        headline = (
            f"{len(ranked)} significant developments detected. "
            f"{portfolio_events} directly relevant to your portfolio."
        )
        notice = None
        if degraded:
            notice = (
                "Some sources are temporarily unavailable. Showing the latest "
                "verified information available."
            )

        return DailyBriefingOut(
            greeting=_greeting(now),
            headline=headline,
            generated_at=now,
            window=_window(window_hours, now),
            stats=BriefingStats(
                total_events=len(ranked),
                portfolio_events=portfolio_events,
                domain_counts=domain_counts,
            ),
            top_priorities=ranked[:5],
            finance=finance[: max(stories_per_domain, 5)],
            sections=sections,
            activity=activity,
            provider=provider,
            degraded=degraded,
            notice=notice,
        )

    @staticmethod
    def _cache_key(preferences: dict, holdings: list[dict], window_hours: int) -> str:
        basis = {
            "domains": preferences.get("preferred_domains", []),
            "spd": preferences.get("stories_per_domain", 5),
            "symbols": sorted(h.get("symbol", "") for h in holdings),
            "w": window_hours,
            "day": datetime.now(UTC).strftime("%Y-%m-%d-%H"),
        }
        digest = hashlib.sha256(str(basis).encode()).hexdigest()[:16]
        return f"aoen:briefing:{digest}"


briefing_service = BriefingService()
