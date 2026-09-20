"""Query Planning Agent (§10).

Generates targeted searches for each preferred domain. For finance it builds
queries dynamically from the user's holdings across the priority hierarchy (§5):
direct holdings, sectors, and macro-economic themes.
"""

from __future__ import annotations

from typing import Any

from app.agents.state import PlannedQuery
from app.domains import DEFAULT_DOMAINS, Domain, FinanceRelevanceTier

# Macro themes relevant to markets (§5, Priority 3). Not user-specific.
_MACRO_QUERIES = [
    "RBI monetary policy interest rate decision",
    "India inflation CPI data",
    "USD INR rupee exchange rate",
    "crude oil price movement",
    "US Federal Reserve interest rate decision",
    "global stock market movement today",
]

_GENERAL_FINANCE_QUERIES = [
    "Indian stock market Sensex Nifty today",
    "global markets IPO banking news",
]

# Lightweight per-domain query templates for non-finance domains.
_DOMAIN_QUERIES: dict[Domain, list[str]] = {
    Domain.TECHNOLOGY: [
        "major technology and AI news today",
        "big tech product launches and funding today",
    ],
    Domain.INTERNATIONAL: [
        "top international world news today",
        "major geopolitical developments today",
    ],
    Domain.INDIA: [
        "top India national news today",
        "India policy and economy news today",
    ],
    Domain.BUSINESS: ["major business and corporate news today"],
    Domain.SCIENCE: ["important science and research breakthroughs today"],
    Domain.EDUCATION: ["major education sector and policy news today"],
    Domain.SPORTS: ["top sports headlines and results today"],
    Domain.ENTERTAINMENT: ["major entertainment and film industry news today"],
    Domain.GENERAL: ["top world news headlines today"],
}


class QueryPlanningAgent:
    """Plans the set of searches for a briefing run."""

    name = "query_planning"

    def plan(
        self,
        preferred_domains: list[str],
        holdings: list[dict[str, Any]],
    ) -> list[PlannedQuery]:
        """Return the full list of planned queries."""
        domains = self._resolve_domains(preferred_domains)
        queries: list[PlannedQuery] = []

        for domain in domains:
            if domain is Domain.FINANCE:
                queries.extend(self._finance_queries(holdings))
            else:
                for q in _DOMAIN_QUERIES.get(domain, []):
                    queries.append(PlannedQuery(query=q, domain=domain))

        # De-duplicate identical query strings while preserving order.
        seen: set[str] = set()
        unique: list[PlannedQuery] = []
        for pq in queries:
            if pq.query not in seen:
                seen.add(pq.query)
                unique.append(pq)
        return unique

    @staticmethod
    def _resolve_domains(preferred: list[str]) -> list[Domain]:
        resolved: list[Domain] = []
        for key in preferred or []:
            try:
                resolved.append(Domain(key))
            except ValueError:
                continue
        return resolved or list(DEFAULT_DOMAINS)

    @staticmethod
    def _finance_queries(holdings: list[dict[str, Any]]) -> list[PlannedQuery]:
        queries: list[PlannedQuery] = []

        # Priority 1 — direct holdings (§5).
        monitored = [h for h in holdings if h.get("news_monitoring", True)]
        for h in monitored:
            name = h.get("name") or h.get("symbol", "")
            symbol = h.get("symbol", "")
            queries.append(
                PlannedQuery(
                    query=f"{name} {symbol} stock news earnings",
                    domain=Domain.FINANCE,
                    holding_symbol=symbol,
                    finance_tier=FinanceRelevanceTier.DIRECT_HOLDING,
                )
            )

        # Priority 2 — sectors represented in the portfolio (§5).
        sectors = sorted({h.get("sector") for h in monitored if h.get("sector")})
        for sector in sectors:
            queries.append(
                PlannedQuery(
                    query=f"{sector} sector India news prices demand policy",
                    domain=Domain.FINANCE,
                    finance_tier=FinanceRelevanceTier.SECTOR,
                )
            )

        # Priority 3 — macro-economic themes (§5).
        for q in _MACRO_QUERIES:
            queries.append(
                PlannedQuery(
                    query=q,
                    domain=Domain.FINANCE,
                    finance_tier=FinanceRelevanceTier.MACRO,
                )
            )

        # Priority 4 — general financial news (§5).
        for q in _GENERAL_FINANCE_QUERIES:
            queries.append(
                PlannedQuery(
                    query=q,
                    domain=Domain.FINANCE,
                    finance_tier=FinanceRelevanceTier.GENERAL,
                )
            )

        return queries
