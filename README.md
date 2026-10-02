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

## Development Workflow

1. Create a feature branch from `main`
2. Make changes, commit using [Conventional Commits](https://www.conventionalcommits.org/)
3. Push branch and open a Pull Request
4. CI runs automatically (lint, typecheck, test, build)
5. Get 1 approval, ensure CI is green and branch is up to date
6. Squash merge to `main`
7. Frontend auto-deploys to GitHub Pages

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
