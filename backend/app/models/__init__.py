"""SQLAlchemy ORM models (§26).

Importing this package registers every model on ``Base.metadata`` so Alembic
autogeneration and ``create_all`` see the full schema.
"""

from app.core.database import Base
from app.models.agent import AgentExecution
from app.models.briefing import BriefingItem, DailyBriefing
from app.models.news import (
    NewsArticle,
    NewsCategory,
    NewsEvent,
    NewsImpact,
    NewsInsight,
    NewsSource,
)
from app.models.portfolio import Portfolio, PortfolioHolding
from app.models.user import User, UserPreference
from app.models.voice import VoiceSession

__all__ = [
    "AgentExecution",
    "Base",
    "BriefingItem",
    "DailyBriefing",
    "NewsArticle",
    "NewsCategory",
    "NewsEvent",
    "NewsImpact",
    "NewsInsight",
    "NewsSource",
    "Portfolio",
    "PortfolioHolding",
    "User",
    "UserPreference",
    "VoiceSession",
]
