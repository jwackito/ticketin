## Why

The bootstrap proved the tooling works but the application has no domain behavior — the backend serves only `GET /health` and the declared database stack is unused. This change delivers the first real vertical slice: a read-only event catalog API. It validates the full spec-driven workflow (proposal → design → specs → tasks) with observable behavior, and establishes the `Event` model and backend foundation that later features (organizer writes, ticket purchase, check-in) will build on.

## What Changes

- Add backend foundation: `pydantic-settings` configuration, SQLAlchemy 2.0 engine/session, Alembic migrations, and a test harness against PostgreSQL.
- Add an `Event` model and migration: `id`, `title`, `description`, `venue`, `starts_at`, `capacity`, `status` (`draft`/`published`), `created_at`, `updated_at`.
- Add read-only catalog endpoints:
  - `GET /api/v1/events` — published, upcoming events with limit/offset pagination.
  - `GET /api/v1/events/{id}` — published event detail, time-independent.
- Add a one-shot `migrate` compose service so `docker compose up` creates the schema before the API starts.
- Make `GET /health` report database reachability and fix the compose healthcheck to avoid `curl`.
- Add an idempotent seed command (`python -m app.seed`) with demo events for local development.
- Add a PostgreSQL service to the backend CI job and run migrations before tests.
- Fix environment configuration: required `DATABASE_URL`, `TEST_DATABASE_URL`, and `.env.example` host `db`.

Not included: authentication, event creation/editing, ticket purchase, capacity enforcement, and the frontend catalog UI (separate change `event-catalog-ui`).

## Capabilities

### New Capabilities

- `event-catalog`: public read-only access to published, upcoming events, including listing with pagination and retrieving a single event by id.

### Modified Capabilities

(none — no existing capability requirements change)

## Impact

- Backend: new `app/core`, `app/db`, `app/models`, `app/schemas`, `app/services`, and `app/api/v1` modules; `app/main.py` gains routers; `app/seed.py` added.
- Dependencies: `alembic` added to main dependencies.
- Database: first Alembic migration; no changes to existing tables.
- Infrastructure: `docker-compose.yml` gains a `migrate` service and environment wiring; `.env.example` updated.
- CI: backend job gains a PostgreSQL service container and a migration step.
- API: two new versioned endpoints and a DB-aware health response.
- Frontend: no changes in this change.
- Documentation: README gains migration, seed, and API usage notes.
