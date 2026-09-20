"""Unit tests for the modular agents (§50)."""

from datetime import UTC, datetime

from app.agents.classification import NewsClassificationAgent
from app.agents.dedup import NewsDeduplicationAgent
from app.agents.finance_relevance import FinanceRelevanceAgent
from app.agents.query_planning import QueryPlanningAgent
from app.agents.ranking import NewsRankingAgent
from app.agents.state import WorkingArticle, WorkingEvent
from app.domains import Domain, FinanceRelevanceTier, ImpactType
from app.providers.base import RawArticle


def _raw(title: str, content: str = "", source: str = "reuters.com", query: str = "q"):
    return RawArticle(
        title=title,
        url=f"https://{source}/{abs(hash(title))}",
        content=content,
        source_name=source,
        query=query,
        score=0.9,
        published_at=datetime.now(UTC),
    )


def test_query_planning_generates_finance_tiers_from_holdings():
    planner = QueryPlanningAgent()
    holdings = [
        {
            "symbol": "TATASTEEL",
            "name": "Tata Steel",
            "sector": "Steel",
            "news_monitoring": True,
        }
    ]
    queries = planner.plan(["finance"], holdings)
    tiers = {q.finance_tier for q in queries}
    assert FinanceRelevanceTier.DIRECT_HOLDING in tiers
    assert FinanceRelevanceTier.SECTOR in tiers
    assert FinanceRelevanceTier.MACRO in tiers
    # The direct-holding query should mention the holding.
    assert any("Tata Steel" in q.query for q in queries)


def test_query_planning_skips_unmonitored_holdings():
    planner = QueryPlanningAgent()
    holdings = [{"symbol": "X", "name": "XCorp", "news_monitoring": False}]
    queries = planner.plan(["finance"], holdings)
    assert not any(
        q.finance_tier is FinanceRelevanceTier.DIRECT_HOLDING for q in queries
    )


def test_classification_infers_domain_from_keywords():
    classifier = NewsClassificationAgent()
    art = WorkingArticle(raw=_raw("Cricket series win for India", "wicket match"))
    art.domain = Domain.GENERAL
    [out] = classifier.classify([art])
    assert out.domain is Domain.SPORTS


def test_dedup_merges_similar_titles_into_one_event():
    deduper = NewsDeduplicationAgent()
    # Different publishers reporting the same event with strong token overlap
    # collapse into one multi-source event (§15); an unrelated story stays apart.
    arts = [
        WorkingArticle(
            raw=_raw(
                "RBI keeps repo rate unchanged in policy review", source="reuters.com"
            )
        ),
        WorkingArticle(
            raw=_raw(
                "RBI keeps repo rate unchanged, maintains stance",
                source="bloomberg.com",
            )
        ),
        WorkingArticle(
            raw=_raw("RBI keeps repo rate unchanged as expected", source="cnbc.com")
        ),
        WorkingArticle(
            raw=_raw(
                "India clinch cricket series with commanding win", source="thehindu.com"
            )
        ),
    ]
    events = deduper.deduplicate(arts)
    assert len(events) == 2
    multi = [e for e in events if e.source_count > 1]
    assert len(multi) == 1
    assert multi[0].source_count == 3


def test_finance_relevance_direct_holding_and_impact():
    agent = FinanceRelevanceAgent()
    event = WorkingEvent(
        title="Tata Steel posts record profit and margin surge",
        domain=Domain.FINANCE,
        summary="Tata Steel profit jumps on higher prices.",
    )
    holdings = [
        {
            "symbol": "TATASTEEL",
            "name": "Tata Steel",
            "sector": "Steel",
            "news_monitoring": True,
        }
    ]
    [out] = agent.analyze([event], holdings)
    assert out.finance_tier is FinanceRelevanceTier.DIRECT_HOLDING
    assert out.impacts and out.impacts[0].holding_symbol == "TATASTEEL"
    assert out.impacts[0].impact_type is ImpactType.POSITIVE
    # Fact vs analysis separation is populated.
    assert out.what_happened and out.ai_analysis


def test_finance_relevance_macro_tier():
    agent = FinanceRelevanceAgent()
    event = WorkingEvent(
        title="RBI holds repo rate steady amid inflation watch",
        domain=Domain.FINANCE,
        summary="The RBI kept its policy rate unchanged.",
    )
    [out] = agent.analyze([event], [])
    assert out.finance_tier is FinanceRelevanceTier.MACRO


def test_ranking_orders_high_relevance_first_with_honest_tiers():
    ranker = NewsRankingAgent()
    strong = WorkingEvent(
        title="Direct holding earnings",
        domain=Domain.FINANCE,
        finance_tier=FinanceRelevanceTier.DIRECT_HOLDING,
        event_time=datetime.now(UTC),
        articles=[WorkingArticle(raw=_raw("a")), WorkingArticle(raw=_raw("b"))],
    )
    weak = WorkingEvent(title="Minor sports note", domain=Domain.SPORTS)
    ranked = ranker.rank([weak, strong])
    assert ranked[0] is strong
    assert 0.0 <= strong.relevance_score <= 1.0
    assert ranked[0].relevance_tier.value in {"high", "medium", "low"}
