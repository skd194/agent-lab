"""Tests for providers and the end-to-end workflow (§50)."""

import pytest

from app.providers import get_news_provider
from app.providers.demo import DemoNewsProvider
from app.workflows.news_workflow import build_news_workflow


async def test_demo_provider_returns_articles():
    provider = DemoNewsProvider()
    result = await provider.search("steel prices india", max_results=4)
    assert result.ok
    assert len(result.articles) > 0
    assert all(a.url for a in result.articles)


def test_provider_selection_defaults_to_demo():
    # In demo mode (default), the offline provider is selected (§38).
    provider = get_news_provider()
    assert provider.name == "demo"


@pytest.mark.asyncio
async def test_workflow_runs_end_to_end_offline(holdings):
    run = build_news_workflow(get_news_provider())
    final = await run(
        {
            "preferences": {"preferred_domains": ["finance", "technology"]},
            "holdings": holdings,
            "stories_per_domain": 5,
            "max_results": 4,
            "activity": [],
        }
    )
    briefing = final["briefing"]
    assert briefing["stats"]["total_events"] > 0
    # Activity log has one step per agent (§30).
    assert len(briefing["activity"]) >= 8
    # Finance events were produced for the portfolio.
    assert isinstance(briefing["finance"], list)
