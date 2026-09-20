# AOEN — Personal Intelligence System

> **Understand the world. Know what matters.**

AOEN is a personal AI intelligence and command-center application. It behaves
like a personal intelligence officer that continuously understands what is
happening in the world and tells you what matters **to you** — with **Finance
and your investment portfolio as the highest-priority domain**.

The first capability is a **daily world-intelligence briefing**: AOEN researches,
filters, deduplicates, summarizes, prioritizes and personalizes the news before
presenting it, so you understand the most important developments in seconds.

---

## 1. What AOEN is

- A **daily briefing** across 10 domains (Finance, Technology, International,
  India, Business, Science, Education, Sports, Entertainment, General).
- A **finance intelligence terminal**: configure your portfolio and AOEN ranks
  news by relevance to your holdings (direct → sector → macro → general),
  separating **fact** from **AI analysis** and **portfolio relevance**.
- **Ask AOEN** chat + **voice** interaction (push-to-talk, interruptible).
- Designed to grow into a broader personal AI OS (email, calendar, tasks…).

AOEN is **informational only** and never gives buy/sell/hold advice.

---

## 2. Architecture

```
User Preferences ─┐
Portfolio ────────┤
                  ▼
        Query Planning Agent ──► (finance queries generated from holdings)
                  ▼
        News Discovery Agent ──► NewsSearchProvider (Tavily | Demo)
                  ▼
   Normalize → Classify → Deduplicate (events) → Summarize
                  ▼
      Finance Relevance → Ranking → Daily Briefing Agent
                  ▼
        FastAPI  ──►  React frontend  ──►  Voice Briefing
```

- **Provider abstraction (§8):** the rest of the system depends on
  `NewsSearchProvider`, not on Tavily. The existing Tavily/LangChain agent is
  preserved (`backend/app/providers/tavily_agent.py`) and wrapped by
  `TavilyNewsProvider`. A `DemoNewsProvider` powers offline mode.
- **Stateful workflow (§9):** agents are orchestrated by **LangGraph**
  (`backend/app/workflows/news_workflow.py`). Every agent has a deterministic
  non-LLM fallback so the whole pipeline runs offline.
- **Model-agnostic LLM (§45):** business logic calls `get_chat_model()`; a
  local model (e.g. Ollama) can be added without touching agents.
- **Article vs Event (§27):** many articles from different publishers collapse
  into one deduplicated event with multiple sources.

---

## 3. Technology stack

| Layer     | Technology |
| --------- | ---------- |
| Backend   | Python 3.11+, FastAPI, LangChain, LangGraph, Pydantic v2 |
| Data      | PostgreSQL (SQLAlchemy 2 async + Alembic), Redis |
| Search    | Tavily (via the preserved agent) |
| Frontend  | React 18, TypeScript, Vite, Tailwind CSS, Framer Motion, Recharts, React Query, Zustand |
| Tooling   | uv, black, isort, ruff, pylint, pytest |

---

## 4. Project structure

```
agent-lab/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # briefing, news, finance, ai, voice, preferences, system
│   │   ├── agents/           # query planning, discovery, classification, dedup,
│   │   │                     # summarization, finance relevance, ranking, briefing, voice, llm
│   │   ├── workflows/        # LangGraph news_workflow
│   │   ├── providers/        # NewsSearchProvider + tavily_agent (preserved) + demo
│   │   ├── services/         # briefing, portfolio, chat, voice, demo data/store, mappers
│   │   ├── models/           # SQLAlchemy ORM (14 models)
│   │   ├── schemas/          # Pydantic API contracts
│   │   ├── core/             # config, database, redis, logging
│   │   └── main.py           # FastAPI app
│   ├── alembic/              # migrations
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/       # core (AICore), layout, news, briefing, finance, chat, voice, ui
│       ├── pages/            # Overview, Finance, Domain, News, Portfolio, Preferences, Voice
│       ├── hooks/            # useVoice
│       ├── services/         # api client + React Query hooks
│       ├── stores/           # zustand (AI core, UI)
│       ├── lib/              # format, domains, cn
│       └── types/            # API types
├── docker-compose.yml        # Postgres + Redis
└── readme.md
```

---

## 5. Prerequisites

- **Python 3.11+** and **[uv](https://docs.astral.sh/uv/)**
- **Node.js 18+** and npm
- **Docker** (optional — only for Postgres/Redis; demo mode needs neither)

---

## 6. Installation

```bash
# Backend
cd backend
uv sync

# Frontend
cd ../frontend
npm install
```

> On networks that intercept TLS, uv may need system certificates:
> `uv sync --native-tls` (or set `UV_SYSTEM_CERTS=true`).

---

## 7. Environment variables

Copy `backend/.env.example` to `backend/.env`. Secrets stay **server-side only**
and never reach the browser (§37).

| Variable | Purpose |
| -------- | ------- |
| `DEMO_MODE` | `true` runs fully offline with mock data (default) |
| `TAVILY_API_KEY` | Enables live news search |
| `LLM_API_KEY` / `OPENAI_API_KEY` | Enables live LLM summaries/chat |
| `LLM_PROVIDER` / `LLM_MODEL` | Model selection (default `openai` / `gpt-4o`) |
| `DATABASE_URL` | Postgres DSN (`postgresql+asyncpg://…`) |
| `REDIS_URL` | Redis DSN |
| `CORS_ORIGINS` | Comma-separated allowed origins |

---

## 8. Running the frontend

```bash
cd frontend
npm run dev          # http://localhost:5173
```

The dev server proxies `/api` to the backend on port 8000.

---

## 9. Running the backend

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

---

## 10. Demo mode

AOEN works with **no API keys, no database, and no Redis** (§38). With
`DEMO_MODE=true` (the default):

- News, portfolio, briefing, AI answers and voice routing all use curated mock
  data and deterministic fallbacks.
- The full UI is functional for frontend development.

To go live, set `DEMO_MODE=false` and provide `TAVILY_API_KEY` (+ optionally an
LLM key).

---

## 11. Tavily configuration

The original Tavily agent is **preserved, not recreated** (§8) at
`backend/app/providers/tavily_agent.py`. It is wrapped by `TavilyNewsProvider`,
selected automatically when `DEMO_MODE=false` and `TAVILY_API_KEY` is set:

```bash
DEMO_MODE=false
TAVILY_API_KEY=tvly-...
```

You can still run the original agent standalone:
`uv run python -m app.providers.tavily_agent`.

---

## 12. Database setup

```bash
docker compose up -d postgres          # start Postgres
cd backend
uv run alembic upgrade head            # apply migrations
```

Create a new migration after model changes:
`uv run alembic revision --autogenerate -m "message"`.

---

## 13. Redis setup

```bash
docker compose up -d redis
```

Redis caches briefings and search results (§28). If Redis is unavailable, AOEN
degrades gracefully — a circuit breaker skips the cache so requests stay fast.

---

## 14. Voice setup

Voice uses the browser **Web Speech API** (STT + TTS), so no audio leaves the
device and the mic is active only while you hold the button (§22). Best support
is in Chrome/Edge. If unsupported, use the **Ask AOEN** text dock.

---

## 15. Testing

```bash
cd backend
uv run pytest                 # unit + integration tests
uv run ruff check app         # lint
uv run black --check app      # format check

cd ../frontend
npm run build                 # type-check + production build
```

---

## 16. Troubleshooting

| Symptom | Fix |
| ------- | --- |
| `uv sync` TLS error | `uv sync --native-tls` or set `UV_SYSTEM_CERTS=true` |
| `npm install` socket timeout | retry: `npm install --fetch-retries=6 --fetch-timeout=600000` |
| Port 8000 “forbidden” on Windows | reserved range — run on another port (`--port 8123`) |
| Briefing slow without Redis | expected once; the circuit breaker then skips Redis |
| Empty dashboard | never blank by design — check the backend is running and reachable |

---

## 17. Future architecture

AOEN is built to expand from **World Intelligence** into **Personal** and **Work**
intelligence (email, calendar, tasks, travel, fitness, GitHub, documents) as
independent agents/capabilities. Planned directions:

- **Local/hybrid LLMs** via the existing model abstraction (§45).
- **RAG knowledge layer** (documents, notes, email) behind the same agents (§46).
- **Scheduled automation** — morning/evening briefings and event alerts (§47).

---

## Product principles

Relevance over volume · Facts before interpretation · Source transparency ·
Personalization · User control · Extensibility · Privacy · Explainability.

**AOEN is informational only and does not provide investment advice.**
