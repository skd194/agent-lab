"""Redis client and caching helpers (§28, §36).

Used for search caching, briefing caching, session state and rate limiting.
Degrades gracefully: if Redis is unavailable, callers fall back to recomputation.
A simple circuit breaker disables Redis for a cooldown after a failure so a
missing Redis never slows requests down (important in demo mode §38).
"""

from __future__ import annotations

import json
import time
from typing import Any

import redis.asyncio as aioredis

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_client: aioredis.Redis | None = None

# Circuit breaker: after a failure, skip Redis entirely for this many seconds.
_COOLDOWN_SECONDS = 60.0
_disabled_until: float = 0.0


def _redis_disabled() -> bool:
    return time.monotonic() < _disabled_until


def _trip_breaker() -> None:
    global _disabled_until
    _disabled_until = time.monotonic() + _COOLDOWN_SECONDS


def get_redis() -> aioredis.Redis:
    """Return a lazily-created shared async Redis client with fast-fail timeouts."""
    global _client
    if _client is None:
        _client = aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=0.5,
            socket_timeout=0.5,
            retry_on_timeout=False,
        )
    return _client


async def cache_get_json(key: str) -> Any | None:
    """Get and JSON-decode a cached value, tolerating Redis being down."""
    if _redis_disabled():
        return None
    try:
        raw = await get_redis().get(key)
    except Exception as exc:  # noqa: BLE001 - degrade gracefully if Redis is down
        logger.warning("redis_get_failed", key=key, error=str(exc))
        _trip_breaker()
        return None
    return json.loads(raw) if raw else None


async def cache_set_json(key: str, value: Any, ttl_seconds: int = 300) -> None:
    """JSON-encode and cache a value with a TTL, tolerating Redis being down."""
    if _redis_disabled():
        return
    try:
        await get_redis().set(key, json.dumps(value, default=str), ex=ttl_seconds)
    except Exception as exc:  # noqa: BLE001 - degrade gracefully if Redis is down
        logger.warning("redis_set_failed", key=key, error=str(exc))
        _trip_breaker()


async def close_redis() -> None:
    """Close the shared Redis client on shutdown."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
