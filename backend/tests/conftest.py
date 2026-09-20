"""Pytest fixtures. Tests run in demo mode (the default), so no keys/DB/Redis
are required."""

import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """A TestClient for the AOEN API in demo mode."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def holdings() -> list[dict]:
    return [
        {
            "symbol": "TATASTEEL",
            "name": "Tata Steel",
            "sector": "Steel",
            "news_monitoring": True,
        },
        {
            "symbol": "INFY",
            "name": "Infosys",
            "sector": "IT",
            "news_monitoring": True,
        },
    ]
