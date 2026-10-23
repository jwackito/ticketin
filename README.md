# ticketin

Event ticketing system built with FastAPI + React + PostgreSQL.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** React, Vite, TypeScript
- **Infrastructure:** Docker, GitHub Actions, GitHub Pages

## Quickstart

### Prerequisites

- Docker
- Docker Compose

### Local Development

```bash
docker compose up
```

This starts:
- Frontend dev server (with HMR)
- Backend API (with auto-reload)
- PostgreSQL database

### Docker-Only Workflow

All development tools run inside Docker containers. No local installs required.

```bash
# Run backend linting
docker compose exec backend ruff check .

# Run backend type checking
docker compose exec backend mypy .

# Run backend tests
docker compose exec backend pytest

# Run frontend linting
docker compose exec frontend npm run lint

# Run frontend type checking
docker compose exec frontend npx tsc --noEmit

# Run frontend tests
docker compose exec frontend npx vitest run
```

### Database Migrations

Schema changes are managed with Alembic. `docker compose up` applies migrations
automatically through the one-shot `migrate` service, before the backend starts.

```bash
# Apply migrations manually
docker compose run --rm migrate

# Create a new migration after changing a model
docker compose exec backend alembic revision --autogenerate -m "describe change"
```

### Seed Data

Load demo events (idempotent, safe to re-run):

```bash
docker compose exec backend python -m app.seed
```

### API

The event catalog is versioned under `/api/v1`.

```bash
curl http://localhost:8000/health
# {"status":"ok","database":"ok"}

curl "http://localhost:8000/api/v1/events?limit=20&offset=0"
# {"items":[...],"total":2,"limit":20,"offset":0}

curl http://localhost:8000/api/v1/events/<id>
# the event object, or 404 {"detail":"Event not found"}
```

Interactive docs are served at http://localhost:8000/docs.

## Development Workflow

1. Create a feature branch from `main`
2. Make changes, commit using [Conventional Commits](https://www.conventionalcommits.org/)
3. Push branch and open a Pull Request
4. CI runs automatically (lint, typecheck, test, build)
5. Ensure CI is green and the branch is up to date (no approval required for the solo maintainer)
6. Squash merge to `main`
7. Frontend auto-deploys to GitHub Pages

### Workflow enforcement

Branch protection on `main` requires a pull request and the `backend`, `frontend`, and
`docker` status checks. Direct pushes and force pushes are rejected for everyone,
including the repository owner, so all changes go through a pull request.

To catch a mistake locally before it reaches GitHub, enable the pre-push hook:

```bash
git config core.hooksPath .githooks
```

The hook is a convenience only; the server-side protection is the real gate. It requires an
executable filesystem — on a `noexec` mount git skips it.

### Commit Convention

Commits follow [Conventional Commits](https://www.conventionalcommits.org/). Allowed types:

| Type | Use for |
|---|---|
| `feat` | a new feature |
| `fix` | a bug fix |
| `docs` | documentation only |
| `test` | adding or fixing tests |
| `refactor` | a change that neither fixes a bug nor adds a feature |
| `style` | formatting only |
| `perf` | a performance improvement |
| `ci` | CI configuration |
| `build` | build system or dependencies |
| `chore` | other changes that do not touch source or tests |

Example: `feat: add read-only event catalog API`

### Pre-commit Lint Checks

There is no pre-commit framework and nothing is installed on the host. Run the
container linters before committing:

```bash
docker compose exec backend ruff check .
docker compose exec frontend npm run lint
```

CI runs the same checks plus type checking and tests, and it is the enforcement
gate, so a skipped local check is caught on the pull request.

### Spec-Driven Development

Features are developed with OpenSpec in `openspec/`, following
proposal -> design -> specs -> tasks -> implement.

```bash
openspec list                      # list active changes
openspec show <change>             # read a change
openspec validate <change> --strict
openspec archive <change>          # after implementation and review
```

Create a new change with `openspec new change "<name>"` and capture its artifacts
before writing code. Changes live in `openspec/changes/` until archived.

## Project Structure

```
ticketin/
  frontend/          React + Vite
  backend/           FastAPI
  docker-compose.yml Local dev orchestration
  .github/
    workflows/       CI and deploy pipelines
```

## License

MIT
