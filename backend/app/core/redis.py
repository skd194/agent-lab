"""Redis client and caching helpers (§28, §36).

Used for search caching, briefing caching, session state and rate limiting.
Degrades gracefully: if Redis is unavailable, callers fall back to recomputation.
"""

from __future__ import annotations

import json
from typing import Any

import redis.asyncio as aioredis

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_client: aioredis.Redis | None = None


def get_redis() -> aioredis.Redis:
    """Return a lazily-created shared async Redis client."""
    global _client
    if _client is None:
        _client = aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _client


async def cache_get_json(key: str) -> Any | None:
    """Get and JSON-decode a cached value, tolerating Redis being down."""
    try:
        raw = await get_redis().get(key)
    except Exception as exc:  # noqa: BLE001 - degrade gracefully if Redis is down
        logger.warning("redis_get_failed", key=key, error=str(exc))
        return None
    return json.loads(raw) if raw else None


async def cache_set_json(key: str, value: Any, ttl_seconds: int = 300) -> None:
    """JSON-encode and cache a value with a TTL, tolerating Redis being down."""
    try:
        await get_redis().set(key, json.dumps(value, default=str), ex=ttl_seconds)
    except Exception as exc:  # noqa: BLE001 - degrade gracefully if Redis is down
        logger.warning("redis_set_failed", key=key, error=str(exc))


async def close_redis() -> None:
    """Close the shared Redis client on shutdown."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
