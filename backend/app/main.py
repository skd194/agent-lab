"""AOEN FastAPI application entrypoint (§31)."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    ai,
    briefing,
    finance,
    news,
    preferences,
    system,
    voice,
)
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.core.redis import close_redis

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Startup/shutdown lifecycle."""
    logger.info(
        "aoen_starting",
        environment=settings.environment,
        demo_mode=settings.demo_mode,
        live_search=settings.has_live_search,
        live_llm=settings.has_live_llm,
    )
    yield
    await close_redis()
    logger.info("aoen_stopped")


app = FastAPI(
    title=f"{settings.app_name} — {settings.app_tagline}",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
for module in (system, preferences, briefing, news, finance, ai, voice):
    app.include_router(module.router, prefix=settings.api_prefix)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Simple liveness probe."""
    return {"status": "ok"}
