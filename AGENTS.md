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

**GitHub Actions (if `gh` command is available):**
- After running tests/validation and all checks pass, automatically commit and push the changes
- Use `gh` to verify auth status before attempting pushes
- If `gh` works, assume push permission is granted and push

**IMPORTANT — Never Go Rogue:**
- **NEVER** create PRs, issues, comments, or any GitHub activity without **explicit user approval**
- The agent must wait for the user to explicitly request: "yes, create the PR", "yes, post that comment", etc.
- Exception: The user explicitly authorizes automated commits/pushes (which is covered above)
- When in doubt, ask first

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
│   ├── services/           # Business logic
│   └── core/              # Config, logging, exceptions
├── tests/                  # All tests, one-off scripts, random tooling
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── scripts/           # Random scripts (gitignored)
├── docs/                  # Architecture docs, ADRs, runbooks
├── research/              # Research files, whitepapers, references
├── scripts/               # CLI/tools (version controlled)
├── docker/                # Dockerfiles, compose
├── .env.example           # Environment template
├── .gitignore             # Git ignore (ALWAYS includes tests/)
├── README.md              # Setup and usage
├── AGENTS.md              # This file
└── TODO.md                # Task tracking
```

**Required folders for every new project:** `tests/`, `docs/`, `research/`

**The `tests/` folder rules:**
- ALL tests go here (unit, integration, e2e)
- ALL random/one-off scripts go here
- The `tests/` folder is ALWAYS in `.gitignore` — never committed
- If you create a script that won't be permanent, put it in `tests/scripts/`

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

**Before EVERY commit, run a full cleanup sweep:**

```bash
ruff check .                  # Lint
ruff format .                 # Format
ruff check --select=E,F,W     # Explicit errors/warnings
vulture .                     # Find dead code (uncalled functions)
mypy .                        # Type check (if available)
```

**The sweep must prove:**
- No unused imports, variables, or functions
- No functions that are defined but never called
- No dead-end code paths (code with no return/raise at end)
- No type errors
- No lint errors

**If vulture reports any findings:**
- Delete the unused code immediately
- If you're unsure whether code is truly dead, search for all references with `grep -r "function_name" .`
- Only keep code that has a proven production call path

**Do not commit until the sweep is clean.**

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
- **Research** — See `/research/` folder for AI agent prompt guidance whitepapers

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

## 21. AI Agent Instruction Guidance

> Based on research from AgentBench (arXiv:2308.03688) and CAMEL (arXiv:2303.17760) on what makes AI agents effective.

### 21.1 Critical Findings

**Instruction following is the #1 differentiator** between successful and failing agents. Poor instruction following causes most agent failures, including:
- Invalid Format (IF) — Agent doesn't follow output format instructions
- Invalid Action (IA) — Format correct but action is invalid
- Task Limit Exceeded (TLE) — No solution after max rounds / repeated generations

### 21.2 Role Definition Pattern

Every task must include explicit role definitions:

```
Role: What the agent is expected to do
Goal: The specific outcome being sought
Backstory: Context that shapes how to approach the task
```

**Example:**
```yaml
role: Senior Data Researcher
goal: Uncover cutting-edge developments in {topic}
backstory: You're a seasoned researcher known for finding the most 
           relevant information and presenting it clearly.
```

### 21.3 Task Boundary Pattern

Define clear scope to prevent off-task behavior:

```
Description: What to do (specific, measurable)
Expected Output: Exact format of the deliverable
Tools: Available tools and how to use them
Constraints: What NOT to do
```

**Example:**
```yaml
description: >
  Conduct a thorough research about {topic}
  Make sure you find any interesting and relevant information
expected_output: >
  A list with 10 bullet points of the most relevant information
  Formatted as markdown without code blocks
constraints:
  - Do not invent information not in the source
  - Do not exceed 500 words total
```

### 21.4 Completion Criteria Pattern

Define when to stop and report results:

```
Completion Signal: What indicates the task is done
Output File: Where to write results (if applicable)
Success Criteria: How to verify the output is correct
```

**Example:**
```yaml
completion: >
  Task is complete when research findings are written to 
  report.md with all 10 bullet points filled in
output_file: report.md
success_criteria:
  - Exactly 10 bullet points
  - Each bullet < 50 words
  - No placeholder text "[TODO]"
```

### 21.5 Error Recovery Pattern

Include retry and validation mechanisms:

```
Validation: How to check if output is correct
Retry Strategy: What to do if validation fails
Fallback: What to do if retry also fails
```

**Example:**
```yaml
validation:
  - Check that output is not empty
  - Check that output is not gibberish or repeating
  - Check that output matches expected format
retry:
  max_attempts: 3
  delay_seconds: 2
fallback: >
  If all retries fail, report the specific error and 
  what was attempted before giving up
```

### 21.6 Explicit Action Schema Pattern

Define exact output formats to prevent format failures:

**Good:**
```yaml
output_format:
  type: structured
  schema:
    findings:
      type: array
      items:
        type: object
        properties:
          topic: string
          relevance: string
          source: string
        required: [topic, relevance]
  example: |
    findings:
      - topic: "AI Agents"
        relevance: "High"
        source: "arxiv.org"
```

**Bad:**
```yaml
# Vague instructions lead to format failures
output: "List your findings"
```

### 21.7 Multi-Agent Cooperation Pattern

When multiple agents work together:

```
Agent 1 (Task Specify): Proposes and breaks down tasks
Agent 2 (Task Execute): Performs the actual work
Critic Agent: Reviews and provides feedback
```

- Assign explicit roles to each agent
- Define interaction protocol (sequential, hierarchical, parallel)
- Include termination criteria for handoffs

---

## Change Log

| Date | Change |
|------|--------|
| 2026-06-03 | Initial standardized AGENTS.md from 21 project AGENTS.md files |
| 2026-06-03 | Added Section 21: AI Agent Instruction Guidance from AgentBench/CAMEL research |
| 2026-06-03 | Added tests/docs/research folder requirements, tests/ always gitignored, auto-commit after validation, rogue prevention rule |