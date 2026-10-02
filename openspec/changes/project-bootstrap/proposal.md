## Why

The project needs a clean, professional development workflow from day one. As a 2-4 person university course team building an event ticketing system, we need the full collaboration workflow validated end-to-end before any feature work begins. This bootstrap proves the pipeline works with minimal code — real feature specs come later.

## What Changes

- Git repo initialized with remote (`ticketin`, public, personal account)
- Monorepo structure with `frontend/` (React + Vite) and `backend/` (FastAPI) folders
- Minimal backend: single `GET /health` endpoint returning `{"status": "ok"}` — proves lint, typecheck, test, and Docker build
- Minimal frontend: single component rendering "Hello from ticketin" — proves lint, typecheck, test, Docker build, and deploy
- Docker strategy: `docker-compose.yml` for local dev (frontend + backend + PostgreSQL with volume mounts for live reload), individual `Dockerfile`s for each service
- Docker-only development: all tools and dependencies run inside containers, no local host installs (only Docker required)
- GitHub Actions CI pipeline: lint, typecheck, test, and Docker build verification on every push and PR
- GitHub Actions deploy workflow: frontend builds and deploys to GitHub Pages on merge to main
- Branch protection on `main`: require PR, CI pass, 1 approval, up-to-date branch, no direct pushes
- Conventional Commits convention (`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`)
- PR template with description, testing, and screenshot sections
- Pre-commit hooks (ruff for backend, eslint for frontend) — run via `docker compose exec`
- Spec-driven development workflow using OpenSpec (proposal -> design -> specs -> tasks -> implement)

## Capabilities

### New Capabilities

(none — this is a tooling/workflow bootstrap with no spec-level behavior changes)

### Modified Capabilities

(none — greenfield project)

## Impact

- New repository `ticketin` on GitHub (public, personal account)
- GitHub repository settings (branch protection rules)
- GitHub Actions workflows (CI and deploy)
- Docker configuration for local development and CI
- No existing code or systems affected (greenfield)
- Implementation done incrementally: each phase is a separate PR demonstrating the workflow
