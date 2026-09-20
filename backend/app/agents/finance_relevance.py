"""Finance Relevance Agent (§5, §7).

For finance events, determines the priority tier (direct holding / sector /
macro / general), which holdings may be affected, and an informational impact
classification. It NEVER produces buy/sell/hold advice (§7): output is limited
to FACT, AI ANALYSIS, and PORTFOLIO RELEVANCE.
"""

from __future__ import annotations

from typing import Any

from app.agents.state import HoldingImpact, WorkingEvent
from app.domains import Domain, FinanceRelevanceTier, ImpactType

_POSITIVE = {
    "surge",
    "jump",
    "rises",
    "rise",
    "record",
    "profit",
    "beats",
    "beat",
    "wins",
    "win",
    "approval",
    "expansion",
    "gain",
    "gains",
    "growth",
    "high",
    "order",
    "contract",
    "upgrade",
}
_NEGATIVE = {
    "fall",
    "falls",
    "drop",
    "drops",
    "loss",
    "losses",
    "decline",
    "probe",
    "fraud",
    "ban",
    "cut",
    "cuts",
    "warning",
    "miss",
    "slump",
    "downgrade",
    "layoff",
    "layoffs",
    "penalty",
    "recall",
    "strike",
}

_MACRO_TERMS = {
    "rbi",
    "inflation",
    "cpi",
    "gdp",
    "fed",
    "federal reserve",
    "interest rate",
    "rupee",
    "usd inr",
    "crude",
    "oil",
    "bond yield",
    "monetary policy",
}


def _impact_from_text(text: str) -> ImpactType:
    low = text.lower()
    pos = any(w in low for w in _POSITIVE)
    neg = any(w in low for w in _NEGATIVE)
    if pos and neg:
        return ImpactType.MIXED
    if pos:
        return ImpactType.POSITIVE
    if neg:
        return ImpactType.NEGATIVE
    return ImpactType.WATCH


class FinanceRelevanceAgent:
    """Classifies finance events against the user's portfolio (§5)."""

    name = "finance_relevance"

    def analyze(
        self,
        events: list[WorkingEvent],
        holdings: list[dict[str, Any]],
    ) -> list[WorkingEvent]:
        """Annotate finance events with tier, impacts and analysis."""
        for event in events:
            if event.domain is not Domain.FINANCE:
                continue
            self._analyze_event(event, holdings)
        return events

    def _analyze_event(
        self, event: WorkingEvent, holdings: list[dict[str, Any]]
    ) -> None:
        text = f"{event.title} {event.summary or ''}".lower()
        impact = _impact_from_text(text)

        # Priority 1 — direct holdings (§5).
        affected = [
            h
            for h in holdings
            if h.get("news_monitoring", True)
            and (
                h.get("symbol", "").lower() in text
                or (h.get("name", "").lower() and h["name"].lower() in text)
            )
        ]
        if affected:
            event.finance_tier = FinanceRelevanceTier.DIRECT_HOLDING
            event.impacts = [
                HoldingImpact(
                    holding_symbol=h["symbol"],
                    impact_type=impact,
                    rationale=(f"Directly references {h.get('name', h['symbol'])}."),
                )
                for h in affected
            ]
            names = ", ".join(h.get("name", h["symbol"]) for h in affected)
            event.portfolio_relevance = f"Directly relates to your holding(s): {names}."
            self._set_analysis(event, impact)
            return

        # Priority 2 — sectors represented in the portfolio (§5).
        sectors = {
            h.get("sector", "").lower()
            for h in holdings
            if h.get("sector") and h.get("news_monitoring", True)
        }
        matched_sector = next((s for s in sectors if s and s in text), None)
        if matched_sector:
            event.finance_tier = FinanceRelevanceTier.SECTOR
            sector_holdings = [
                h for h in holdings if (h.get("sector") or "").lower() == matched_sector
            ]
            event.impacts = [
                HoldingImpact(
                    holding_symbol=h["symbol"],
                    impact_type=ImpactType.WATCH,
                    rationale=f"Sector development in {h.get('sector')}.",
                )
                for h in sector_holdings
            ]
            event.portfolio_relevance = (
                f"Affects the {matched_sector.title()} sector, which is "
                "represented in your portfolio."
            )
            self._set_analysis(event, impact)
            return

        # Priority 3 — macro-economic (§5).
        if any(term in text for term in _MACRO_TERMS):
            event.finance_tier = FinanceRelevanceTier.MACRO
            event.portfolio_relevance = (
                "Macro-economic development that can broadly influence markets "
                "and, indirectly, your portfolio."
            )
            self._set_analysis(event, impact)
            return

        # Priority 4 — general financial news (§5).
        event.finance_tier = FinanceRelevanceTier.GENERAL
        event.portfolio_relevance = (
            "General financial news with no direct link to your holdings."
        )
        self._set_analysis(event, impact)

    @staticmethod
    def _set_analysis(event: WorkingEvent, impact: ImpactType) -> None:
        # FACT vs AI ANALYSIS separation (§7). No investment recommendations.
        event.what_happened = event.summary or event.title
        event.ai_analysis = (
            f"AOEN reads this as an informational '{impact.value}' signal for "
            "the related area. This is analysis for awareness only, not "
            "investment advice."
        )
        for holding_impact in event.impacts:
            if holding_impact.impact_type is ImpactType.WATCH and impact is not (
                ImpactType.WATCH
            ):
                holding_impact.impact_type = impact
