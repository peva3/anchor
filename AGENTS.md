# AGENTS.md — Standardized Project Guide

> Universal guidance for AI agents working on any project. Adapt sections to fit project scope.

---

## 1. Core Principles

- **No dead code.** Every function must be called by a production path. Remove unused imports, variables, and definitions immediately.
- **No stubs.** Every function, module, component, and endpoint must have a real implementation.
- **No silent failures.** Wrapped exception handlers (`except Exception: pass`) must have a comment explaining why the failure is non-critical. Log before swallowing.
- **Test-first.** Every module should have corresponding tests. Tests must pass before moving on.
- **Proven integration.** After building any component, verify it works end-to-end. Do not mark a task complete without verification.
- **Cross-service contract tests.** When building features spanning multiple services, write integration tests that exercise the actual HTTP contracts between them.
- **Trace every function call.** Before marking a module complete, verify every public function is called by a production path.

---

## 2. Commit Protocol

**After completing and verifying any task:**
1. `git add <changed files>`
2. `git commit -m "Descriptive commit message"` — describe WHAT changed and WHY
3. `git push origin <branch>`

**Author identity (already configured globally):**
- Username: `peva3`
- Email: `user@example.com`

**Message format conventions:**
- Prefix with scope when applicable: `api: add rate limiting`, `frontend: fix timeline scroll bug`
- For TODO completions: `Sprint N: <description>`
- Include size delta for binary builds: `autoexec.bin +12KB`

---

## 3. Shell Execution Rules

**CRITICAL:** A plugin automatically prepends `snip` to all shell commands. `snip` requires a real executable, so it will fail if applied to shell built-ins (`cd`, `export`, `source`).

**Correct format (Subshell):**
```bash
bash -c 'cd /path/to/directory && your_command --flags'
bash -c 'export VAR=value && your_command'
```

**Incorrect format (Will fail):**
```bash
cd /path/to/directory && your_command --flags
export VAR=value && your_command
```

---

## 4. Code Style

### Python
- **Formatting:** PEP 8, 4-space indentation, 100 char line limit
- **Naming:** `snake_case` (variables/functions), `PascalCase` (classes), `SCREAMING_SNAKE` (constants)
- **Imports:** Grouped stdlib → third-party → local; alphabetical within groups
- **Types:** Use type hints for all function signatures
- **Docstrings:** Google style for modules, classes, and public functions
- **Error Handling:** Specific exceptions, never bare `except:`
- **Async:** Use `async/await` for I/O-bound operations

### TypeScript / JavaScript
- **Formatting:** 2-space indentation, semicolons optional but consistent
- **Naming:** `camelCase` (variables/functions), `PascalCase` (components/types)
- **Types:** Strict mode enabled, explicit return types on exported functions
- **Components:** Functional components with hooks, no class components

### General
- No emojis in code or commit messages
- No `print` statements — use `logging`
- Keep functions under 50 lines; extract sub-functions for complex logic
- Add tests for all new functionality

---

## 5. Project Structure Conventions

```
project/
├── src/                    # Source code
│   ├── api/               # API routes/endpoints
│   ├── models/            # Data models/schemas
│   ├── services/          # Business logic
│   ├── core/              # Config, logging, exceptions
│   └── tests/             # Tests (mirror source structure)
├── docs/                  # Architecture docs, ADRs
├── scripts/               # CLI/tools
├── docker/                # Dockerfiles, compose
├── .env.example           # Environment template
├── README.md              # Setup and usage
├── AGENTS.md              # This file
└── TODO.md                # Task tracking
```

---

## 6. TODO.md — Task Tracking Standard

Use this structure for tracking project tasks:

```markdown
# TODO.md — Project Name

## Legend
- ✅ Complete
- 🔄 In Progress
- ⬜ Not Started

## Current Sprint / Phase

| # | Status | Description |
|---|--------|-------------|
| 1 | ✅ | Completed task |
| 2 | 🔄 | Active task |
| 3 | ⬜ | Upcoming task |

## Completed Sprints

| Sprint | Status | Deliverable |
|--------|--------|-------------|
| 1   | ✅ | Feature A |
| 2   | ✅ | Feature B |

## Notes
- Document architectural decisions made during task completion
- Record any deviations from original plan and why
- Track build size delta for firmware/binary projects
```

**For multi-phase projects**, also track sub-tasks:
```
| 5a | ✅ | Sub-task A |
| 5b | ✅ | Sub-task B |
```

---

## 7. Docker / Deployment

- **Rebuild after code changes.** Containers use built images, not source files. After modifying code:
  ```bash
  docker compose build <service> && docker compose up -d <service>
  # or for all services:
  docker compose up -d --build
  ```

- **Container health checks.** All services should have healthcheck configured.

- **Ports.** Document all exposed ports and what runs on each:
  ```
  | Service | Port | Host Access | Role |
  |---------|------|-------------|------|
  | api     | 8000 | :8000       | REST API |
  | frontend| 3000 | :3090       | Web UI   |
  ```

- **Environment variables.** Use `.env.example` with documented defaults. All config via env vars, not code changes.

---

## 8. Testing Requirements

- **Unit tests** for all new functions
- **Integration tests** for workflows spanning multiple components
- **Cross-service contract tests** for HTTP API interactions
- Mock external APIs (not live calls in CI)
- Use fixtures in `conftest.py` for shared setup

### Test Commands
```bash
pytest                           # All tests
pytest tests/test_specific.py    # Single file
pytest -k "pattern"              # Matching tests
pytest --cov=. --cov-report=term-missing  # With coverage
```

---

## 9. Linting & Type Checking

Run before every commit:
```bash
ruff check . && ruff format .    # Python
mypy .                           # Python type check (if available)
npm run lint                     # JavaScript/TypeScript
```

Fix all findings before committing. Do not disable rules without good reason and a comment.

---

## 10. Error Handling Patterns

```python
# Good: specific exception with context
try:
    result = await client.post(url, json=data)
    result.raise_for_status()
except httpx.TimeoutException:
    logger.warning(f"Timeout calling {model}, retrying")
    raise RetryableError(f"Timeout for {url}") from None
except httpx.HTTPStatusError as e:
    logger.error(f"HTTP {e.response.status_code} from {url}")
    raise ApiError(f"Failed to call {url}") from e

# Bad: silent swallow
except Exception:
    pass
```

- Always include context in exceptions (use `from None` to suppress chain)
- Log at appropriate level: DEBUG for retryable, WARNING for degraded, ERROR for fatal
- Use `None` return with type annotation, not tuple

---

## 11. Configuration Management

- **Environment variables** for all configurable values
- **`.env.example`** as a template with all variables documented
- **Prefix convention** for namespacing (e.g., `APP_`, `SERVICE_`, `DB_`)
- **No config files in code** — everything via env vars or `.env`

---

## 12. API Design

- **REST conventions:** `GET` (read), `POST` (create), `PATCH` (update), `DELETE` (remove)
- **Prefix:** All API endpoints use `/api/...` (no `/v1/`)
- **Response format:** Consistent wrapper `{ "data": ..., "error": null }` or `{ "items": [...], "count": N }`
- **Pagination:** Cursor-based for large datasets
- **Error responses:** `{ "error": "message", "code": "ERROR_CODE" }` with appropriate HTTP status

---

## 13. Security Best Practices

- **Input validation.** Use Pydantic models or equivalent for all API inputs
- **Parameterized queries.** Never use string interpolation for SQL
- **Sanitize for logging.** Use `sanitize_for_logging()` before logging user input
- **Redact secrets.** API keys masked in logs automatically
- **Rate limiting.** Implement on public endpoints
- **No secrets in code.** All secrets via env vars or mounted secrets

---

## 14. Logging Standards

```python
import logging
logger = logging.getLogger(__name__)

# Use lazy %s formatting (not f-strings) for performance
logger.debug("Processing item %s", item_id)
logger.info("Fetched %d items from %s", count, source)
logger.warning("Retrying after %ds", delay)
logger.error("Failed to process %s: %s", item_id, str(e))
```

- Use appropriate log levels: DEBUG (per-request details), INFO (operations), WARNING (recoverable issues), ERROR (failures)
- No `print` statements — use `logging`
- Include relevant context (IDs, counts, durations) in log messages

---

## 15. Git Workflow

- **Small, focused commits.** One logical change per commit.
- **Descriptive messages.** First line <72 chars, optional body for detail.
  ```
  api: add rate limiting middleware
  
  - Added Redis-backed rate limiter
  - Configurable per-IP limits
  - Returns 429 when exceeded
  ```
- **Never force push** to shared branches
- **Branch naming:** `feature/name`, `fix/name`, `sprint-n`

---

## 16. Documentation Requirements

- **README.md** — Setup, quick start, architecture overview
- **API docs** — OpenAPI/Swagger at `/docs` for APIs
- **Architecture docs** — `docs/architecture.md`, ADRs in `docs/adr/`
- **Code comments** — Every non-trivial function needs a docstring explaining WHAT, HOW, WHY
- **AGENTS.md** — This file, updated when project conventions change

---

## 17. Dependency Management

- Pin exact versions in `requirements.txt` or `pyproject.toml`
- Run `pip-audit` or `safety` periodically to check for vulnerabilities
- Keep dependencies minimal — avoid adding libraries for simple tasks
- Document why each major dependency exists

---

## 18. Performance Considerations

- **Async for I/O.** Use `asyncio` and `httpx.AsyncClient` for concurrent HTTP calls
- **Connection pooling.** Reuse HTTP clients and database connections
- **Caching.** Cache expensive operations with appropriate TTLs
- **Batching.** Batch API calls and DB writes where possible
- **Profile before optimizing.** Use profiling tools to identify bottlenecks, don't guess

---

## 19. Build & Deployment

For compiled/firmware projects:
- **Track build size.** Log autoexec.bin / binary size in commits.
- **Verify after changes.** Build must succeed and size must be within limits.
- **Deploy location.** Note the verified deployment path.

---

## 20. External Integrations

For each external API/service integrated:
- **Rate limits.** Document limits and how you handle them.
- **Auth method.** Document authentication mechanism.
- **Error handling.** Document error codes and retry strategy.
- **Health checks.** How to verify the integration is working.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-06-03 | Initial standardized AGENTS.md from 21 project AGENTS.md files |