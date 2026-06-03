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

### Language — English Only
- **ALL code, comments, documentation, variable names, commit messages, and user-facing text MUST be in English**
- No foreign language in any file, variable name, comment, or documentation
- This ensures all agents and developers across any language background can collaborate effectively
- Exception: Test data with realistic content (names, addresses) may use any language for authenticity

---

## 5. Project Structure Conventions

```
project/
├── src/                    # Source code
│   ├── api/               # API routes/endpoints
│   ├── models/            # Data models/schemas
│   ├── services/          # Business logic
│   └── core/              # Config, logging, exceptions
├── tests/                  # All tests, one-off scripts, random tooling
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── scripts/           # Random scripts (gitignored)
├── docs/                  # Architecture docs, ADRs, runbooks
├── research/              # Research files, whitepapers, references
├── scripts/               # CLI/tools (version controlled)
├── docker/                # Dockerfiles, compose
├── DEEPDIVE.md            # System narrative — detailed explanation
├── .env.example           # Environment template
├── .gitignore             # Git ignore (ALWAYS includes tests/)
├── README.md              # Setup and usage
├── AGENTS.md              # This file
└── TODO.md                # Task tracking
```

**Required folders for every new project:** `tests/`, `docs/`, `research/`

**DEEPDIVE.md — Living System Narrative:**

Every project MUST have a `DEEPDIVE.md` file at the root. This is not documentation — it's a detailed narrative explaining HOW and WHY the system is built the way it is.

**When to update DEEPDIVE.md:**
- After ANY architectural change
- After ANY significant refactor
- When adding new integration patterns
- When removing code (explain WHY it was removed)
- When making decisions that future agents need to understand

**DEEPDIVE.md must cover:**
- **System layout** — Why files are organized this way, why this tech stack
- **Data flow** — How data moves through the system, from ingestion to output
- **Key decisions** — Every non-obvious choice, including alternatives rejected and WHY
- **Gotchas and landmines** — Known failure modes, edge cases that bite
- **Interconnections** — How services/Modules communicate, what depends on what
- **Why things work** — Not just WHAT the code does, but WHY it was designed that way

**DEEPDIVE.md is NOT:**
- A substitute for inline comments
- A restatement of what code does (assume the code is self-documenting)
- Static — it MUST be updated when the system changes

**Example DEEPDIVE.md entry:**
```markdown
## Why the API is Split into public/admin

We split the API into port 8000 (public, read-only+search) and port 8004 
(admin, localhost-only, full CRUD) because:

- The ingestion pipeline needs to write without auth overhead
- Admin operations (scraper config, manual overrides) shouldn't be exposed
- Public users only need search and read operations
- This follows defense-in-depth: even if public API is compromised,
  admin operations remain protected by network isolation

Date: 2026-05-15
Decision: Split API into dual ports (migration 009)
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

**Commit Messages — Sound Human, Not AI:**

Write commits as if explaining to a colleague why this change exists:

```
Good (human-sounding):
"Prevented race condition in token refresh by adding mutex lock around 
auth state mutation. Previously, concurrent requests could cause the 
refresh callback to fire twice, resulting in a 401 loop."

Bad (AI-sounding):
"fix: fixed race condition in auth service"
```

**The WHY matters most:**
- Explain the problem that existed before this change
- Explain what the change does and why it solves the problem
- If there were alternatives considered, note why you picked this one
- Include any context that future developers (or agents) need to understand

**Pattern:**
```
<type>: <what changed>

<problem>: Why this needed fixing
<solution>: What the change does and why
<context>: Any important decisions, trade-offs, or gotchas
```

**Examples:**
```
api: Added JWT refresh endpoint to eliminate 401 loops

The token refresh had a race condition where concurrent requests could
trigger multiple refresh calls. Added mutex lock around auth state.
Ref: https://github.com/org/repo/issues/1234
```

```
frontend: Rewired timeline scrubber to use IntersectionObserver

GSAP physics caused dot highlighting to desync when scrolling fast.
IntersectionObserver 1px center tripwire provides reliable sync without
third-party dependencies. Removed all physics, reduced bundle by 47KB.
```

```
db: Added content_hash unique constraint to prevent duplicate ingestion

Two scrapers could race and insert the same article from different RSS 
feeds. Added unique constraint on content_hash with NULLS NOT DISTINCT.
Migration 010 adds constraint with deduplication pass.
```

**Small commits with big explanations are fine.** A 3-line change can have a 10-line commit message explaining the problem it solves.

---

- **Small, focused commits.** One logical change per commit.
- **Descriptive messages.** First line <72 chars, optional body for detail.
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

## 22. Multi-Agent Cooperation Patterns

Based on CAMEL (arXiv:2303.17760) and MetaGPT (arXiv:2308.00352).

### 22.1 Role Definition Template

Every multi-agent task requires explicit role definitions:

```yaml
role: Senior <Domain> Engineer
goal: <Specific outcome being sought>
backstory: |
  You are a seasoned engineer known for <expertise>.
  You approach problems by <methodology>.
constraints:
  - Do not <forbidden action>
  - Always <required action>
  - Stop when <termination condition>
```

### 22.2 Sequential Handoff Pattern (Assembly Line)

For workflows where agents pass work sequentially (MetaGPT-style):

```
Product Manager → Architect → Engineer → QA → Deploy
```

**Rules:**
1. Each agent has explicit input/output contracts
2. Verification gate at each handoff before proceeding
3. Document any deviations at handoff boundaries
4. Supervisor agent tracks overall progress

**Example:**
```
Agent 1 (PM): Defines requirements → outputs SPEC.md
Agent 2 (Architect): Reviews SPEC → outputs architecture.md
Agent 3 (Engineer): Implements → outputs code + tests
Agent 4 (QA): Verifies → outputs test report
```

### 22.3 Hierarchical Pattern

For supervisor/worker architectures:

```
Supervisor Agent
├── Worker 1 (specific subtask)
├── Worker 2 (specific subtask)
└── Worker 3 (specific subtask)
```

**Rules:**
1. Supervisor assigns clear sub-tasks with boundaries
2. Workers report results to supervisor
3. Supervisor aggregates and decides next steps
4. Timeout on workers — if exceeded, supervisor escalates

### 22.4 Collaborative Pattern

For peer-to-peer agent cooperation:

```
Agent A ←→ Shared Context ←→ Agent B
              ↓
          Critic Agent
```

**Rules:**
1. Agents share a common context (document, state, memory)
2. Critic agent reviews and provides feedback
3. Agents iterate based on critique
4. Termination when consensus reached or max iterations hit

### 22.5 Multi-Agent Termination Criteria

For all patterns, define:
- **Max iterations** — Stop after N cycles even if not complete
- **Consensus threshold** — When to stop (e.g., 2 of 3 agents agree)
- **Escalation path** — What to do when termination reached without success
- **Context snapshot** — Save state before termination for resume

---

## 23. Verification Gates

Before proceeding to the next step, verify explicitly.

### 23.1 Format Validation

Output must match expected schema:

```python
# Validate structured output
import jsonschema
jsonschema.validate(instance=output, schema=expected_format)
```

### 23.2 Action Validation

Action must be valid for current state:

```python
# Check state before acting
if not is_valid_action(current_state, proposed_action):
    raise InvalidActionError(f"Cannot {action} in state {current_state}")
```

### 23.3 Context Validation

No context limit exceeded:

```
Before each major step:
- Estimate tokens needed for remaining work
- If remaining context < 20%, summarize/snapshot current state
- If context limit would be exceeded, flush and resume fresh
```

### 23.4 Termination Validation

Completion criteria must be met:

```
completion_checklist:
  - [ ] Output matches expected format
  - [ ] All functions have production call paths
  - [ ] No unused imports/variables (vulture clean)
  - [ ] Tests pass
  - [ ] Lint clean
  - [ ] Type check clean
  - [ ] Documentation updated (DEEPDIVE.md if needed)
```

### 23.5 Error Recovery Hierarchy

When validation fails:

1. **Retry** (max 3 attempts, exponential backoff: 1s, 2s, 4s)
2. **Alternative approach** — Try different method to achieve same goal
3. **Fallback** — Degrade gracefully (skip non-critical, continue core)
4. **Escalate** — Report detailed error with what was attempted, let user decide

---

## 24. Common Failure Modes

Based on AgentBench (arXiv:2308.03688) findings on LLM agent failures.

### 24.1 Invalid Format (IF)

**Cause:** Agent doesn't follow output format instructions.

**Prevention:**
- Provide explicit schema with examples
- Use JSON schema validation
- Give exactly one valid output format

**Recovery:**
- Show example of correct format
- Retry with stricter constraints

### 24.2 Invalid Action (IA)

**Cause:** Format correct but action is invalid for current state.

**Prevention:**
- Validate state before suggesting actions
- Provide explicit list of valid actions
- Include state machine documentation

**Recovery:**
- Report current state and valid actions
- Suggest valid alternative

### 24.3 Task Limit Exceeded (TLE)

**Cause:** No solution found after maximum iterations/rounds.

**Prevention:**
- Define clear completion criteria upfront
- Set maximum iteration count
- Implement early termination when progress stalls

**Recovery:**
- Save current state for manual review
- Report what was tried and why it failed
- Ask user for guidance on alternative approach

### 24.4 Context Limit Exceeded (CLE)

**Cause:** Interaction history exceeds max context.

**Prevention:**
- Summarize context periodically (every ~50% of context)
- Snapshot key decisions to external storage
- Start fresh session with summary if needed

**Recovery:**
- Save all context to file
- Start new session with summarized state
- Resume from checkpoint

### 24.5 Hallucination Failures

**Cause:** Agent generates plausible but incorrect information.

**Prevention:**
- Require source citations in research tasks
- Validate against known facts before accepting
- Use tool outputs as ground truth, not agent memory

**Recovery:**
- Cross-check with authoritative source
- Flag as uncertain if cannot verify

---

## 25. Common Gotchas

Lessons learned from multiple projects — things that regularly bite developers.

### 25.1 Python Version Mismatches
- Ensure Python 3.12+ for modern projects
- Use `python3 -m venv` to specify version explicitly
- Check with `python --version` before installing packages

### 25.2 Shell Command Failures
- Remember `snip` prepends to all commands automatically
- Use `bash -c '...'` format for built-ins (`cd`, `export`, `source`)
- Direct `cd` commands will fail

### 25.3 Environment Variables
- Always create `.env` from `.env.example`
- Never commit `.env` (it's in `.gitignore`)
- Missing env vars cause silent failures — check logs

### 25.4 Package Conflicts
- Use fresh virtual environments
- Install from lockfiles, not individual packages
- Run `pip freeze` to see exact versions installed

### 25.5 Type Errors
- Run `mypy` before committing
- Don't use `Any` — use `unknown` if type is truly unknown
- Generic types need explicit parameters: `list[str]` not `list`

### 25.6 Import Order
- Ruff auto-fixes import order: `ruff check --fix .`
- Stdlib → third-party → local, alphabetical within groups
- Run format check before committing

### 25.7 Race Conditions
- Concurrent operations on shared state need locks
- Test concurrent access explicitly
- Log when acquiring/releasing locks for debugging

### 25.8 Testing edge cases
- Test the empty case (empty list, empty string, None)
- Test the overflow case (very large input)
- Test the concurrent case (multiple simultaneous calls)

### 25.9 Git Mistakes
- Never `git add .` — add specific files
- Check `git diff --cached` before committing
- Use `git status` to verify what will be pushed

### 25.10 Docker Debugging
- Use `docker compose logs <service>` to see what's failing
- `docker compose exec <service> bash` to get shell inside
- Restart with `docker compose restart <service>`

---

## 26. Getting Help

When stuck on a problem.

### 26.1 Self-Service First

1. Check project documentation in `/docs/`
2. Search `/research/` for similar patterns or whitepapers
3. Review past commits for similar fixes: `git log --grep="keyword"`
4. Run linting/smoke tests — actual errors often reveal the issue
5. Search codebase with `grep -r "pattern" .` for similar implementations

### 26.2 Framework-Specific Resources

```
LangChain:    https://docs.langchain.com/
AutoGPT:      https://docs.agpt.co/
CAMEL:        https://docs.camel-ai.org/
MetaGPT:      https://deepwisdom.com/
Anthropic:   https://docs.anthropic.com/
OpenAI:      https://platform.openai.com/docs/
```

### 26.3 When to Escalate

Ask the user when:
- Problem requires making decisions with trade-offs (not clear cut)
- Fix requires changing architecture rather than code
- Issue is not in code but in requirements/expectations
- You've been stuck for more than 15 minutes with no progress

### 26.4 How to Ask for Help

When escalating, provide:
- What you were trying to do
- What you tried
- What happened vs what expected
- Relevant error messages or logs

---

## 27. Code Quality Standards

Best-in-class practices for writing production-quality Python code.

### 27.1 Python Idioms

#### Context Managers — Always Use Them for Resources

```python
# CORRECT - context manager handles cleanup
with open('/path/to/file', 'r') as f:
    content = f.read()

# With transaction
with conn.begin_transaction() as txn:
    do_stuff(txn)
    txn.commit()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    resource = acquire_resource(name)
    try:
        yield resource
    finally:
        release_resource(resource)

# Usage
with managed_resource("cache") as cache:
    cache.get("key")

# WRONG - manual cleanup risks exceptions
try:
    f = open('/path/file', 'r')
    content = f.read()
finally:
    f.close()  # If read() throws, this doesn't run
```

#### Type Choices — dataclass vs NamedTuple vs TypedDict vs Class

```python
# Use dataclass for: simple data containers with automatic methods
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

@dataclass
class InventoryItem:
    name: str
    unit_price: float
    quantity_on_hand: int = 0
    tags: list[str] = field(default_factory=list)  # NEVER use mutable default!

# Use NamedTuple for: immutable lightweight structs
from typing import NamedTuple

class Employee(NamedTuple):
    name: str
    id: int
    department: str = "Engineering"

# Use TypedDict for: dict with specific key types (JSON-like data)
from typing import TypedDict, Required, NotRequired

class Movie(TypedDict, total=True):
    title: Required[str]
    year: int  # Required when total=True
    director: NotRequired[str]

# Use class for: complex behavior, inheritance, encapsulation
class DatabaseConnection:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    def connect(self) -> None:
        """Establish connection to database."""
        ...
```

#### List Comprehensions vs Loops vs Generators

```python
# Use list comprehension for: simple transformations/filtering
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# Use dict comprehension for: key-value transformations
squares_dict = {x: x**2 for x in range(10)}
filtered = {k: v for k, v in original.items() if v > 1}

# Use generators for: large sequences, memory efficiency, pipelining
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Generator expression - O(1) memory for million items
million_squares = (x**2 for x in range(1_000_000))  # No memory used yet!

# Generator pipeline - memory efficient
def process_large_file(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            yield parse_line(line)

# WRONG - loop when comprehension fits (less readable)
result = []
for x in items:
    if x > 0:
        result.append(x * 2)

# CORRECT
result = [x * 2 for x in items if x > 0]
```

---

### 27.2 Anti-Patterns — NEVER Do These

#### Mutable Default Arguments

```python
# WRONG - shared mutable default causes bugs
def append_to_list(item, items=[]):
    items.append(item)
    return items

append_to_list(1)  # Returns [1]
append_to_list(2)  # Returns [1, 2] — BUG!

# CORRECT - None + create new
def append_to_list(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# For dataclasses, use default_factory
from dataclasses import field

@dataclass
class Node:
    children: list['Node'] = field(default_factory=list)
```

#### Global State

```python
# WRONG - hidden mutable state
_counter = 0

def increment():
    global _counter
    _counter += 1

# CORRECT - encapsulate
class Counter:
    def __init__(self):
        self._count = 0

    def increment(self):
        self._count += 1

    @property
    def count(self):
        return self._count
```

#### Circular Imports

```python
# WRONG - circular dependency
# module_a.py
from module_b import something  # If module_b imports from module_a

# CORRECT - use TYPE_CHECKING for type hints
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module_b import Something  # Only for type checking, not runtime

# Or use late imports inside functions
def some_function():
    from module_b import something  # Deferred import
    return something()
```

#### Using type() for Type Checking

```python
# WRONG
if type(obj) is type(1):
    obj.do_something()

# CORRECT - use isinstance()
if isinstance(obj, int):
    obj.do_something()

if isinstance(obj, (int, float)):
    handle_numeric(obj)
```

#### Bare except / Catching Exception

```python
# WRONG - catches everything including KeyboardInterrupt
try:
    do_something()
except:  # NEVER do this
    print("Error")

# CORRECT - catch specific exceptions
try:
    result = collection[key]
except KeyError:
    return key_not_found(key)
```

---

### 27.3 Security Constraints — MANDATORY

#### SQL Injection Prevention

```python
# WRONG - SQL injection vulnerable
query = f"SELECT * FROM users WHERE name = '{name}'"
cursor.execute(query)

# CORRECT - parameterized queries
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))

# Using SQLAlchemy
from sqlalchemy import text

query = text("SELECT * FROM users WHERE name = :name")
result = session.execute(query, {"name": name})
```

#### Input Validation

```python
import re
from urllib.parse import urlparse

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_filename(filename: str) -> str:
    # Remove path components and special characters
    return re.sub(r'[^a-zA-Z0-9.-]', '', filename)

def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
```

#### NO eval()/exec() on User Input

```python
# WRONG - code injection vulnerability
user_input = "os.system('rm -rf /')"
result = eval(user_input)  # DANGEROUS!

# CORRECT - safe literal evaluation only
import ast

def safe_eval(expression: str):
    try:
        return ast.literal_eval(expression)  # Only parses literals
    except ValueError:
        raise ValueError(f"Invalid literal: {expression}")
```

#### File Path Traversal Prevention

```python
from pathlib import Path

def safe_read_file(base_dir: Path, user_path: str) -> str:
    requested_path = (base_dir / user_path).resolve()

    if not requested_path.is_relative_to(base_dir):
        raise ValueError("Access denied: path outside allowed directory")

    return requested_path.read_text()
```

#### Secure Password Handling

```python
import bcrypt
import secrets

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def generate_token() -> str:
    return secrets.token_urlsafe(32)
```

---

### 27.4 Performance Patterns

#### String Concatenation — Use join(), Not + in Loops

```python
# WRONG - O(n²) in loop
result = ""
for item in items:
    result += str(item)

# CORRECT - O(n)
result = "".join(str(item) for item in items)

# For building from parts
parts = ["Hello", name, "!"]
final = " ".join(parts)
```

#### Avoiding N+1 Query Patterns

```python
# WRONG - N+1 problem
users = session.query(User).all()
for user in users:
    print(user.posts.count())  # Query per user!

# CORRECT - eager loading
from sqlalchemy.orm import joinedload, selectinload

users = session.query(User).options(
    joinedload(User.posts)
).all()
for user in users:
    print(len(user.posts))  # No additional queries

# CORRECT - use subqueries for aggregations
from sqlalchemy import func

user_post_counts = session.query(
    User.id,
    func.count(Post.id).label('post_count')
).outerjoin(Post).group_by(User.id).all()
```

#### When to Use Generators

```python
# Use when: large dataset, streaming, don't need random access
def process_large_file(filepath):
    with open(filepath, 'r') as f:
        for line in f:  # One line at a time, O(1) memory
            yield parse_line(line)

# Generator expression - lazy evaluation
squares = (x**2 for x in range(1_000_000))  # No computation yet

# Pipeline - memory efficient chaining
def filter_even(numbers):
    return (x for x in numbers if x % 2 == 0)

def double(numbers):
    return (x * 2 for x in numbers)

result = filter_even(double(range(1_000_000)))  # O(1) memory
```

#### Avoiding Unnecessary Copies

```python
# WRONG - unnecessary copies waste memory
original = [1, 2, 3]
backup = original[:]  # Creates copy when you might not need it

# CORRECT - only copy when needed
def modify_list(lst):
    lst_copy = lst.copy()  # Explicit copy when required
    # modify copy, original unchanged

# For dicts
copy_dict = original_dict.copy()  # Shallow copy

# For deep copies of nested structures
import copy
deep_copy = copy.deepcopy(nested_structure)
```

---

### 27.5 Documentation Quality

#### Docstrings — Google Style for All Public APIs

```python
def calculate_area(width: float, height: float) -> float:
    """Calculate the area of a rectangle.

    Args:
        width: The width of the rectangle in units.
        height: The height of the rectangle in units.

    Returns:
        The area in square units.

    Raises:
        ValueError: If width or height is negative.
    """
    if width < 0 or height < 0:
        raise ValueError("Dimensions must be non-negative")
    return width * height

class DataProcessor:
    """Transforms raw input data into structured format.

    Handles edge cases like missing values, type mismatches,
    and provides consistent output regardless of input variations.

    Attributes:
        validation_mode: If True, raises on invalid data.
        default_value: Fallback for missing fields.
    """

    def process(self, data: dict) -> ProcessedData:
        """Process raw data dictionary."""
```

#### Comments — Explain WHY, Not WHAT

```python
# GOOD comment - explains WHY (not what code already says)
# We use depth-first search because it preserves path order
# needed for the undo system to work correctly
def find_path(graph, start, end):
    ...

# WRONG comment - states the obvious
# Increment counter by 1
counter += 1

# GOOD inline comment for non-obvious behavior
result = [x for x in items if x > 0]  # Filter out negatives/zero

# Use TODO/FIXME for temporary notes
# TODO: Remove this hack after fixing upstream bug
# FIXME: Race condition on concurrent access
```

---

### 27.6 Testing Quality

#### Arrange-Act-Assert Pattern

```python
def test_transfer_funds():
    # Arrange - set up test data
    source = Account(balance=100)
    destination = Account(balance=50)

    # Act - perform the action under test
    result = transfer_funds(source, destination, 25)

    # Assert - verify outcomes
    assert result is True
    assert source.balance == 75
    assert destination.balance == 75
```

#### Test Isolation — No Interdependencies

```python
# WRONG - tests depend on each other
global user_id
def test_create_user():
    global user_id
    user_id = create_user("Alice")

def test_update_user():  # Depends on test_create_user running first!
    update_user(user_id, name="Bob")

# CORRECT - each test is fully independent
def test_create_user():
    user = create_user("Alice")
    assert user.id is not None

def test_update_user():
    user = create_user("Bob")
    updated = update_user(user.id, name="Charlie")
    assert updated.name == "Charlie"
```

#### Mock vs Real vs Spy

```python
# Mock - completely replace dependency
from unittest.mock import Mock

def test_order_processor():
    mock_db = Mock()
    mock_db.save.return_value = True

    processor = OrderProcessor(db=mock_db)
    result = processor.process(Order(id=1))

    mock_db.save.assert_called_once()

# Spy - watch calls but use real implementation
def test_logger_calls_write():
    with patch('app.file_write') as mock_write:
        logger = Logger()
        logger.write("message")

        mock_write.assert_called_once_with("message")

# Real object - integration test
def test_database_connection():
    db = RealDatabaseConnection()  # Integration test
    db.connect()
    assert db.is_connected()
```

#### What Makes a Good Test

```python
# GOOD - clear name, tests one thing, readable
def test_user_creation_with_valid_data():
    """User can be created with valid name and email."""
    user = User(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"

# GOOD - edge case testing
def test_negative_dimensions_raise_value_error():
    """Negative width or height raises ValueError."""
    with pytest.raises(ValueError):
        calculate_area(-5, 10)

# BAD - too generic, tests too much
def test_stuff():
    result = do_something()
    assert result is not None
```

---

### 27.7 Error Handling Patterns

#### Specific Exception Catching

```python
# CORRECT - catch specific exceptions
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Invalid data format: {e}")
except KeyError as e:
    logger.error(f"Missing required key: {e}")
except TimeoutError:
    logger.warning("Operation timed out, retrying")

# Best practice - minimal try block
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)  # Only runs if no exception
```

#### Exception Chaining — Preserve Tracebacks

```python
# CORRECT - explicit chaining with 'from'
try:
    validate_input(data)
except ValidationError as e:
    raise ConfigurationError(f"Failed to load config: {e}") from e

# CORRECT - implicit chaining (re-raise after handling)
try:
    config = load_config(path)
except FileNotFoundError:
    raise ConfigurationError(f"Config not found: {path}") from None

# WRONG - loses original traceback
try:
    do_something()
except SomeError:
    raise OtherError("Message")  # from e is missing!
```

#### Custom Exception Design

```python
class AppError(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class ResourceNotFoundError(AppError):
    """Raised when a requested resource is not found."""
    pass

# Usage
def get_user(user_id):
    user = db.find_user(user_id)
    if not user:
        raise ResourceNotFoundError(
            f"User {user_id} not found",
            code="USER_NOT_FOUND"
        )
```

#### Circuit Breaker Pattern

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self):
        return (time.time() - self.last_failure_time) >= self.timeout

    def _on_success(self):
        self.failures = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

#### Retry with Exponential Backoff

```python
import time
import random

@exponential_retry(max_attempts=5, base_delay=0.5, max_delay=60)
def fragile_operation():
    pass  # Will retry with backoff on failure

def exponential_retry(max_attempts=3, base_delay=1, max_delay=60):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        delay += random.uniform(0, 0.1 * delay)
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
```

---

### 27.8 Code Quality Checklist

Before marking any code complete, verify:

- [ ] **No mutable default arguments** — Use `None` + create new, or `field(default_factory=...)`
- [ ] **No global mutable state** — Encapsulate in classes, pass as parameters
- [ ] **No circular imports** — Use `TYPE_CHECKING` or late imports
- [ ] **Use isinstance() not type()** — For type checking
- [ ] **No bare except** — Catch specific exceptions only
- [ ] **No eval()/exec()** — On any user input
- [ ] **SQL uses parameterized queries** — Never string interpolation
- [ ] **Input validated and sanitized** — Every external input
- [ ] **Context managers used** — For file/database/connection resources
- [ ] **Type hints on all public APIs** — Functions, classes, methods
- [ ] **Docstrings on all public APIs** — Google style with Args/Returns/Raises
- [ ] **Comments explain WHY** — Not what code already says
- [ ] **Tests follow AAA pattern** — Arrange, Act, Assert
- [ ] **Tests are isolated** — No interdependencies
- [ ] **Generators for large data** — Memory efficiency
- [ ] **String join() not + in loops** — Performance
- [ ] **No N+1 queries** — Use eager loading or subqueries
- [ ] **Exception chaining preserved** — Use `from e` when appropriate
- [ ] **Custom exceptions inherit from AppError** — Consistent hierarchy

---

## 28. Default Tech Stack Playbook

Best-in-class recommendations for common project types, based on analysis of top GitHub projects (FastAPI, Next.js, Gin, etc.) and current industry trends.

### 28.1 How to Use This Playbook

When starting a new project, identify the project type below and use the recommended stack.
This playbook prioritizes:
- Production-proven technologies (Microsoft, Netflix, Uber use FastAPI)
- Strong ecosystem and community support
- Best performance per complexity ratio
- Async-first for I/O-bound workloads

---

### 28.2 REST APIs

#### Python API — FastAPI (RECOMMENDED)

**Stack:** FastAPI + Pydantic + Uvicorn + SQLAlchemy + PostgreSQL

**Evidence:** Microsoft, Uber, Netflix, Cisco use FastAPI in production. 98.9k GitHub stars.

```
project/
├── src/
│   ├── api/              # FastAPI routes
│   ├── models/           # Pydantic models (request/response)
│   ├── services/         # Business logic
│   └── core/             # Config, logging, database
├── tests/
├── alembic/              # DB migrations (if using SQLAlchemy)
└── docker-compose.yml
```

**Why FastAPI:**
- Auto-generated OpenAPI docs (Swagger UI)
- Type hints throughout (mypy-friendly)
- Async support (high throughput)
- Pydantic validation built-in
- Performance on par with Node.js/Go

**When to choose FastAPI over alternatives:**
- ✅ ML model serving (first-class async, streaming responses)
- ✅ Data ingestion APIs (high throughput, validation)
- ✅ Microservices (lightweight, fast cold starts)
- ✅ Internal tooling (auto-docs save time)
- ❌ Full admin panel needed (use Django instead)
- ❌ Simple scripts (use Flask or click/typer instead)

#### Node.js API — Express.js or Fastify

**Express.js Stack:** Express + TypeORM + PostgreSQL

**Fastify Stack:** Fastify + Prisma/Drizzle + PostgreSQL

```
When to use Node.js over Python:
- Team has strong JS/TS expertise
- Frontend is React/Next.js (shared language)
- Need existing npm ecosystem integration
```

#### Go API — Gin (RECOMMENDED)

**Stack:** Gin + GORM + PostgreSQL

**Evidence:** 88.6k stars, benchmark fastest Go framework.

```
When to use Go over Python:
- Sub-millisecond latency required
- High concurrency (10k+ requests/sec)
- Memory footprint must be minimal
- Team has Go experience
```

---

### 28.3 Full-Stack Web Applications

**RECOMMENDED Stack:**

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | Next.js 15 (App Router) | SSR/SSG, React 18, API routes |
| Styling | Tailwind CSS + shadcn/ui | Utility-first, accessible components |
| API | FastAPI (Python) or Route handlers | FastAPI for complex, Next.js for simple |
| Database | PostgreSQL | ACID, JSON, vectors, pgvector |
| Cache | Redis | Sessions, rate limiting, caching |
| Search | Typesense or Meilisearch | Typo-tolerant, fast |
| Auth | NextAuth.js or custom JWT | NextAuth for Next.js, JWT for others |
| Deploy | Vercel (frontend) + Railway/Render (backend) | Easiest scaling |

**Project Structure:**

```
web-app/
├── frontend/                 # Next.js app
│   ├── app/                # App Router pages
│   ├── components/         # UI components (shadcn/ui)
│   ├── lib/                # Utilities
│   └── public/             # Static assets
├── backend/                 # FastAPI
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── core/
│   └── docker-compose.yml
├── postgres/
├── redis/
└── docker-compose.yml
```

---

### 28.4 Data Pipelines / Scraping

**Stack:** Python + FastAPI/Flask + Celery + Redis + PostgreSQL + Playwright/Scrapy

**For heavy scraping:**
```
Crawler → Playwright/Scrapy → Task Queue (Celery) → Processing (Pandas/Polars) → Database
                ↓
         Rate limiting (Redis)
         Duplicate detection (PostgreSQL)
```

**Key libraries:**
- **Scrapy** — Large-scale crawling, built-in rate limiting
- **Playwright** — JS-rendered pages, headless browsers
- **Celery** — Distributed task queue with Redis broker
- **Pandas/Polars** — Data processing (Polars for speed)
- **BeautifulSoup** — Simple HTML parsing

---

### 28.5 Machine Learning / AI Applications

**Model Serving Stack:** FastAPI + Uvicorn + PyTorch/TensorFlow

```
# Production ML serving pattern
import torch
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict")
async def predict(data: InputData):
    with torch.no_grad():
        result = model(input_tensor)
    return {"prediction": result.tolist()}
```

**LLM Applications:**
- **LangChain / LlamaIndex** — RAG, agents, tool use
- **vLLM** — High-throughput LLM inference (PagedAttention)
- **pgvector** — Vector storage in PostgreSQL
- **Redis** — Semantic caching for LLM responses

**Data Processing:**
- **Polars** — Fast DataFrame library (10x pandas)
- **Dask** — Parallel pandas for out-of-memory data
- **Apache Arrow** — Columnar format for interchange

---

### 28.6 Real-Time Applications

**Stack:** Socket.io + FastAPI + Redis + PostgreSQL

```
Client ←→ Socket.io Server ←→ Redis (pub/sub) ←→ Background workers
                ↓
         FastAPI REST API (fallback)
```

**When to use WebSocket vs SSE:**
- **WebSocket (Socket.io):** Bidirectional, low latency, complex state
- **SSE (Server-Sent Events):** Server→client only, simpler, HTTP/2 friendly

**Key patterns:**
```python
# Redis pub/sub for multi-server WebSocket
# Channels: user-specific, room-specific, broadcast
```

---

### 28.7 CLI Tools

#### Python CLI — Typer (RECOMMENDED)

**Evidence:** Created by FastAPI team, 18k+ stars.

```python
import typer

app = typer.Typer()

@app.command()
def create(name: str, email: str):
    """Create a new user."""
    ...
```

**Why Typer:**
- Type hints = automatic CLI argument parsing
- Google-style docstrings = help text
- Same team as FastAPI (consistent DX)

#### Go CLI — Cobra

**Evidence:** Used by Kubernetes, Docker CLI. 35k+ stars.

**When to use:**
- Cross-compilation to multiple platforms
- Team has Go experience
- Need to integrate with Go ecosystem

---

### 28.8 Embedded / Firmware Projects

**Note:** This differs from typical software projects. See also: `/app/70d/` for Canon camera firmware example.

**Languages:**
- **C/C++** — Industry standard, maximum control
- **Rust** — Memory safety without GC, embedded support growing
- **Zig** — Emerging, systems programming with modern tooling

**When starting firmware projects:**
- Document target hardware in DEEPDIVE.md
- Track build sizes in commits
- Use QEMU for development/testing when possible

---

### 28.9 Quick Reference Table

| Project Type | Language | Framework | Database | Cache | Notes |
|-------------|----------|-----------|----------|-------|-------|
| REST API (general) | Python | FastAPI | PostgreSQL | Redis | First choice |
| REST API (high-perf) | Go | Gin | PostgreSQL | Redis | Sub-ms latency |
| REST API (Node team) | TypeScript | Express/Fastify | PostgreSQL | Redis | Team familiarity |
| Full-stack Web | TypeScript | Next.js | PostgreSQL | Redis | SSR + API routes |
| ML Model Serving | Python | FastAPI | - | Redis | Async + streaming |
| Data Pipeline | Python | FastAPI/Flask | PostgreSQL | Redis | Celery for workers |
| Real-time App | Python/TS | Socket.io | PostgreSQL | Redis | Bidirectional |
| CLI Tool | Python | Typer | - | - | Use click as alternative |
| CLI Tool | Go | Cobra | - | - | Cross-platform |
| Web Scraper | Python | Scrapy | PostgreSQL | Redis | Rate limiting built-in |
| Content Site | TypeScript | Next.js | PostgreSQL | Redis | SSG + ISR |

---

### 28.10 Tech Stack Decision Tree

When unsure what stack to choose:

```
Is it a web app with user-facing UI?
├── Yes → Next.js + Tailwind + shadcn/ui
└── No ↓

Is it an API/service?
├── Does it need ML/AI model serving?
│   ├── Yes → FastAPI + PyTorch
│   └── No ↓
├── High performance needed?
│   ├── Yes → Go/Gin or Rust/Actix
│   └── No ↓
└── Team expertise?
    ├── Python → FastAPI
    ├── Node → Express/Fastify
    └── Go → Gin

Is it a CLI tool?
├── Python team → Typer
└── Go team → Cobra

Is it embedded/firmware?
└── C/C++ (standard) or Rust (modern)
```

---

### 28.11 Anti-Recommendations

**Avoid these (unless specific reason):**
- **Django** — Overkill for APIs, use FastAPI instead
- **Flask alone** — Use FastAPI for new projects (better async, auto-docs)
- **Mongoose** — Use Prisma/Drizzle for TypeScript (better DX)
- **MongoDB** — Use PostgreSQL for most cases (ACID, JSON support)
- **REST framework (Django)** — Use FastAPI instead
- **Express alone** — Use Fastify for new projects (faster, schema validation)

---

## Change Log

| Date | Change |
|------|--------|
| 2026-06-03 | Initial standardized AGENTS.md from 21 project AGENTS.md files |
| 2026-06-03 | Added Section 21: AI Agent Instruction Guidance from AgentBench/CAMEL research |
| 2026-06-03 | Added tests/docs/research folder requirements, tests/ always gitignored, auto-commit after validation, rogue prevention rule |
| 2026-06-03 | Added comprehensive pre-commit lint/vulture sweep requirement |
| 2026-06-03 | Added human-sounding commit message guidelines with WHY-focused pattern |
| 2026-06-03 | Added DEEPDIVE.md requirement for living system narrative documentation |
| 2026-06-03 | Added Sections 22-26: Multi-agent patterns, verification gates, failure modes, common gotchas, getting help |
| 2026-06-03 | Added Section 27: Comprehensive code quality standards (Python idioms, anti-patterns, security, performance, testing, error handling) |
| 2026-06-03 | Added Section 28: Default tech stack playbook (FastAPI, Next.js, Gin, databases, decision tree, anti-recommendations) |