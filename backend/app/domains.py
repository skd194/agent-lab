"""Canonical AOEN news domains (§3).

Domains are defined centrally so query planning, classification, and the
frontend all agree on the same set. Order reflects default display priority.
"""

from enum import Enum


class Domain(str, Enum):
    """Primary AOEN intelligence domains."""

    FINANCE = "finance"
    TECHNOLOGY = "technology"
    INTERNATIONAL = "international"
    INDIA = "india"
    BUSINESS = "business"
    SCIENCE = "science"
    EDUCATION = "education"
    SPORTS = "sports"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"


DOMAIN_LABELS: dict[Domain, str] = {
    Domain.FINANCE: "Finance & Markets",
    Domain.TECHNOLOGY: "Technology",
    Domain.INTERNATIONAL: "International",
    Domain.INDIA: "India",
    Domain.BUSINESS: "Business",
    Domain.SCIENCE: "Science",
    Domain.EDUCATION: "Education",
    Domain.SPORTS: "Sports",
    Domain.ENTERTAINMENT: "Entertainment",
    Domain.GENERAL: "General",
}

# Default domains a new user sees, in order (§24).
DEFAULT_DOMAINS: list[Domain] = [
    Domain.FINANCE,
    Domain.TECHNOLOGY,
    Domain.INTERNATIONAL,
    Domain.INDIA,
    Domain.SCIENCE,
    Domain.SPORTS,
]


class ImpactType(str, Enum):
    """Informational impact classification (§7). NOT investment advice."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"
    WATCH = "watch"


class RelevanceTier(str, Enum):
    """Human-readable relevance buckets shown in the UI (§16)."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FinanceRelevanceTier(str, Enum):
    """Finance priority hierarchy (§5)."""

    DIRECT_HOLDING = "direct_holding"  # Priority 1
    SECTOR = "sector"  # Priority 2
    MACRO = "macro"  # Priority 3
    GENERAL = "general"  # Priority 4


def relevance_tier_from_score(score: float) -> RelevanceTier:
    """Map a 0..1 internal score to a coarse, honest tier (§16).

    We deliberately avoid exposing fake precision like "93.27% important".
    """
    if score >= 0.66:
        return RelevanceTier.HIGH
    if score >= 0.33:
        return RelevanceTier.MEDIUM
    return RelevanceTier.LOW
