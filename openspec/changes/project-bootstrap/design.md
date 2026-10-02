## Context

Greenfield project. No existing code, no existing CI/CD, no existing conventions. The team is 2-4 developers building an event ticketing system for a university software engineering course. Stack is decided: FastAPI + React + PostgreSQL/SQLAlchemy, everything dockerized, frontend deployed to GitHub Pages, backend runs in CI and local docker-compose only. This is a **minimal bootstrap** — the goal is to validate the full workflow end-to-end with minimal code, not to build the application. Real feature specs come later. See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Validate the entire development workflow end-to-end with minimal code
- Establish a monorepo structure that supports independent frontend and backend development
- CI pipeline that gates every PR on lint, typecheck, test, and Docker build
- Automated frontend deployment to GitHub Pages on merge to main
- Local development environment reproducible with a single `docker compose up`
- Branch protection that enforces the workflow without blocking the team
- Conventional Commits, PR template, and pre-commit hooks to standardize contributions
- Spec-driven development workflow using OpenSpec
- Implementation done incrementally: each phase is a separate PR demonstrating the workflow

**Non-Goals:**
- Building the actual event ticketing application (features come later)
- Backend deployment to a public host (CI + local only)
- Kubernetes, Helm, or any orchestration beyond docker-compose
- Multi-environment staging (single `main` branch deploys to production)
- Feature flags or trunk-based development
- Release branching or semantic versioning automation

## Decisions

### D1: Monorepo with shared access (not forks)

**Decision:** Single repository, all developers are collaborators, feature branches + PRs to main.

**Rationale:** For a 2-4 person trusted team, forks add sync overhead without benefit. Shared access simplifies coordination, visibility, and CI.

**Alternatives considered:**
- Fork-based workflow — rejected: unnecessary complexity for a small trusted team
- Multiple repos (frontend + backend) — rejected: harder to coordinate cross-cutting changes, split CI, split issues/PRs

### D2: GitHub Flow (feature branches + PRs to main)

**Decision:** Short-lived feature branches from main, PR back to main, squash merge.

**Rationale:** Simple, industry-standard, works well for small teams. No release branches needed for a course project.

**Alternatives considered:**
- Git Flow (develop/release/main) — rejected: too much ceremony for 2-4 people
- Trunk-based (direct to main with feature flags) — rejected: branch protection with PRs is a course requirement

### D3: Docker strategy — docker-compose for local, Dockerfiles for CI

**Decision:** Each service has its own `Dockerfile`. Root `docker-compose.yml` orchestrates frontend + backend + PostgreSQL for local dev. CI builds each image independently to verify they work.

**Rationale:** Dockerfiles are needed for CI image builds and potential future deployment. docker-compose provides a one-command local environment. Keeping them separate avoids coupling local dev to CI.

**Alternatives considered:**
- Single Dockerfile for everything — rejected: harder to develop, slower builds
- docker-compose only (no standalone Dockerfiles) — rejected: CI needs to build images independently

### D4: CI pipeline — parallel jobs for backend and frontend

**Decision:** GitHub Actions workflow with separate jobs for backend (ruff, mypy, pytest) and frontend (eslint, tsc, vitest), plus a Docker build verification job. All run on every push and PR.

**Rationale:** Parallel jobs give fast feedback. Separate jobs make it clear which service failed. Docker build verification ensures images are buildable.

**Alternatives considered:**
- Single job running everything — rejected: slower, harder to debug
- CI only on PR (not on push) — rejected: catching issues before PR is better

### D5: Frontend deployment to GitHub Pages via GitHub Actions

**Decision:** On merge to main, a workflow builds the React app and deploys to GitHub Pages using the `actions/deploy-pages` action.

**Rationale:** GitHub Pages is free, integrated with GitHub, and sufficient for a static React frontend. No backend deployment needed.

**Alternatives considered:**
- Manual build and push to `gh-pages` branch — rejected: error-prone, not automated
- Netlify/Vercel — rejected: external service, unnecessary for a course project

### D6: Branch protection rules

**Decision:** On `main`: require PR, require CI pass, require 1 approval, require up-to-date branch, no direct pushes, no force pushes.

**Rationale:** Enforces the workflow without being overly restrictive. 1 approval is sufficient for a 2-4 person team.

**Alternatives considered:**
- 2 approvals — rejected: too slow for a small team
- No branch protection — rejected: course requirement, and it's a good practice

### D7: Conventional Commits

**Decision:** Enforce commit message format: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`, `style:`, `perf:`, `ci:`, `build:`.

**Rationale:** Standard format, enables changelog generation, looks professional for a course project.

**Alternatives considered:**
- No convention — rejected: inconsistent history, harder to read
- Custom format — rejected: no reason to invent a new one

### D8: Pre-commit hooks

**Decision:** Use `pre-commit` framework with ruff (backend) and eslint (frontend) hooks. Run via `docker compose exec` — no local pre-commit install.

**Rationale:** Catches lint issues before CI, faster feedback, teaches good habits. Running via docker aligns with the Docker-only workflow (D10).

**Alternatives considered:**
- No pre-commit hooks — rejected: CI-only feedback is slower
- Husky (JS-focused) — rejected: backend is Python, need a language-agnostic solution
- Local pre-commit install — rejected: violates Docker-only workflow (D10)

### D9: Spec-driven development with OpenSpec

**Decision:** Use OpenSpec workflow for feature development: proposal -> design -> specs -> tasks -> implement.

**Rationale:** Course requirement, teaches spec-first thinking, integrates with the project's OpenSpec setup.

**Alternatives considered:**
- Ad-hoc development — rejected: course requirement
- Other spec tools — rejected: OpenSpec is already scaffolded

### D10: Docker-only development environment (no local host installs)

**Decision:** All development tools and dependencies run inside Docker containers. The only local requirement is Docker itself. No Python packages, Node packages, or CLI tools (ruff, mypy, eslint, tsc, pytest, vitest) are installed on the host.

**Rationale:**
- Eliminates "works on my machine" environment drift across the team
- New team members only need Docker to start developing
- Clean host — no global Python/Node version conflicts
- Consistent tool versions pinned in Dockerfiles

**Implications:**
- Local dev workflow: `docker compose up`, then `docker compose exec backend ruff check .` / `docker compose exec frontend npm run lint`
- Pre-commit hooks: run via `docker compose exec` (or skipped locally; CI remains the enforcement gate)
- IDE: developers can use VS Code Remote-Containers or attach to running containers for IntelliSense
- Adding a new tool: update the Dockerfile, never install locally
- If a local install is truly needed: ask the team first

**Alternatives considered:**
- Local venv + node_modules — rejected: environment drift, setup complexity, version conflicts across OSes
- VS Code Dev Containers — possible future enhancement, but adds complexity for a course project

### D11: Source code mounted as volumes in dev containers

**Decision:** In docker-compose, mount the host source directories into the containers so code changes on the host are reflected immediately without rebuilding images.

**Rationale:**
- Enables live reloading (uvicorn --reload, Vite HMR)
- Developers edit files in their IDE on the host, container sees changes instantly
- No rebuild on every code change — fast iteration
- Makes the Docker-only workflow (D10) practical

**Implications:**
- docker-compose.yml services include:
  - `./backend:/app` — backend source
  - `./frontend:/app` — frontend source
- Backend runs uvicorn with `--reload` flag
- Frontend runs Vite dev server with HMR (built-in)
- PostgreSQL uses a named volume for data persistence (not a bind mount)
- CI is unaffected — it builds images directly without relying on volume mounts
- `node_modules` and Python packages stay inside the container (anonymous volumes prevent host mounts from overwriting installed dependencies)

**Alternatives considered:**
- Rebuild image on every change — rejected: slow, frustrating
- Copy code into image (no mount) — rejected: no live reload, requires rebuild for every change

### D12: Incremental implementation via separate PRs

**Decision:** The bootstrap is implemented as a sequence of small PRs, each demonstrating the workflow in action. No single massive code dump.

**Rationale:**
- Each PR is small and reviewable
- The bootstrap demonstrates the workflow it sets up (eats its own dog food)
- Branch protection and conventions are enforced incrementally, not bypassed
- Easier to identify and fix issues early

**Implementation order:**
1. Repo scaffold (git init, remote, README, .gitignore)
2. Minimal backend (health endpoint + tooling)
3. Minimal frontend (hello component + tooling)
4. Docker Compose (orchestration + volumes)
5. CI pipeline (GitHub Actions)
6. Deploy pipeline (GitHub Pages)
7. Branch protection + conventions

**Alternatives considered:**
- Single massive PR — rejected: defeats code review, can't enforce branch protection meaningfully
- Feature-complete bootstrap — rejected: scope creep, delays workflow validation

## Risks / Trade-offs

- [GitHub Pages deployment requires repository to be public or GitHub Pro] → Resolved: repo is public.
- [Pre-commit hooks can be bypassed] → Acceptable risk for a course project; CI is the real gate.
- [docker-compose version differences across developer machines] → Mitigation: pin docker-compose version in documentation, use Docker Desktop or Docker Engine consistently.
- [Branch protection "up to date" requirement can cause merge conflicts] → Mitigation: rebase frequently, keep PRs small and short-lived.
- [No backend deployment means no live API for frontend to consume] → Acceptable for bootstrap scope; frontend can be developed with mock data or against local backend.
- [Minimal code may not exercise all CI paths] → Acceptable: the goal is workflow validation, not coverage. Real features will exercise more paths.
