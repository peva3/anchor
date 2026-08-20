# Skill 25: Common Gotchas

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 25. Common Gotchas

Lessons learned from multiple projects — things that regularly bite developers.

### 25.1 Python Version Mismatches
- Ensure Python 3.13+ for modern projects; know what features your floor version allows
- Use `python3 -m venv` to specify version explicitly
- Check with `python --version` before installing packages
- If the repo uses **uv**, use `uv sync` / `uv run` instead of ad-hoc pip installs — it reads `uv.lock`

### 25.2 Shell Command Failures
- Remember `snip` prepends to all commands automatically
- Use `bash -c '...'` format for built-ins (`cd`, `export`, `source`)
- Direct `cd` commands will fail
- Quote variable expansions and paths with spaces; prefer `set -euo pipefail` in scripts

### 25.3 Environment Variables
- Always create `.env` from `.env.example`
- Never commit `.env` (it's in `.gitignore`)
- Missing env vars cause silent failures — check logs
- Validate config at startup (fail fast) rather than crashing mid-request

### 25.4 Package Conflicts
- Use fresh virtual environments
- Install from lockfiles, not individual packages
- Run `pip freeze` to see exact versions installed

### 25.5 Type Errors
- Run `mypy` (or pyright/basedpyright) before committing
- In Python, "truly unknown" is `object` (safe, must be narrowed) or `Any` (escape hatch — avoid). `unknown` is the TypeScript equivalent; don't carry that keyword into Python
- Generic types need explicit parameters: `list[str]` not `list`

### 25.6 Import Order
- Ruff auto-fixes import order: `ruff check --fix .`
- Stdlib → third-party → local, alphabetical within groups
- Run format check before committing

### 25.7 Race Conditions
- Concurrent operations on shared state need locks
- Test concurrent access explicitly
- Log when acquiring/releasing locks for debugging

### 25.8 Async Gotchas (Python)
- Never call blocking I/O in the event loop — wrap with `asyncio.to_thread`/`run_in_executor` or it stalls every coroutine ([Section 18](skills/18-performance-considerations.md))
- Await your coroutines — an un-awaited coroutine silently never runs (and `asyncio.run()` inside a running loop raises)
- Use `asyncio.TaskGroup`/`except*` for concurrent failures (PEP 654) — `asyncio.gather` raises `ExceptionGroup`
- Prefer `httpx.AsyncClient` over `requests` in async code paths

### 25.9 Testing edge cases
- Test the empty case (empty list, empty string, None)
- Test the overflow case (very large input)
- Test the concurrent case (multiple simultaneous calls)

### 25.10 Git Mistakes
- Never `git add .` — add specific files
- Check `git diff --cached` before committing
- Use `git status` to verify what will be pushed

### 25.11 Docker Debugging
- Use `docker compose logs <service>` to see what's failing
- `docker compose exec <service> bash` to get shell inside
- Restart with `docker compose restart <service>`

---

