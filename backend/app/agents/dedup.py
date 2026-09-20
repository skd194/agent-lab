"""News Deduplication Agent (§15).

Groups articles that describe the same real-world event into a single
:class:`WorkingEvent` with multiple sources. Uses token-overlap (Jaccard) plus
title sequence similarity rather than naive exact title matching (§15). Works
offline; an embedding model can replace the similarity function later.
"""

from __future__ import annotations

import re
from collections import Counter
from difflib import SequenceMatcher

from app.agents.state import WorkingArticle, WorkingEvent
from app.core.logging import get_logger
from app.domains import Domain

logger = get_logger(__name__)

_STOPWORDS = {
    "the",
    "a",
    "an",
    "to",
    "of",
    "in",
    "on",
    "for",
    "and",
    "or",
    "as",
    "at",
    "by",
    "is",
    "are",
    "be",
    "with",
    "from",
    "after",
    "over",
    "amid",
    "says",
    "say",
    "new",
    "will",
    "its",
    "it",
    "into",
    "up",
    "down",
    "how",
    "why",
    "what",
    "this",
    "that",
    "today",
    "news",
    "report",
    "reports",
}

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9]+")
_SIMILARITY_THRESHOLD = 0.42


def _tokens(text: str) -> set[str]:
    words = _WORD_RE.findall(text.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 2}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _title_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _extract_entities(text: str, limit: int = 6) -> list[str]:
    """Cheap proper-noun-ish entity extraction (capitalised multiword runs)."""
    candidates = re.findall(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,2})\b", text)
    counts = Counter(c.strip() for c in candidates if len(c) > 2)
    return [name for name, _ in counts.most_common(limit)]


class NewsDeduplicationAgent:
    """Clusters similar articles into events (§15, §27)."""

    name = "deduplication"

    def deduplicate(self, articles: list[WorkingArticle]) -> list[WorkingEvent]:
        """Group articles into deduplicated events."""
        clusters: list[list[WorkingArticle]] = []
        signatures: list[set[str]] = []

        for article in articles:
            sig = _tokens(article.raw.title)
            matched = -1
            best = _SIMILARITY_THRESHOLD
            for i, existing in enumerate(signatures):
                score = _jaccard(sig, existing)
                if (
                    score >= best
                    or _title_ratio(article.raw.title, clusters[i][0].raw.title) >= 0.68
                ):
                    best = max(best, score)
                    matched = i
            if matched >= 0:
                clusters[matched].append(article)
                signatures[matched] |= sig
            else:
                clusters.append([article])
                signatures.append(sig)

        events = [self._build_event(cluster) for cluster in clusters]
        logger.info("dedup_complete", articles=len(articles), events=len(events))
        return events

    @staticmethod
    def _build_event(cluster: list[WorkingArticle]) -> WorkingEvent:
        # Representative article: highest search score, then longest title.
        rep = max(cluster, key=lambda a: (a.raw.score, len(a.raw.title)))
        # Majority domain across the cluster.
        domain_counts = Counter(a.domain for a in cluster)
        domain = domain_counts.most_common(1)[0][0]
        published = [a.raw.published_at for a in cluster if a.raw.published_at]
        entities = _extract_entities(f"{rep.raw.title}. {rep.raw.content}")
        return WorkingEvent(
            title=rep.raw.title,
            domain=domain if isinstance(domain, Domain) else Domain.GENERAL,
            articles=cluster,
            entities=entities,
            event_time=max(published) if published else None,
        )
