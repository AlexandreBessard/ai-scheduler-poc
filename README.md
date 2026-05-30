# AI Appointment Scheduler — POC

An AI-powered appointment scheduling proof-of-concept. Customers describe what they need in plain language; a [LangGraph](https://github.com/langchain-ai/langgraph) + Claude agent interprets the request, checks availability, and books the appointment. Staff manage everything through a separate admin dashboard.

---

## Demo

| Customer chat | Admin dashboard |
|---|---|
| Customer types *"I'd like a haircut next Tuesday around 10am"* | Staff see all appointments with live status badges |
| Agent reasons, checks slots, confirms the booking | Direct read from the service layer — no AI overhead |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Angular monorepo (frontend/)                           │
│                                                         │
│  client-app :4200          admin-app :4201              │
│  ┌─────────────────┐       ┌─────────────────────────┐  │
│  │ SchedulingPrompt│       │   AppointmentList       │  │
│  └────────┬────────┘       └───────────┬─────────────┘  │
└───────────┼────────────────────────────┼────────────────┘
            │  POST /chat (SSE)          │  GET /appointments
            ▼                            ▼
┌─────────────────────────────────────────────────────────┐
│  FastAPI backend (backend/)  :8000                      │
│                                                         │
│  /chat ──► LangGraph ReAct agent                        │
│                │                                        │
│                ├── agent_node (Claude + tools)          │
│                └── tools_node                           │
│                      ├── check_availability             │
│                      ├── book_appointment               │
│                      ├── list_appointments              │
│                      └── cancel_appointment             │
│                                                         │
│  /appointments ──► appointment_service (direct, no AI)  │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
                    PostgreSQL :5433
                    (Docker Compose)
```

The LangGraph graph is compiled **once at startup** and shared across all requests. Each browser session gets a unique `threadId` that acts as the LangGraph checkpoint key, preserving conversation history across turns.

---

## Tech stack

| Layer | Technology |
|---|---|
| LLM | Claude (`claude-sonnet-4-6`) via `langchain-anthropic` |
| Agent orchestration | LangGraph `StateGraph` (ReAct loop) |
| API | FastAPI + Uvicorn |
| Date parsing | `python-dateparser` (natural language → `datetime`) |
| Config | `pydantic-settings` |
| Frontend | Angular 21 (standalone components, no NgModules) |
| Database | PostgreSQL 16 via Docker Compose |

---

## Quickstart

### Prerequisites

- Docker
- Python 3.11+
- Node.js 20+ / npm 10+
- An [Anthropic API key](https://console.anthropic.com/)

### 1 — Start the database

```bash
docker compose up -d
```

PostgreSQL is now available on **port 5433** (5432 is reserved for any system Postgres).
Credentials: `scheduler / scheduler`, database `scheduler`.

### 2 — Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then open .env and set ANTHROPIC_API_KEY
uvicorn app.main:app --reload --port 8000
```

API → `http://localhost:8000`  
Interactive docs → `http://localhost:8000/docs`

### 3 — Start the frontend apps

```bash
cd frontend
npm install

# In two separate terminals:
ng serve client-app               # http://localhost:4200  (customer chat)
ng serve admin-app --port 4201    # http://localhost:4201  (admin dashboard)
```

---

## Environment variables

Defined in `backend/.env` (copy from `backend/.env.example`).

| Variable | Required | Default |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | — |
| `CLAUDE_MODEL` | No | `claude-sonnet-4-6` |
| `DATABASE_URL` | No | `postgresql+asyncpg://scheduler:scheduler@localhost:5433/scheduler` |
| `CORS_ORIGINS` | No | `["http://localhost:4200","http://localhost:4201"]` |
| `ENV` | No | `development` |

---

## Project structure

```
ai-scheduler-poc/
├── backend/
│   ├── app/
│   │   ├── agent/          # LangGraph graph, nodes, state
│   │   ├── api/routes/     # /chat (SSE) and /appointments
│   │   ├── models/         # Pydantic domain models
│   │   ├── services/       # appointment_service (only layer that touches storage)
│   │   ├── tools/          # LangChain @tool functions (thin wrappers)
│   │   └── utils/          # date_parser.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   └── projects/
│       ├── client-app/     # Customer chat UI (port 4200)
│       └── admin-app/      # Staff dashboard (port 4201)
├── docker-compose.yml
└── CLAUDE.md
```

---

## Running tests

```bash
cd backend
pytest                                        # all tests
pytest tests/path/to/test_file.py::test_name  # single test
```

```bash
cd frontend
ng test client-app
ng test admin-app
```

---

## Key design decisions

**Two separate request paths** — the customer chat goes through the LangGraph agent; the admin dashboard reads directly from `appointment_service`. This keeps the admin view fast and deterministic with no AI latency or cost.

**Tools are thin** — each tool validates input, parses dates, then delegates to `appointment_service`. All data logic lives in the service layer; swapping storage only requires changes there.

**Thread isolation** — the Angular client generates a `threadId` (UUID) per session. LangGraph uses this as the checkpoint key, so conversation history is preserved across turns and concurrent users never share state.

**Graph compiled once** — `build_graph()` is called in the FastAPI lifespan and stored on `app.state`. No per-request compilation overhead.
