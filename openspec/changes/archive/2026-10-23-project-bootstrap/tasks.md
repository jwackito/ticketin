## 1. Repo Scaffold

- [x] 1.1 Run `git init` and verify `.git` directory exists
- [x] 1.2 Create GitHub repo `ticketin` (public, personal account) and verify it is accessible
- [x] 1.3 Add remote origin and verify `git remote -v` shows the correct URL
- [x] 1.4 Create monorepo directory structure (`frontend/`, `backend/`, `.github/`) and verify all directories exist
- [x] 1.5 Create `README.md` with project overview, tech stack, and quickstart instructions and verify it renders correctly
- [x] 1.6 Create `.gitignore` for Python, Node, Docker, and IDE artifacts and verify sensitive files are excluded
- [x] 1.7 Create initial commit and push to main and verify code is on GitHub

## 2. Minimal Backend (FastAPI)

- [x] 2.1 Initialize FastAPI project structure with `pyproject.toml` and verify `pip install -e .` succeeds
- [x] 2.2 Create minimal FastAPI app with single `GET /health` endpoint returning `{"status": "ok"}` and verify endpoint responds
- [x] 2.3 Create `backend/Dockerfile` with Python base image and verify image builds successfully
- [x] 2.4 Configure ruff for linting and verify `ruff check .` passes
- [x] 2.5 Configure mypy for type checking and verify `mypy .` passes
- [x] 2.6 Configure pytest with test for `/health` endpoint and verify `pytest` passes
- [x] 2.7 Create branch, commit, push, open PR, and verify CI workflow triggers (once CI exists)

## 3. Minimal Frontend (React + Vite)

- [x] 3.1 Initialize React project with Vite and verify `npm run dev` starts the dev server
- [x] 3.2 Create minimal React component rendering "Hello from ticketin" and verify it renders in browser
- [x] 3.3 Create `frontend/Dockerfile` with Node base image and multi-stage build and verify image builds successfully
- [x] 3.4 Configure ESLint and verify `eslint .` passes
- [x] 3.5 Configure TypeScript strict mode and verify `tsc --noEmit` passes
- [x] 3.6 Configure Vitest with test for hello component and verify `vitest run` passes
- [x] 3.7 Create branch, commit, push, open PR, and verify CI workflow triggers (once CI exists)

## 4. Docker Compose

- [x] 4.1 Create `docker-compose.yml` with frontend, backend, and PostgreSQL services and verify `docker compose up` starts all services
- [x] 4.2 Configure volume mounts for backend (`./backend:/app`) and frontend (`./frontend:/app`) and verify code changes on host are reflected in containers without rebuild
- [x] 4.3 Configure anonymous volumes for `node_modules` and Python packages to prevent host mounts from overwriting installed dependencies and verify dependencies persist in containers
- [x] 4.4 Configure health checks for all services and verify `docker compose ps` shows all services healthy
- [x] 4.5 Set up environment variable configuration with `.env.example` and verify services start with example env vars
- [x] 4.6 Document Docker-only development workflow in README (all tools run via `docker compose exec`, no local installs) and verify documentation is clear

## 5. CI Pipeline (GitHub Actions)

- [x] 5.1 Create `.github/workflows/ci.yml` with backend job (ruff, mypy, pytest) and verify workflow triggers on push and PR
- [x] 5.2 Add frontend job (eslint, tsc, vitest) to CI workflow and verify workflow triggers on push and PR
- [x] 5.3 Add Docker build verification job to CI workflow and verify both images build successfully in CI
- [x] 5.4 Verify CI workflow runs on a test PR and all jobs pass

## 6. Deploy Pipeline (GitHub Actions)

- [x] 6.1 Create `.github/workflows/deploy.yml` with frontend build and GitHub Pages deploy job and verify workflow triggers on merge to main
- [x] 6.2 Configure GitHub Pages deployment action and verify frontend deploys successfully on merge to main
- [x] 6.3 Verify deployed frontend is accessible at GitHub Pages URL

## 7. Branch Protection

- [x] 7.1 Enable branch protection on `main` requiring a PR before merging with `enforce_admins` enabled, and verify a direct push to `main` is rejected (see D13)
- [x] 7.2 Require the `backend`, `frontend`, and `docker` status checks before merging and verify the protection config lists all three
- [x] 7.3 Set required approvals to 0 (solo maintainer) so the author can self-merge a green PR, and verify `required_approving_review_count` is 0 in the protection config
- [x] 7.4 Require the branch to be up to date before merging and verify `strict` is enabled in the protection config
- [x] 7.5 Disable force pushes on `main` and verify a force push is rejected
- [x] 7.6 Create `AGENTS.md` with the never-push-to-`main` rule and verify the file exists with that directive
- [x] 7.7 Add `.githooks/pre-push` rejecting pushes to `main`, document `git config core.hooksPath .githooks` in the README, and verify the hook logic rejects a push to `main` (invoked with `sh`; the workspace `noexec` mount prevents git from executing it, so server-side protection is the operative guard)
- [x] 7.8 Verify the pre-enforcement direct commits (`d03adc8`, `1126960`) are recorded as a documented exception in design D13 and that history is not rewritten

## 8. Conventions and Templates

- [x] 8.1 Create `.github/PULL_REQUEST_TEMPLATE.md` with description, testing, and screenshot sections and verify template appears when opening a PR
- [x] 8.2 Document Conventional Commits format in README and verify commit messages follow the convention
- [x] 8.3 Define pre-commit lint checks as `docker compose exec backend ruff check .` and `docker compose exec frontend npm run lint` and verify both run in the containers (no local install)
- [x] 8.4 Document pre-commit hook workflow in README (run via `docker compose exec`, CI is the enforcement gate) and verify documentation is clear

## 9. Spec-Driven Development Setup

- [x] 9.1 Verify OpenSpec CLI is installed and `openspec list --json` works
- [x] 9.2 Document spec-driven development workflow in README (proposal -> design -> specs -> tasks -> implement) and verify documentation is clear
- [x] 9.3 Create the `project-bootstrap` OpenSpec change to verify the workflow functions end-to-end (specs skipped — no spec-level behavior) and verify the change is created successfully
