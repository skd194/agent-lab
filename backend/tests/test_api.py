"""API endpoint + portfolio CRUD tests (§50)."""


def test_system_status(client):
    r = client.get("/api/system/status")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "AOEN"
    assert body["demo_mode"] is True


def test_briefing_today_structure(client):
    r = client.get("/api/briefing/today")
    assert r.status_code == 200
    b = r.json()
    for key in (
        "greeting",
        "headline",
        "window",
        "stats",
        "top_priorities",
        "finance",
        "sections",
        "activity",
    ):
        assert key in b
    assert b["stats"]["total_events"] > 0


def test_news_categories_and_detail(client):
    cats = client.get("/api/news/categories").json()
    assert any(c["key"] == "finance" for c in cats)
    detail = client.get("/api/news/evt-rbi-policy")
    assert detail.status_code == 200
    assert detail.json()["category"] == "finance"


def test_news_detail_404(client):
    assert client.get("/api/news/does-not-exist").status_code == 404


def test_finance_portfolio_metrics(client):
    p = client.get("/api/finance/portfolio").json()
    assert p["overview"]["holdings_count"] == len(p["holdings"])
    # Current value is quantity * last price aggregated.
    assert p["overview"]["current_value"] > 0
    assert all("unrealized_pl_pct" in h for h in p["holdings"])


def test_finance_news_ranked_by_portfolio_relevance(client):
    events = client.get("/api/finance/news").json()
    assert len(events) > 0
    # The first item should be the most portfolio-relevant tier available.
    first = events[0]
    assert first["insight"]["finance_tier"] in (
        "direct_holding",
        "sector",
        "macro",
        "general",
    )


def test_portfolio_crud_roundtrip(client):
    payload = {
        "symbol": "WIPRO",
        "name": "Wipro",
        "exchange": "NSE",
        "sector": "IT",
        "quantity": 50,
        "average_price": 400,
        "priority": "LOW",
        "news_monitoring": True,
    }
    created = client.post("/api/finance/portfolio", json=payload)
    assert created.status_code == 201
    hid = created.json()["id"]

    updated = client.put(f"/api/finance/portfolio/{hid}", json={"quantity": 75})
    assert updated.status_code == 200
    assert updated.json()["quantity"] == 75

    deleted = client.delete(f"/api/finance/portfolio/{hid}")
    assert deleted.status_code == 204
    # Deleting again is a 404.
    assert client.delete(f"/api/finance/portfolio/{hid}").status_code == 404


def test_preferences_update(client):
    client.put("/api/preferences", json={"stories_per_domain": 7})
    prefs = client.get("/api/preferences").json()
    assert prefs["stories_per_domain"] == 7


def test_ai_chat_grounded_in_event(client):
    r = client.post(
        "/api/ai/chat",
        json={
            "message": "Explain this",
            "event_id": "evt-tatasteel-earnings",
            "history": [],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["answer"]
    assert len(body["sources"]) >= 1


def test_voice_command_routing(client):
    r = client.post(
        "/api/voice/command", json={"transcript": "AOEN, give me the finance briefing"}
    )
    assert r.status_code == 200
    assert r.json()["intent"] == "finance_briefing"

    r2 = client.post(
        "/api/voice/command", json={"transcript": "what's happening with Tata Steel"}
    )
    assert r2.json()["intent"] == "entity_query"
    assert "tata steel" in r2.json()["args"].get("entity", "").lower()
