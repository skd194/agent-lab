"""Curated demo data (§38, §54).

Hand-crafted, realistic content so AOEN looks and feels premium with zero API
keys. Used by the service layer whenever demo mode is on or the database is
unavailable. Nothing here is hard-coded into business logic — it is seed data.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.domains import Domain

_NOW = datetime.now(UTC)


def _ago(hours: float) -> datetime:
    return _NOW - timedelta(hours=hours)


# --- Demo user + preferences (§24) ------------------------------------------
DEMO_USER = {
    "id": "demo-user",
    "name": "Commander",
    "email": None,
}

DEMO_PREFERENCES = {
    "name": "Commander",
    "timezone": "Asia/Kolkata",
    "briefing_time": "08:00",
    "news_window_hours": 24,
    "stories_per_domain": 5,
    "voice_enabled": True,
    "preferred_domains": [
        Domain.FINANCE.value,
        Domain.TECHNOLOGY.value,
        Domain.INTERNATIONAL.value,
        Domain.INDIA.value,
        Domain.SCIENCE.value,
        Domain.SPORTS.value,
    ],
}


# --- Demo portfolio (§4, §6) — fully illustrative, not advice ---------------
DEMO_HOLDINGS = [
    {
        "id": "h-tatasteel",
        "symbol": "TATASTEEL",
        "name": "Tata Steel",
        "exchange": "NSE",
        "sector": "Steel",
        "quantity": 300,
        "average_price": 128.5,
        "priority": "HIGH",
        "news_monitoring": True,
        "last_price": 141.2,
        "day_change_pct": 1.8,
    },
    {
        "id": "h-infy",
        "symbol": "INFY",
        "name": "Infosys",
        "exchange": "NSE",
        "sector": "IT",
        "quantity": 90,
        "average_price": 1420.0,
        "priority": "HIGH",
        "news_monitoring": True,
        "last_price": 1536.4,
        "day_change_pct": -0.6,
    },
    {
        "id": "h-hdfcbank",
        "symbol": "HDFCBANK",
        "name": "HDFC Bank",
        "exchange": "NSE",
        "sector": "Banking",
        "quantity": 120,
        "average_price": 1510.0,
        "priority": "MEDIUM",
        "news_monitoring": True,
        "last_price": 1662.0,
        "day_change_pct": 0.9,
    },
    {
        "id": "h-reliance",
        "symbol": "RELIANCE",
        "name": "Reliance Industries",
        "exchange": "NSE",
        "sector": "Energy",
        "quantity": 40,
        "average_price": 2380.0,
        "priority": "MEDIUM",
        "news_monitoring": True,
        "last_price": 2547.5,
        "day_change_pct": 0.3,
    },
]


def _article(title, url, source, summary, hours, query):
    return {
        "title": title,
        "url": url,
        "source_name": source,
        "ai_summary": summary,
        "published_at": _ago(hours).isoformat(),
        "retrieved_at": _NOW.isoformat(),
        "search_query": query,
    }


# --- Curated events across domains (§13, §15) -------------------------------
# Each event mirrors the EventOut schema. Finance events carry AI insight (§7).
DEMO_EVENTS: list[dict] = [
    {
        "id": "evt-tatasteel-earnings",
        "title": "Tata Steel posts stronger quarterly margins on firmer prices",
        "summary": (
            "Tata Steel reported improved operating margins for the quarter, "
            "helped by firmer domestic steel prices and lower input costs."
        ),
        "category": Domain.FINANCE.value,
        "why_it_matters": "One of your high-priority holdings; margins drive the stock.",
        "relevance_tier": "high",
        "entities": ["Tata Steel", "India", "Steel"],
        "verified": True,
        "event_time": _ago(3).isoformat(),
        "sources": [
            _article(
                "Tata Steel Q results beat estimates on margin recovery",
                "https://reuters.com/markets/tata-steel-q-results",
                "reuters.com",
                "Margins recovered on firmer steel prices and cost control.",
                3,
                "Tata Steel TATASTEEL stock news earnings",
            ),
            _article(
                "Tata Steel margins improve as steel prices firm up",
                "https://livemint.com/markets/tata-steel-margins",
                "livemint.com",
                "Analysts note sequential margin improvement.",
                4,
                "Tata Steel TATASTEEL stock news earnings",
            ),
        ],
        "insight": {
            "what_happened": (
                "Tata Steel reported stronger sequential operating margins on "
                "firmer domestic prices and softer coking coal costs."
            ),
            "ai_analysis": (
                "AOEN reads this as an informational 'positive' signal for the "
                "steel area. Analysis for awareness only, not investment advice."
            ),
            "portfolio_relevance": "Directly relates to your holding: Tata Steel.",
            "finance_tier": "direct_holding",
            "impacts": [
                {
                    "holding_symbol": "TATASTEEL",
                    "impact_type": "positive",
                    "rationale": "Directly references Tata Steel earnings.",
                }
            ],
        },
    },
    {
        "id": "evt-steel-import-duty",
        "title": "India weighs safeguard duty on steel imports amid cheap inflows",
        "summary": (
            "The government is considering a safeguard duty on certain steel "
            "imports to counter a surge in low-priced inflows."
        ),
        "category": Domain.FINANCE.value,
        "why_it_matters": "Sector-wide policy that affects your Steel holding.",
        "relevance_tier": "high",
        "entities": ["India", "Steel", "Import Duty"],
        "verified": True,
        "event_time": _ago(6).isoformat(),
        "sources": [
            _article(
                "India may impose safeguard duty on steel imports",
                "https://cnbc.com/india-steel-safeguard-duty",
                "cnbc.com",
                "Move aims to protect domestic mills from cheap imports.",
                6,
                "Steel sector India news prices demand policy",
            ),
        ],
        "insight": {
            "what_happened": (
                "India is weighing a safeguard duty on select steel imports."
            ),
            "ai_analysis": (
                "AOEN reads this as an informational 'watch' signal for the "
                "steel sector. Analysis for awareness only, not advice."
            ),
            "portfolio_relevance": (
                "Affects the Steel sector, represented by Tata Steel."
            ),
            "finance_tier": "sector",
            "impacts": [
                {
                    "holding_symbol": "TATASTEEL",
                    "impact_type": "watch",
                    "rationale": "Sector development in Steel.",
                }
            ],
        },
    },
    {
        "id": "evt-rbi-policy",
        "title": "RBI holds repo rate steady, keeps stance unchanged",
        "summary": (
            "The Reserve Bank of India kept its policy repo rate unchanged and "
            "maintained its stance, citing balanced growth-inflation dynamics."
        ),
        "category": Domain.FINANCE.value,
        "why_it_matters": "Macro anchor for banks and broad markets.",
        "relevance_tier": "high",
        "entities": ["RBI", "India"],
        "verified": True,
        "event_time": _ago(5).isoformat(),
        "sources": [
            _article(
                "RBI keeps repo rate unchanged",
                "https://reuters.com/rbi-repo-rate",
                "reuters.com",
                "Rate held; stance unchanged.",
                5,
                "RBI monetary policy interest rate decision",
            ),
            _article(
                "Reserve Bank leaves rates on hold",
                "https://bloomberg.com/rbi-rates-hold",
                "bloomberg.com",
                "Governor flags data-dependent path.",
                5,
                "RBI monetary policy interest rate decision",
            ),
            _article(
                "RBI maintains status quo on rates",
                "https://moneycontrol.com/rbi-status-quo",
                "moneycontrol.com",
                "Markets had largely priced in the hold.",
                6,
                "RBI monetary policy interest rate decision",
            ),
        ],
        "insight": {
            "what_happened": "The RBI kept the repo rate and stance unchanged.",
            "ai_analysis": (
                "AOEN reads this as an informational 'neutral' macro signal. "
                "Analysis for awareness only, not investment advice."
            ),
            "portfolio_relevance": (
                "Macro development that broadly influences markets and banks "
                "like HDFC Bank."
            ),
            "finance_tier": "macro",
            "impacts": [
                {
                    "holding_symbol": "HDFCBANK",
                    "impact_type": "neutral",
                    "rationale": "Rate decision affects banking margins.",
                }
            ],
        },
    },
    {
        "id": "evt-ai-platform",
        "title": "Major cloud provider unveils next-generation AI platform",
        "summary": (
            "A leading cloud provider announced a new AI platform with cheaper "
            "inference and expanded enterprise tooling."
        ),
        "category": Domain.TECHNOLOGY.value,
        "why_it_matters": "Signals intensifying enterprise AI competition.",
        "relevance_tier": "high",
        "entities": ["AI", "Cloud"],
        "verified": True,
        "event_time": _ago(2).isoformat(),
        "sources": [
            _article(
                "Cloud giant launches new AI platform",
                "https://reuters.com/tech-ai-platform",
                "reuters.com",
                "Cheaper inference; new enterprise tools.",
                2,
                "major technology and AI news today",
            ),
            _article(
                "New enterprise AI stack announced",
                "https://cnbc.com/tech-ai-stack",
                "cnbc.com",
                "Aimed at large enterprise deployments.",
                3,
                "major technology and AI news today",
            ),
        ],
    },
    {
        "id": "evt-semiconductor",
        "title": "Global chipmakers expand capacity amid AI demand",
        "summary": (
            "Several chipmakers outlined capacity expansions to meet surging "
            "demand for AI accelerators."
        ),
        "category": Domain.TECHNOLOGY.value,
        "why_it_matters": "Supply signals ripple across the tech supply chain.",
        "relevance_tier": "medium",
        "entities": ["Semiconductors", "AI"],
        "verified": True,
        "event_time": _ago(7).isoformat(),
        "sources": [
            _article(
                "Chipmakers ramp capacity for AI",
                "https://ft.com/chip-capacity-ai",
                "ft.com",
                "Fabs expand to meet accelerator demand.",
                7,
                "big tech product launches and funding today",
            ),
        ],
    },
    {
        "id": "evt-summit",
        "title": "Leaders convene for summit on trade and security",
        "summary": (
            "Heads of state gathered for a summit focused on trade corridors "
            "and regional security cooperation."
        ),
        "category": Domain.INTERNATIONAL.value,
        "why_it_matters": "Outcomes can reshape trade and supply chains.",
        "relevance_tier": "medium",
        "entities": ["Summit", "Trade"],
        "verified": True,
        "event_time": _ago(8).isoformat(),
        "sources": [
            _article(
                "World leaders meet for trade and security summit",
                "https://reuters.com/world-summit",
                "reuters.com",
                "Agenda spans trade corridors and security.",
                8,
                "top international world news today",
            ),
        ],
    },
    {
        "id": "evt-india-infra",
        "title": "India approves major infrastructure investment package",
        "summary": (
            "The cabinet cleared a large infrastructure package spanning roads, "
            "ports and logistics corridors."
        ),
        "category": Domain.INDIA.value,
        "why_it_matters": "Infra spending supports growth and industrials.",
        "relevance_tier": "medium",
        "entities": ["India", "Infrastructure"],
        "verified": True,
        "event_time": _ago(9).isoformat(),
        "sources": [
            _article(
                "India clears big infrastructure package",
                "https://livemint.com/india-infra-package",
                "livemint.com",
                "Roads, ports and logistics in focus.",
                9,
                "top India national news today",
            ),
        ],
    },
    {
        "id": "evt-space",
        "title": "ISRO successfully tests reusable launch technology",
        "summary": (
            "India's space agency completed a key test of reusable launch "
            "technology, a step toward lower-cost access to space."
        ),
        "category": Domain.SCIENCE.value,
        "why_it_matters": "Cheaper launch capacity expands the space economy.",
        "relevance_tier": "medium",
        "entities": ["ISRO", "Space"],
        "verified": True,
        "event_time": _ago(10).isoformat(),
        "sources": [
            _article(
                "ISRO tests reusable launch vehicle tech",
                "https://thehindu.com/isro-rlv-test",
                "thehindu.com",
                "Milestone for low-cost launch.",
                10,
                "important science and research breakthroughs today",
            ),
        ],
    },
    {
        "id": "evt-cricket",
        "title": "India clinch series with commanding win",
        "summary": (
            "India sealed the series with a dominant all-round performance in "
            "the deciding match."
        ),
        "category": Domain.SPORTS.value,
        "why_it_matters": "Marquee series result for fans.",
        "relevance_tier": "low",
        "entities": ["India", "Cricket"],
        "verified": True,
        "event_time": _ago(11).isoformat(),
        "sources": [
            _article(
                "India win series with big victory",
                "https://reuters.com/sports-india-series",
                "reuters.com",
                "All-round display seals the series.",
                11,
                "top sports headlines and results today",
            ),
        ],
    },
]
