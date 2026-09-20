"""In-memory demo store (§38).

Provides working CRUD for preferences and portfolio holdings without a database
so the entire app is functional in demo mode. Seeded from curated demo data and
reset per process. When ``DEMO_MODE=false`` with Postgres available, the DB
repositories take over (see app/repositories).
"""

from __future__ import annotations

import copy
from uuid import uuid4

from app.services import demo_data


class DemoStore:
    """Process-lifetime in-memory store for demo mode."""

    def __init__(self) -> None:
        self._preferences = copy.deepcopy(demo_data.DEMO_PREFERENCES)
        self._holdings = copy.deepcopy(demo_data.DEMO_HOLDINGS)

    # -- Preferences ---------------------------------------------------------
    def get_preferences(self) -> dict:
        return copy.deepcopy(self._preferences)

    def update_preferences(self, data: dict) -> dict:
        self._preferences.update({k: v for k, v in data.items() if v is not None})
        return copy.deepcopy(self._preferences)

    # -- Holdings ------------------------------------------------------------
    def list_holdings(self) -> list[dict]:
        return copy.deepcopy(self._holdings)

    def add_holding(self, data: dict) -> dict:
        holding = {"id": f"h-{uuid4().hex[:8]}", **data}
        self._holdings.append(holding)
        return copy.deepcopy(holding)

    def update_holding(self, holding_id: str, data: dict) -> dict | None:
        for h in self._holdings:
            if h["id"] == holding_id:
                h.update({k: v for k, v in data.items() if v is not None})
                return copy.deepcopy(h)
        return None

    def delete_holding(self, holding_id: str) -> bool:
        before = len(self._holdings)
        self._holdings = [h for h in self._holdings if h["id"] != holding_id]
        return len(self._holdings) < before


demo_store = DemoStore()
