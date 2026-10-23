# Design

## Context

See `proposal.md` — Why. The backend currently has a single `/health` route, no configuration module, no database session, and no migrations; `sqlalchemy`, `psycopg2-binary`, and `pydantic-settings` are declared but unused. PostgreSQL 16 already runs in `docker-compose.yml`, and CI builds the backend image but never runs it against a database.

The requirements this design implements are in `specs/event-catalog/spec.md`. This document records only the technical choices that are not obvious from those requirements.

## Goals / Non-Goals

**Goals:**

- Establish the backend layering, configuration, migration, and test patterns that later features reuse.
- Make `docker compose up` produce a working, migrated, seeded-capable API.
- Keep the API contract stable enough that the follow-up UI change does not require breaking changes.

**Non-Goals:**

- Authentication, authorization, or organizer identity.
- Event creation, editing, publishing, or deletion.
- Ticket purchase, capacity reservation, or check-in.
- Frontend work; the catalog UI is a separate change.
- Production backend deployment or least-privilege database users.

## Decisions

### D1: Backend foundation plus one read capability

**Decision:** Deliver the foundation (config, DB session, Alembic, test harness) together with the read-only `event-catalog` capability rather than as a standalone infrastructure change.

**Rationale:** A foundation-only change has almost no observable behavior to specify, so it would not exercise the `specs` artifact. Pairing it with the first read endpoint gives the spec real scenarios while keeping the UI out of scope.

**Alternatives considered:**
- Infrastructure-only change first — rejected: thin spec, and the foundation would be validated only by "the app boots".
- Backend + frontend in one change — rejected: mixes API and UI concerns and doubles the review surface.

### D2: Event model

**Decision:** A single `events` table.

| column | type | constraints |
|---|---|---|
| `id` | `UUID` | primary key, Python-side `uuid4` default |
| `title` | `varchar(200)` | not null |
| `description` | `text` | nullable |
| `venue` | `varchar(200)` | not null |
| `starts_at` | `timestamptz` | not null, stored UTC |
| `capacity` | `integer` | not null, `> 0` |
| `status` | `varchar(16)` | not null, `CHECK (status IN ('draft','published'))`, default `draft` |
| `created_at` | `timestamptz` | not null, server default `now()` |
| `updated_at` | `timestamptz` | not null, server default `now()`, updated on change |

Index: `(status, starts_at)` for the list query.

**Rationale:** UUIDs avoid enumerable public ids and will be referenced by orders and tickets. A `varchar` + CHECK is cheaper to evolve than a native PostgreSQL enum (`ALTER TYPE` is awkward). Timezone-aware timestamps stored in UTC prevent a class of bugs that is expensive to fix after ticket times exist.

**Alternatives considered:**
- Serial integer ids — rejected: enumerable and harder to expose publicly.
- Native PG enum — rejected: migration friction for a course project.
- `timestamp` without timezone — rejected: local-time ambiguity.
- Adding `price`, `ends_at`, `organizer_id`, or a `Venue` entity now — rejected: would pre-commit the purchase spec.

### D3: API contract

**Decision:** Versioned prefix `/api/v1`.

- `GET /api/v1/events?limit=20&offset=0` returns `{items, total, limit, offset}`.
- `GET /api/v1/events/{id}` returns a bare event object.
- Ordering is `starts_at ASC, id ASC`.
- `limit` default 20, range 1–100; `offset` default 0, minimum 0.

**Rationale:** The envelope makes `total` available and avoids a breaking change when pagination is added later. Ordering by `(starts_at, id)` makes offset paging deterministic when events share a start time. The detail endpoint has no collection semantics, so a bare object is simpler for the client.

**Alternatives considered:**
- Bare array for the list — rejected: adding pagination later would break every client.
- Cursor pagination — rejected: composite cursor complexity with no concurrency need at this scale.
- `limit`/`offset` as form or header parameters — rejected: query parameters are conventional and visible in OpenAPI.

### D4: Upcoming filter on the list only

**Decision:** The list filters `starts_at >= now()`; the detail endpoint does not filter on time.

**Rationale:** A public catalog that shows past events looks broken, while a deep link to an event that just started should keep working. Keeping detail time-independent also avoids a race where a page 404s exactly at start time.

**Alternatives considered:**
- No time filter — rejected: the UI would filter client-side, moving a product rule out of the API.
- Time filter on detail too — rejected: breaks bookmarked/ongoing event pages.
- `?include_past=true` now — rejected: additive later; no current consumer.

### D5: Default FastAPI error shape

**Decision:** Use FastAPI's default errors: `404 {"detail": "Event not found"}` and standard 422 validation responses. Draft and unknown ids return the same 404 body.

**Rationale:** One UI consumer reads one endpoint; a custom envelope adds handlers and schemas without a current need. Identical 404s for draft and unknown prevent leaking unpublished events.

**Alternatives considered:**
- Custom `{error: {code, message}}` envelope — rejected as speculative; additive later if clients need codes.

### D6: Router plus service module, no repository

**Decision:** `api/v1/events.py` handles HTTP concerns; `services/events.py` owns the published/upcoming/ordering/pagination rules and returns domain objects or `None`. The router maps `None` to 404.

**Rationale:** The spec asserts the query rules, so they should be testable without HTTP. A repository interface with one implementation and one caller is ceremony at this stage; it can be extracted later without changing the service signature.

**Alternatives considered:**
- Queries inline in the router — rejected: mixes HTTP and domain rules.
- Router → service → repository — rejected: three hops for two read queries.

### D7: Migrations via a one-shot compose service

**Decision:** Alembic owns the schema. A `migrate` service runs `alembic upgrade head` once; `backend` waits on `db` health and `migrate` completion.

**Rationale:** Running migrations inside the app command makes every start a schema operation and races with multiple workers. A manual step is easy to forget and fails as a 500 on `/events`.

**Alternatives considered:**
- Migrations in the app entrypoint — rejected: couples schema changes to process start.
- Manual `docker compose exec backend alembic upgrade head` — rejected: violates the one-command local promise.
- `Base.metadata.create_all` at startup — rejected: no migration history, no rollback.

### D8: Required configuration

**Decision:** `Settings` requires `database_url` (no default). Compose supplies it via `${DATABASE_URL:-postgresql://ticketin:ticketin@db:5432/ticketin}`; `.env.example` uses host `db` and adds `TEST_DATABASE_URL`. Compose auto-loads a root `.env` for interpolation; no `env_file` mount.

**Rationale:** A baked-in `localhost` default is exactly the bug the current `.env.example` has — it works on the host and fails in a container. Required settings fail fast and visibly.

**Alternatives considered:**
- Default connection string in `Settings` — rejected: hides misconfiguration.
- Mounting `.env` with `env_file` — rejected: extra mount and errors when the file is absent.
- Reading `.env` from the repo root inside the container — rejected: only `./backend` is mounted at `/app`.

### D9: PostgreSQL for tests

**Decision:** Tests use a separate `ticketin_test` database on the same PostgreSQL server. A session fixture creates the database if missing and runs `alembic upgrade head`; each test runs in a transaction that is rolled back.

**Rationale:** The locked model relies on UUID, `timestamptz`, and CHECK constraints, so SQLite would test different behavior. Running Alembic in the fixture means a broken migration fails tests instead of shipping green.

**Alternatives considered:**
- SQLite — rejected: dialect divergence and untested migrations.
- Dedicated `db-test` container — rejected: duplicate compose/CI wiring for no behavioral gain.
- `Base.metadata.create_all` in tests — rejected: bypasses migrations.
- Truncating tables between tests — rejected: slower than transaction rollback.

### D10: Idempotent seed command

**Decision:** `python -m app.seed` inserts four demo events with fixed UUIDs via `session.merge`. It is never invoked at application startup and is not used by tests.

Demo rows: two published upcoming events (`now + 7d`, `now + 14d`), one draft (`now + 21d`), one past published (`now - 7d`).

**Rationale:** The read-only API needs rows for local development and the upcoming UI change. Fixed UUIDs make re-running the command safe. The four rows exercise every locked list rule.

**Alternatives considered:**
- Alembic data migration — rejected: demo data would run in every environment.
- Startup seeding — rejected: hidden side effects and races.
- SQL init script — rejected: bypasses the app and only runs on first volume creation.

### D11: DB-aware health endpoint

**Decision:** `GET /health` runs `SELECT 1` through the session dependency. Success returns `200 {"status":"ok","database":"ok"}`; failure returns `503 {"status":"degraded","database":"unreachable"}`. The compose probe uses Python's `urllib.request` instead of `curl`.

**Rationale:** A backend reporting healthy while the database is down hides the failure the scaffold should surface. `python:3.12-slim` has no `curl`, so the current probe can never pass.

**Alternatives considered:**
- Liveness-only health — rejected: no database signal.
- Separate `/health/live` and `/health/ready` — rejected: two endpoints and probes for a single-process course deployment.
- Installing `curl` in the image — rejected: unnecessary package for a one-line probe.

### D12: CI uses a PostgreSQL service in the backend job

**Decision:** Add a health-checked `postgres:16-alpine` service to the existing backend job, set `DATABASE_URL`/`TEST_DATABASE_URL`, run `alembic upgrade head`, then lint, typecheck, and test. `alembic` moves to main dependencies.

**Rationale:** Reuses the existing job and matches the local database version. The service user is a superuser, so the test fixture can create `ticketin_test`. Alembic in main dependencies keeps the `migrate` service working if the image is built without dev extras.

**Alternatives considered:**
- Separate integration job — rejected: duplicates setup for no benefit.
- `docker compose` in CI — rejected: image builds before tests roughly double feedback time.
- Testcontainers — rejected: Docker-in-Docker complexity.

## Risks / Trade-offs

- [Time-dependent tests can flake near midnight or on slow machines] → tests create events relative to `now` (`+1 day`, `-1 day`) rather than at exact boundaries; no clock mocking needed.
- [One-shot `migrate` may not re-run on every `docker compose up` after new migrations] → document `docker compose run --rm migrate` when pulling schema changes.
- [Test fixture needs `CREATE DATABASE` privilege] → acceptable while `ticketin` is the compose/CI superuser; if a least-privilege user is introduced, pre-create `ticketin_test` and drop the create step.
- [Upcoming filter hides an event exactly at `starts_at`] → accepted; detail remains reachable and an archive view can be added additively.
- [`total` adds a second `COUNT(*)` query] → accepted at catalog scale; revisit with an index-only count or caching if needed.
- [Moving `alembic` to main dependencies slightly increases the image] → accepted; migrations are an operational concern of the image.

## Migration Plan

1. Add `alembic` and generate the initial migration for `events`.
2. Add the `migrate` service; `backend` waits for it.
3. `docker compose up --build` creates the schema, then starts the API.
4. Run `docker compose exec backend python -m app.seed` to load demo rows.
5. Rollback: `alembic downgrade base` drops `events`; there is no existing data to preserve.
6. No backend deployment exists; frontend and Pages are unaffected.

## Open Questions

None blocking. Pagination performance and an archive view are deferred to future changes.
