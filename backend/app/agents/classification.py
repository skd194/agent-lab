"""News Classification Agent (§10).

Assigns each article to a domain. Articles inherit the domain of the query that
found them; this agent refines that using keyword heuristics (and can override
a GENERAL label). Works fully offline; an LLM can sharpen it later.
"""

from __future__ import annotations

from app.agents.state import WorkingArticle
from app.domains import Domain

# Minimal keyword signals per domain (lowercase). Deliberately conservative.
_KEYWORDS: dict[Domain, tuple[str, ...]] = {
    Domain.FINANCE: (
        "stock",
        "shares",
        "market",
        "sensex",
        "nifty",
        "rbi",
        "inflation",
        "earnings",
        "ipo",
        "rupee",
        "bond",
        "crude",
        "fed",
        "interest rate",
    ),
    Domain.TECHNOLOGY: (
        "ai",
        "artificial intelligence",
        "software",
        "chip",
        "semiconductor",
        "startup",
        "app",
        "cloud",
        "gadget",
        "smartphone",
        "openai",
        "google",
    ),
    Domain.SPORTS: (
        "cricket",
        "football",
        "match",
        "tournament",
        "olympics",
        "goal",
        "wicket",
        "series win",
        "championship",
    ),
    Domain.SCIENCE: (
        "research",
        "study",
        "scientists",
        "space",
        "nasa",
        "isro",
        "climate",
        "discovery",
        "physics",
        "biology",
    ),
    Domain.ENTERTAINMENT: (
        "film",
        "movie",
        "box office",
        "actor",
        "music",
        "series",
        "bollywood",
        "hollywood",
    ),
    Domain.EDUCATION: (
        "school",
        "university",
        "exam",
        "students",
        "education policy",
        "neet",
        "curriculum",
    ),
    Domain.INDIA: ("india", "modi", "parliament", "delhi", "mumbai"),
    Domain.INTERNATIONAL: (
        "united nations",
        "war",
        "summit",
        "president",
        "election",
        "border",
    ),
}


class NewsClassificationAgent:
    """Classifies articles into domains (§10)."""

    name = "classification"

    def classify(self, articles: list[WorkingArticle]) -> list[WorkingArticle]:
        """Refine the domain of each article in place and return the list."""
        for article in articles:
            # Trust a specific (non-general) domain from query planning.
            if article.domain is not Domain.GENERAL:
                continue
            article.domain = self._infer(article)
        return articles

    @staticmethod
    def _infer(article: WorkingArticle) -> Domain:
        text = f"{article.raw.title} {article.raw.content}".lower()
        best_domain = Domain.GENERAL
        best_score = 0
        for domain, keywords in _KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_domain = domain
        return best_domain
