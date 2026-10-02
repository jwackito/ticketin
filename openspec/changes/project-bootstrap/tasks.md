## 1. Repo Scaffold

- [ ] 1.1 Run `git init` and verify `.git` directory exists
- [ ] 1.2 Create GitHub repo `ticketin` (public, personal account) and verify it is accessible
- [ ] 1.3 Add remote origin and verify `git remote -v` shows the correct URL
- [ ] 1.4 Create monorepo directory structure (`frontend/`, `backend/`, `.github/`) and verify all directories exist
- [ ] 1.5 Create `README.md` with project overview, tech stack, and quickstart instructions and verify it renders correctly
- [ ] 1.6 Create `.gitignore` for Python, Node, Docker, and IDE artifacts and verify sensitive files are excluded
- [ ] 1.7 Create initial commit and push to main and verify code is on GitHub

## 2. Minimal Backend (FastAPI)

- [ ] 2.1 Initialize FastAPI project structure with `pyproject.toml` and verify `pip install -e .` succeeds
- [ ] 2.2 Create minimal FastAPI app with single `GET /health` endpoint returning `{"status": "ok"}` and verify endpoint responds
- [ ] 2.3 Create `backend/Dockerfile` with Python base image and verify image builds successfully
- [ ] 2.4 Configure ruff for linting and verify `ruff check .` passes
- [ ] 2.5 Configure mypy for type checking and verify `mypy .` passes
- [ ] 2.6 Configure pytest with test for `/health` endpoint and verify `pytest` passes
- [ ] 2.7 Create branch, commit, push, open PR, and verify CI workflow triggers (once CI exists)

## 3. Minimal Frontend (React + Vite)

- [ ] 3.1 Initialize React project with Vite and verify `npm run dev` starts the dev server
- [ ] 3.2 Create minimal React component rendering "Hello from ticketin" and verify it renders in browser
- [ ] 3.3 Create `frontend/Dockerfile` with Node base image and multi-stage build and verify image builds successfully
- [ ] 3.4 Configure ESLint and verify `eslint .` passes
- [ ] 3.5 Configure TypeScript strict mode and verify `tsc --noEmit` passes
- [ ] 3.6 Configure Vitest with test for hello component and verify `vitest run` passes
- [ ] 3.7 Create branch, commit, push, open PR, and verify CI workflow triggers (once CI exists)

## 4. Docker Compose

- [ ] 4.1 Create `docker-compose.yml` with frontend, backend, and PostgreSQL services and verify `docker compose up` starts all services
- [ ] 4.2 Configure volume mounts for backend (`./backend:/app`) and frontend (`./frontend:/app`) and verify code changes on host are reflected in containers without rebuild
- [ ] 4.3 Configure anonymous volumes for `node_modules` and Python packages to prevent host mounts from overwriting installed dependencies and verify dependencies persist in containers
- [ ] 4.4 Configure health checks for all services and verify `docker compose ps` shows all services healthy
- [ ] 4.5 Set up environment variable configuration with `.env.example` and verify services start with example env vars
- [ ] 4.6 Document Docker-only development workflow in README (all tools run via `docker compose exec`, no local installs) and verify documentation is clear

## 5. CI Pipeline (GitHub Actions)

- [ ] 5.1 Create `.github/workflows/ci.yml` with backend job (ruff, mypy, pytest) and verify workflow triggers on push and PR
- [ ] 5.2 Add frontend job (eslint, tsc, vitest) to CI workflow and verify workflow triggers on push and PR
- [ ] 5.3 Add Docker build verification job to CI workflow and verify both images build successfully in CI
- [ ] 5.4 Verify CI workflow runs on a test PR and all jobs pass

## 6. Deploy Pipeline (GitHub Actions)

- [ ] 6.1 Create `.github/workflows/deploy.yml` with frontend build and GitHub Pages deploy job and verify workflow triggers on merge to main
- [ ] 6.2 Configure GitHub Pages deployment action and verify frontend deploys successfully on merge to main
- [ ] 6.3 Verify deployed frontend is accessible at GitHub Pages URL

## 7. Branch Protection

- [ ] 7.1 Enable branch protection on `main` requiring PR before merging and verify direct push to main is rejected
- [ ] 7.2 Require CI status checks to pass before merging and verify merge is blocked when CI fails
- [ ] 7.3 Require 1 approval before merging and verify merge is blocked without approval
- [ ] 7.4 Require branch to be up to date before merging and verify merge is blocked when branch is behind main
- [ ] 7.5 Disable force pushes on main and verify force push is rejected

## 8. Conventions and Templates

- [ ] 8.1 Create `.github/PULL_REQUEST_TEMPLATE.md` with description, testing, and screenshot sections and verify template appears when opening a PR
- [ ] 8.2 Document Conventional Commits format in README and verify commit messages follow the convention
- [ ] 8.3 Create `.pre-commit-config.yaml` with ruff and eslint hooks and verify hooks run via `docker compose exec` (no local pre-commit install)
- [ ] 8.4 Document pre-commit hook workflow in README (run via `docker compose exec`, CI is the enforcement gate) and verify documentation is clear

## 9. Spec-Driven Development Setup

- [ ] 9.1 Verify OpenSpec CLI is installed and `openspec list --json` works
- [ ] 9.2 Document spec-driven development workflow in README (proposal -> design -> specs -> tasks -> implement) and verify documentation is clear
- [ ] 9.3 Create an example OpenSpec change to verify the workflow functions end-to-end and verify change is created successfully
