# Tasks

## 1. Backend foundation and test harness

- [ ] 1.1 Add `alembic` to the main dependencies in `backend/pyproject.toml` and verify `docker compose build backend` succeeds and `alembic --version` runs inside the container.
- [ ] 1.2 Create `backend/app/core/config.py` with a `Settings` model requiring `database_url` and a cached `get_settings()`, and verify it raises a validation error when `DATABASE_URL` is unset and loads when it is set.
- [ ] 1.3 Create `backend/app/db/base.py` and `backend/app/db/session.py` with the engine, `SessionLocal`, and `get_db`, and verify a `SELECT 1` through `get_db` succeeds against the compose PostgreSQL.
- [ ] 1.4 Initialize Alembic (`backend/alembic.ini`, `backend/alembic/env.py`) wired to `Settings` and `Base.metadata`, and verify `alembic current` runs against the dev database.
- [ ] 1.5 Update `.env.example` (host `db`, add `TEST_DATABASE_URL`) and compose interpolation for both URLs, and verify `docker compose config` shows the resolved values.
- [ ] 1.6 Add `backend/tests/conftest.py` that creates `ticketin_test` when missing, runs `alembic upgrade head`, and rolls back each test's transaction, and verify a sample database test passes with `pytest`.
- [ ] 1.7 Document backend setup (migrations and tests) in `README.md` and verify the documented commands run as written.

## 2. Event model and migration

- [ ] 2.1 Create `backend/app/models/event.py` with the columns, CHECK constraints, index, and defaults from design D2, and verify the module imports and passes `mypy`.
- [ ] 2.2 Generate the initial migration in `backend/alembic/versions/` and verify `alembic upgrade head` and `alembic downgrade base` both succeed.
- [ ] 2.3 Add model tests for `capacity > 0` and the `status` CHECK constraint, and verify `pytest tests/test_models.py` passes.

## 3. Event schemas, service, and API

- [ ] 3.1 Create `backend/app/schemas/event.py` with `EventRead` and `EventPage`, and verify a unit test serializes an ORM event and a page envelope correctly.
- [ ] 3.2 Create `backend/app/services/events.py` with `list_published` (published + upcoming filter, ordering, pagination, total) and `get_published`, and verify service tests cover draft/past exclusion, ordering, and time-independent detail.
- [ ] 3.3 Create `backend/app/api/v1/events.py` with both endpoints and `None` → 404, wire the router into `app/main.py` under `/api/v1`, and verify the OpenAPI document exposes both paths.
- [ ] 3.4 Add API tests for listing: default page, explicit page, offset past end, empty catalog, ordering, and 422 on invalid `limit`/`offset`, and verify they pass.
- [ ] 3.5 Add API tests for detail: published, past published, draft 404, unknown 404, and malformed UUID 422, and verify they pass.
- [ ] 3.6 Document the catalog endpoints in `README.md` with example requests and responses, and verify the examples match actual responses.

## 4. Health and compose orchestration

- [ ] 4.1 Make `GET /health` run `SELECT 1` and return the 200/503 responses from design D11, and verify tests cover both outcomes.
- [ ] 4.2 Replace the compose healthcheck `curl` with the stdlib Python probe and verify the backend reports healthy in `docker compose ps`.
- [ ] 4.3 Add the one-shot `migrate` service and make `backend` wait on `service_completed_successfully`, and verify a clean `docker compose up` creates the schema before the API starts.
- [ ] 4.4 Document the migration workflow, including `docker compose run --rm migrate`, in `README.md` and verify the commands run as written.

## 5. Seed data

- [ ] 5.1 Create `backend/app/seed.py` with the four fixed-UUID demo events and `session.merge`, and verify `docker compose exec backend python -m app.seed` inserts them.
- [ ] 5.2 Add a seed idempotency test that runs the seed twice and asserts the event count is unchanged, and verify it passes.
- [ ] 5.3 Document the seed command in `README.md` and verify it runs as written.

## 6. CI

- [ ] 6.1 Add the health-checked PostgreSQL service, `DATABASE_URL`/`TEST_DATABASE_URL`, and an `alembic upgrade head` step to the backend job in `.github/workflows/ci.yml`, and verify the YAML parses and the same commands pass locally.
- [ ] 6.2 Push a branch and open a pull request, then verify the backend job runs migrations and tests against PostgreSQL and all required checks pass.

## 7. Integration verification

- [ ] 7.1 From a clean volume, run `docker compose up --build`, seed the database, and verify `GET /health`, `GET /api/v1/events`, `GET /api/v1/events/{id}`, and the 404 cases against the running stack.
- [ ] 7.2 Run `docker compose exec backend ruff check .`, `docker compose exec backend mypy .`, and `docker compose exec backend pytest`, and verify all pass.
- [ ] 7.3 Run `openspec validate event-catalog-api --strict` and verify it passes.

## Workflow follow-up

- Archive this change after the review requirements are satisfied.
- Keep `project-bootstrap` open until its own implementation gaps are verified.
