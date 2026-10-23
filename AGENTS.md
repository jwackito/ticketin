# AGENTS.md

Instructions for coding agents working in this repository.

## Workflow (non-negotiable)

- **Never commit or push directly to `main`.**
- Always: create a branch, commit, push the branch, open a pull request, wait for CI, merge.
- Before any `git commit` or `git push`, confirm the current branch is not `main`.
- Branch naming: `<type>/<short-slug>` (for example `feat/event-catalog-api`, `chore/workflow-guardrails`).
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/).

`main` is protected on the server: direct pushes and force pushes are rejected, and pull
requests must pass the `backend`, `frontend`, and `docker` status checks before merging.
No approval is required, so the maintainer can merge their own pull request once CI is green.

## Repository facts

- Public repository on a personal account; currently a solo maintainer.
- Backend: FastAPI + SQLAlchemy + PostgreSQL, in `backend/`.
- Frontend: React + Vite + TypeScript, in `frontend/`.
- Docker-only development: run all tools with `docker compose exec` (see `README.md`).
- Spec-driven development with OpenSpec in `openspec/`.

## Local pre-push hook (recommended)

Enable the guard that blocks accidental direct pushes to `main`:

```bash
git config core.hooksPath .githooks
```

This is a local convenience and can be skipped with `--no-verify`; the server-side branch
protection is the real gate. The hook only runs on an executable filesystem — on a `noexec`
mount git skips it, leaving server-side protection as the only guard.
