"""LangGraph news intelligence workflow (§9).

Wires the modular agents into a stateful pipeline:

    plan → discover → classify → dedup → summarize → finance → rank → briefing

Each node records a step in the activity log (§30) with timing (§51). The
whole graph runs offline in demo mode because every agent has a non-LLM path.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import Any

from langgraph.graph import END, START, StateGraph

from app.agents.briefing import DailyBriefingAgent
from app.agents.classification import NewsClassificationAgent
from app.agents.dedup import NewsDeduplicationAgent
from app.agents.discovery import NewsDiscoveryAgent
from app.agents.finance_relevance import FinanceRelevanceAgent
from app.agents.query_planning import QueryPlanningAgent
from app.agents.ranking import NewsRankingAgent
from app.agents.state import PipelineState
from app.agents.summarization import NewsSummarizationAgent
from app.core.logging import get_logger
from app.providers.base import NewsSearchProvider

logger = get_logger(__name__)


def _step(state: PipelineState, agent: str, message: str, started: float, **extra):
    """Append an activity step (§30) with elapsed time (§51)."""
    entry = {
        "agent": agent,
        "message": message,
        "status": "ok",
        "duration_ms": int((time.perf_counter() - started) * 1000),
        **extra,
    }
    state.setdefault("activity", []).append(entry)


def build_news_workflow(
    provider: NewsSearchProvider,
) -> Callable[[PipelineState], Awaitable[PipelineState]]:
    """Compile the LangGraph workflow bound to a search provider."""
    planner = QueryPlanningAgent()
    discovery = NewsDiscoveryAgent(provider)
    classifier = NewsClassificationAgent()
    deduper = NewsDeduplicationAgent()
    summarizer = NewsSummarizationAgent()
    finance = FinanceRelevanceAgent()
    ranker = NewsRankingAgent()
    briefer = DailyBriefingAgent()

    async def plan_node(state: PipelineState) -> dict[str, Any]:
        started = time.perf_counter()
        prefs = state.get("preferences", {})
        queries = planner.plan(
            prefs.get("preferred_domains", []), state.get("holdings", [])
        )
        _step(state, planner.name, f"Generated {len(queries)} search queries", started)
        return {"queries": queries, "activity": state["activity"]}

    async def discover_node(state: PipelineState) -> dict[str, Any]:
        started = time.perf_counter()
        articles, degraded = await discovery.discover(
            state.get("queries", []),
            max_results=state.get("max_results", 5),
            time_range=state.get("time_range"),
        )
        _step(
            state,
            discovery.name,
            f"Retrieved {len(articles)} articles from {provider.name}",
            started,
            item_count=len(articles),
        )
        return {
            "articles": articles,
            "degraded": degraded,
            "provider": provider.name,
            "activity": state["activity"],
        }

    async def classify_node(state: PipelineState) -> dict[str, Any]:
        started = time.perf_counter()
        articles = classifier.classify(state.get("articles", []))
        _step(state, classifier.name, f"Classified {len(articles)} articles", started)
        return {"articles": articles, "activity": state["activity"]}

    async def dedup_node(state: PipelineState) -> dict[str, Any]:
        started = time.perf_counter()
        events = deduper.deduplicate(state.get("articles", []))
        _step(
            state,
            deduper.name,
            f"Deduplicated to {len(events)} events",
            started,
            item_count=len(events),
        )
        return {"events": events, "activity": state["activity"]}

    async def summarize_node(state: PipelineState) -> dict[str, Any]:
        started = time.perf_counter()
        events = await summarizer.summarize(state.get("events", []))
        _step(state, summarizer.name, "Generated summaries", started)
        return {"events": events, "activity": state["activity"]}

    async def finance_node(state: PipelineState) -> dict[str, Any]:
        started = time.perf_counter()
        events = finance.analyze(state.get("events", []), state.get("holdings", []))
        _step(state, finance.name, "Analysed portfolio relevance", started)
        return {"events": events, "activity": state["activity"]}

    async def rank_node(state: PipelineState) -> dict[str, Any]:
        started = time.perf_counter()
        events = ranker.rank(state.get("events", []))
        _step(state, ranker.name, f"Ranked {len(events)} stories", started)
        return {"events": events, "activity": state["activity"]}

    async def briefing_node(state: PipelineState) -> dict[str, Any]:
        started = time.perf_counter()
        prefs = state.get("preferences", {})
        briefing = briefer.build(
            state.get("events", []),
            preferred_domains=prefs.get("preferred_domains", []),
            stories_per_domain=state.get("stories_per_domain", 5),
        )
        _step(state, briefer.name, "Generated briefing", started)
        briefing["activity"] = state["activity"]
        return {"briefing": briefing, "activity": state["activity"]}

    graph = StateGraph(PipelineState)
    graph.add_node("plan", plan_node)
    graph.add_node("discover", discover_node)
    graph.add_node("classify", classify_node)
    graph.add_node("dedup", dedup_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("finance", finance_node)
    graph.add_node("rank", rank_node)
    graph.add_node("briefing", briefing_node)

    graph.add_edge(START, "plan")
    graph.add_edge("plan", "discover")
    graph.add_edge("discover", "classify")
    graph.add_edge("classify", "dedup")
    graph.add_edge("dedup", "summarize")
    graph.add_edge("summarize", "finance")
    graph.add_edge("finance", "rank")
    graph.add_edge("rank", "briefing")
    graph.add_edge("briefing", END)

    compiled = graph.compile()

    async def run(initial: PipelineState) -> PipelineState:
        initial.setdefault("activity", [])
        return await compiled.ainvoke(initial)

    return run
