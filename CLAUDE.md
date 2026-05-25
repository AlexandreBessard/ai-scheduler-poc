# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

AI-powered appointment scheduling POC. Customers describe what they need in natural language; a LangGraph + Claude agent books the appointment. Staff see all scheduled appointments in a separate admin view.

- **IDE:** PyCharm (JetBrains)
- **AWS region:** `eu-west-3` (Paris), profile: `default`

---

## Repository layout

```
ai-scheduler-poc/
├── frontend/          # Angular 21 monorepo (two apps)
├── backend/           # Python FastAPI + LangGraph agent
└── docker-compose.yml # PostgreSQL on port 5433
```

---

## Infrastructure

```bash
# Start PostgreSQL (port 5433 — 5432 is taken by a system PostgreSQL)
docker compose up -d
```

Credentials: user `scheduler`, password `scheduler`, database `scheduler`.

---

## Backend (`backend/`)

### Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set ANTHROPIC_API_KEY
```

### Commands

```bash
uvicorn app.main:app --reload --port 8000   # dev server → http://localhost:8000/docs
pytest                                       # all tests
pytest tests/path/to/test_file.py::test_fn  # single test
```

### Architecture

Two separate request paths — never mix them:

| Path | Route | Description |
|---|---|---|
| **Agent** | `POST /chat` | Client-app → LangGraph ReAct loop → SSE stream |
| **Direct** | `GET /appointments` | Admin-app → `appointment_service` directly, no agent |

**Agent flow (`/chat`):**
1. Request carries `{ message, thread_id }`. The `thread_id` (UUID per browser session) is the LangGraph checkpoint key — this is how multi-turn conversation and concurrent users are isolated.
2. The compiled graph (built once at startup in the FastAPI lifespan, stored on `app.state`) runs a ReAct loop: `agent_node` → `tools_node` → `agent_node` → … → `END`.
3. Response is streamed as SSE via `graph.astream_events()`.

**Key architectural rules:**
- Tools are thin: validate input, parse dates, delegate to `appointment_service`. No data logic in tools.
- `appointment_service` is the only layer that touches storage. Swapping in/out a database only requires changes there.
- The LangGraph graph is compiled **once** at startup — never per request.
- Tool docstrings are part of the prompt: Claude reads them to decide when/how to call each tool. Keep them precise.

**Date parsing:** `app/utils/date_parser.py` wraps `python-dateparser` with `PREFER_DATES_FROM: future`. Tools call `parse_datetime()` / `parse_date()` before passing values to the service. Claude may pass relative strings like `"tomorrow afternoon"` as tool arguments.

**Environment variables** (see `backend/.env.example`):

| Variable | Required | Default |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | — |
| `CLAUDE_MODEL` | No | `claude-sonnet-4-6` |
| `DATABASE_URL` | Yes | `postgresql+asyncpg://scheduler:scheduler@localhost:5433/scheduler` |
| `CORS_ORIGINS` | No | `["http://localhost:4200","http://localhost:4201"]` |

---

## Frontend (`frontend/`)

Angular 21 monorepo. Both apps are standalone components (no NgModules).

| App | Port | Entry component | Purpose |
|---|---|---|---|
| `client-app` | 4200 | `SchedulingPrompt` | Customer chat UI |
| `admin-app` | 4201 | `AppointmentList` | Staff appointment dashboard |

### Commands

```bash
cd frontend
ng serve client-app                # http://localhost:4200
ng serve admin-app --port 4201     # http://localhost:4201
ng build client-app
ng build admin-app
ng test client-app
ng test admin-app
```

### Architecture

- Each app has a single route `/` pointing to its root component. Root `app.html` is just `<router-outlet />`.
- **`client-app/SchedulingPrompt`** — chat interface. Generates a `threadId` via `crypto.randomUUID()` on component init (displayed top-right as a session badge). `send()` must pass `{ message, threadId }` to `POST /chat` and stream the SSE response. Currently uses a placeholder `setTimeout`.
- **`admin-app/AppointmentList`** — appointment table with status badges. Data is hardcoded; replace with a call to `GET /appointments`.
- **Keycloak** not wired up yet. When added, guard both apps via `app.routes.ts`.
- **Shared code** (models, API services, auth guard) → `ng generate library shared` under `frontend/projects/shared/`.
