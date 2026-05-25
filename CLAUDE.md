# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

An AI-powered appointment scheduling POC. Customers describe what they need in natural language; the system schedules the appointment. Staff see scheduled appointments in a separate admin view.

## Environment

- **Language:** Python (backend — not yet scaffolded)
- **AWS region:** `eu-west-3` (Paris), AWS profile: `default`
- **IDE:** IntelliJ / PyCharm

## Frontend (`frontend/`)

Angular 21 monorepo workspace with two standalone apps:

| App | Port | Purpose |
|---|---|---|
| `client-app` | 4200 (default) | Customer chat-style prompt to request an appointment |
| `admin-app` | 4201 | Staff dashboard listing all scheduled appointments |

### Key commands

```bash
cd frontend

# Serve
ng serve client-app               # http://localhost:4200
ng serve admin-app --port 4201    # http://localhost:4201

# Build
ng build client-app
ng build admin-app

# Test
ng test client-app
ng test admin-app
```

### Architecture

- Both apps are **standalone components** (no NgModules).
- Routing: each app has its own `app.routes.ts`; the root component is just `<router-outlet />`.
- **`client-app`** — single route `/` → `SchedulingPrompt`: a chat interface where the user types a natural-language request. The `send()` method currently uses a placeholder `setTimeout`; replace it with a real API call to the backend.
- **`admin-app`** — single route `/` → `AppointmentList`: a table of appointments with status badges. Data is hardcoded in the component; replace with a real API service.
- **Keycloak** is intentionally not wired up yet. When added, guard both apps with an auth guard in their respective `app.routes.ts`.
- **Shared code** (models, API services, auth) should go in a library under `frontend/projects/shared/` when needed (`ng generate library shared`).
