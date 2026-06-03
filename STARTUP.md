# STARTUP.md — Project Bootstrap Guide

> This file guides an AI agent to fully populate a new project with all required files and structures.
> Read all instructions and execute them in order.

## PHASE 1: Create Directory Structure

First, create the required folder structure:

```bash
mkdir -p src/api src/models src/services src/core tests/unit tests/integration tests/scripts docs/adr docs/workflows research papers github whitepapers scripts docker/.github workflows .github .cursor/rules .windsurf .continue .claude/projects
```

## PHASE 2: Create All Agent Configuration Files

### 2.1 Create CLAUDE.md

```markdown
# CLAUDE.md — Claude Code Agent Instructions

> This file provides instructions to Claude Code (Anthropic's CLI agent).
> For full project guidance, see AGENTS.md.

**All project rules, patterns, and requirements are defined in AGENTS.md.**

Read AGENTS.md before making any changes. Follow every section:
- Section 1: Core Principles (no dead code, test-first, proven integration)
- Section 2: Commit Protocol (auto-push after validation if gh works)
- Section 5: Project Structure (tests/, docs/, research/ folders required)
- Section 9: Linting (full vulture sweep before every commit)
- Section 15: Human-sounding commits (WHY-focused, not AI-sounding)
- Section 27: Code Quality Standards (Python idioms, anti-patterns, security)
- Section 28: Tech Stack Playbook (FastAPI, Next.js, Gin, etc.)
- Section 29: Operational Patterns (circuit breaker, DLQ, middleware, cache)
- Section 30: Health Endpoint Specification
- Section 31: Production Security Patterns
- Section 32: Docker Support

**Never go rogue.** Do not create PRs, issues, or GitHub activity without explicit user approval.

For system architecture details, see DEEPDIVE.md in the project root.
```

### 2.2 Create CLAUDE.desktop.md

```markdown
# CLAUDE.desktop.md — Claude Desktop App Instructions

> Loaded automatically when this repo is opened in the Claude desktop app.

## Required Reading

**You MUST read these files before working:**
1. `AGENTS.md` — All project rules and conventions (mandatory)
2. `DEEPDIVE.md` — System architecture and design decisions

## Critical Rules from AGENTS.md

### Before Any Commit
```bash
ruff check . && ruff format . && vulture . && mypy .
```

### Required Folders
- `tests/` — All tests + random scripts (always gitignored)
- `docs/` — Architecture documentation
- `research/` — Whitepapers, references

### Commit Style
Explain WHY changes were made, not just WHAT changed.

### Prohibited
- NO PRs, issues, or GitHub activity without explicit user approval
- NO dead code or unused imports
- NO commits without passing full lint/vulture sweep

## Architecture Context

See DEEPDIVE.md for detailed system narrative including:
- Why the project is structured this way
- Key architectural decisions and trade-offs
- Known failure modes and gotchas
```

### 2.3 Create .github/copilot-instructions.md

```markdown
# GitHub Copilot Instructions

> All project rules are defined in `AGENTS.md`. Read it before writing any code.

## Required Reading

**Before any task, read these files:**
- `AGENTS.md` — All project rules and conventions
- `DEEPDIVE.md` — System architecture narrative
- `docs/` — Project documentation

## Critical Rules

1. **No dead code** — Remove unused functions, imports, variables immediately
2. **Test-first** — Write tests before code, verify all pass before committing
3. **Full cleanup sweep** before every commit:
   ```bash
   ruff check . && ruff format . && vulture . && mypy .
   ```
4. **tests/ folder** — All tests and random scripts go here; always in `.gitignore`
5. **docs/ and research/** — Create for every new project
6. **Human-sounding commits** — Explain WHY changes were made, not just WHAT changed
7. **DEEPDIVE.md** — Update after any architectural change

## Prohibited Actions

- **NEVER** create PRs, issues, or GitHub activity without explicit user approval
- **NEVER** leave dead code, stubs, or silent exception handlers
- **NEVER** commit without running the full lint/vulture sweep first

## Project Structure

```
project/
├── src/              # Source code
├── tests/            # All tests (gitignored)
├── docs/             # Architecture docs
├── research/         # Research files
├── DEEPDIVE.md       # System narrative
├── AGENTS.md         # This file
└── TODO.md           # Task tracking
```

## Validation Checklist

Before marking any task complete:
- [ ] All tests pass
- [ ] `ruff check .` clean
- [ ] `vulture .` finds no dead code
- [ ] `mypy .` clean (if Python)
- [ ] Human-sounding commit message explaining WHY
- [ ] DEEPDIVE.md updated if architecture changed
```

### 2.4 Create .cursor/rules/project-rules.mdc

```markdown
# Cursor AI Rules

> These rules are loaded automatically for this project. See `AGENTS.md` for full details.

## Core Directives

1. **Read AGENTS.md before any task** — All rules are defined there
2. **Read DEEPDIVE.md** — System architecture narrative
3. **Follow every section** — Core principles, commit protocol, testing, linting, etc.

## Critical Enforcements

### Pre-Commit Checklist
```bash
ruff check . && ruff format . && vulture . && mypy .
```
**Do not commit until all pass.**

### Required Folders
Every project MUST have:
- `tests/` — All tests + random scripts (in `.gitignore`)
- `docs/` — Architecture documentation
- `research/` — Whitepapers, references

### Commit Style
Human-sounding, WHY-focused messages.

### DEEPDIVE.md
Update after ANY architectural change. Document:
- Why the system is built this way
- Key decisions and trade-offs
- Gotchas and failure modes

## Prohibited
- No PRs/issues/GitHub activity without explicit user approval
- No dead code, unused imports, silent exception handlers
- No commits without running lint/vulture sweep first

## Validation
Before marking complete:
- [ ] Tests pass
- [ ] No vulture findings
- [ ] Type check clean
- [ ] DEEPDIVE.md updated if needed
- [ ] Human commit message
```

### 2.5 Create .windsurf/config.md

```markdown
# Windsurf AI Configuration

> Project-level rules for Windsurf Code agent. See `AGENTS.md` for complete guidelines.

## How to Use

1. Read `AGENTS.md` before starting any work
2. Read `DEEPDIVE.md` for system architecture context
3. Follow all rules in AGENTS.md — they apply to every file and every task

## Pre-Commit Validation

Run before every commit:
```
ruff check . && ruff format . && vulture . && mypy .
```

Clean = commit. Dirty = fix first.

## Project Structure Requirements

```
project/
├── src/           # Source code
├── tests/         # Tests + random scripts (gitignored)
├── docs/          # Documentation
├── research/      # Research files
├── DEEPDIVE.md    # System narrative (update on architecture changes)
├── AGENTS.md      # Project rules (this file references it)
└── TODO.md        # Task tracking
```

## Critical Rules

| Rule | Description |
|------|-------------|
| No dead code | Remove unused functions/imports immediately |
| Test-first | Write tests before code |
| Human commits | WHY-focused, not "fix: bug" |
| Auto-push | After validation, if gh works, push |
| Never rogue | No GitHub activity without user approval |
| Update DEEPDIVE | After any architectural change |

## Prohibited Actions

- Creating PRs, issues, comments without explicit user approval
- Leaving dead code or unused imports
- Committing without lint/vulture sweep passing
- Skipping tests or validation
```

### 2.6 Create .continue/config.md

```markdown
# Continue.dev Configuration

> Config for Continue.dev AI assistant. See `AGENTS.md` for full rules.

## Workspace Rules

1. **AGENTS.md is mandatory** — Read before any task
2. **DEEPDIVE.md** — Read for system architecture context
3. Follow all project conventions in AGENTS.md

## Pre-Commit Checklist

```bash
ruff check .          # Lint
ruff format .         # Format
vulture .             # Dead code detection
mypy .                # Type checking
```

All must pass before committing.

## Project Structure Requirements

- `tests/` — All tests and random scripts (always gitignored)
- `docs/` — Required for every project
- `research/` — Required for every project
- `DEEPDIVE.md` — Living system narrative, update on architecture changes

## Commit Guidelines

Human-sounding commit messages that explain WHY:
```
<type>: <what changed>

<problem>: Why this needed fixing
<solution>: What the change does and why
<context>: Decisions, trade-offs, gotchas
```

## Prohibited

- GitHub PRs/issues without explicit user approval
- Dead code or unused imports
- Skipping lint/vulture sweep
- Skipping tests

## Quick Reference

| Command | Purpose |
|---------|---------|
| `ruff check .` | Lint check |
| `ruff format .` | Format code |
| `vulture .` | Find dead code |
| `mypy .` | Type check |
```

### 2.7 Create docs/AGENT_INSTRUCTIONS.md

```markdown
# AGENT_INSTRUCTIONS.md — Universal AI Agent Instructions

> This file provides a fallback reference for any AI agent that doesn't have
> a native configuration mechanism. All agents should read AGENTS.md first.

## For Any AI Agent

1. **Read `AGENTS.md`** before starting any work — it contains all project rules
2. **Read `DEEPDIVE.md`** for system architecture context
3. **Follow all sections** in AGENTS.md

## Pre-Commit Validation

Before every commit, run:
```bash
ruff check . && ruff format . && vulture . && mypy .
```

All checks must pass. No exceptions.

## Required Project Elements

Every project must have:
- **`tests/`** — All tests + random scripts (in `.gitignore`)
- **`docs/`** — Architecture documentation
- **`research/`** — Whitepapers and references
- **`DEEPDIVE.md`** — Living system narrative (update after architecture changes)

## Prohibited Actions

1. **No GitHub activity** without explicit user approval (PRs, issues, comments)
2. **No dead code** — Remove unused functions/imports immediately
3. **No silent failures** — No `except Exception: pass`
4. **No commits** without passing full lint/vulture sweep

## Commit Message Style

Human-sounding, WHY-focused.

## Multi-Agent Cooperation

When working with other agents:
- Define explicit roles (Role/Goal/Backstory pattern)
- Sequential handoffs with verification gates
- Termination criteria defined upfront
- Error recovery: retry → alternative → fallback → escalate

## Quick Checklist

- [ ] Read AGENTS.md and DEEPDIVE.md
- [ ] Understand project structure (tests/, docs/, research/)
- [ ] Run lint/vulture/mypy before any commit
- [ ] Write human-sounding commit messages
- [ ] Update DEEPDIVE.md after architectural changes
- [ ] Never go rogue — ask for approval for GitHub activity
```

### 2.8 Create .claude/config.json

```json
{
  "project": {
    "name": "CHANGE_ME",
    "description": "Project description — update this",
    "readme": "README.md",
    "always_read": [
      "AGENTS.md",
      "DEEPDIVE.md"
    ]
  },
  "rules": {
    "enforce_vulture_sweep": true,
    "enforce_test_folder_gitignore": true,
    "enforce_docs_research_folders": true,
    "auto_commit_after_validation": true,
    "no_rogue_github_activity": true
  },
  "validation": {
    "pre_commit_checklist": [
      "ruff check .",
      "ruff format .",
      "vulture .",
      "mypy ."
    ],
    "required_folders": [
      "tests/",
      "docs/",
      "research/"
    ]
  }
}
```

### 2.9 Create .claude/projects/standardized-markdown.json

```json
{
  "project": {
    "name": "CHANGE_ME",
    "description": "Project description — update this",
    "readme": "README.md",
    "always_read": [
      "AGENTS.md",
      "DEEPDIVE.md"
    ]
  },
  "rules": {
    "enforce_vulture_sweep": true,
    "enforce_test_folder_gitignore": true,
    "enforce_docs_research_folders": true,
    "auto_commit_after_validation": true,
    "no_rogue_github_activity": true
  },
  "validation": {
    "pre_commit_checklist": [
      "ruff check .",
      "ruff format .",
      "vulture .",
      "mypy ."
    ],
    "required_folders": [
      "tests/",
      "docs/",
      "research/"
    ]
  }
}
```

## PHASE 3: Create Core Project Files

### 3.1 Create .gitignore

```
# Environment and secrets
.env
*.pem
*.key
secrets/
credentials/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing - ALWAYS gitignore tests
tests/
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# Type check
.mypy_cache/
```

### 3.2 Create .env.example

```markdown
# Environment Variables Template
# Copy this to .env and fill in values

# Application
APP_NAME=CHANGE_ME
APP_ENV=development
APP_DEBUG=true

# API Keys (never commit real keys)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# External Services
EXTERNAL_API_KEY=
EXTERNAL_API_URL=

# Feature Flags
ENABLE_FEATURE_X=false
```

### 3.3 Create docker-compose.yml

```yaml
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://app:app@postgres:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./data:/app/data

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 3.4 Create README.md

```markdown
# CHANGE_ME — Project Name

Brief description of what this project does.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Run tests
pytest

# Start the application
python src/main.py
```

## Project Structure

```
project/
├── src/              # Source code
├── tests/            # All tests (gitignored)
├── docs/             # Documentation
├── research/          # Research files
├── AGENTS.md         # AI agent guidance
├── DEEPDIVE.md       # System architecture
└── TODO.md           # Task tracking
```

## Documentation

- [AGENTS.md](AGENTS.md) — Full project rules and guidance
- [DEEPDIVE.md](DEEPDIVE.md) — System architecture narrative
- [docs/](docs/) — Additional documentation

## Development

### Setup

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
```

### Running Tests

```bash
pytest
```

### Linting

```bash
ruff check . && ruff format . && vulture . && mypy .
```

## License

MIT
```

### 3.4 Create TODO.md

```markdown
# TODO.md — Project Name

## Legend
- ✅ Complete
- 🔄 In Progress
- ⬜ Not Started

## Current Sprint / Phase

| # | Status | Description |
|---|--------|-------------|
| 1 | ⬜ | First task |

## Completed Sprints

| Sprint | Status | Deliverable |
|--------|--------|-------------|
| 1   | ✅ | Initial project setup |

## Notes

- Document architectural decisions made during task completion
- Record any deviations from original plan and why
```

### 3.5 Create DEEPDIVE.md

```markdown
# DEEPDIVE.md — System Architecture Narrative

> This file explains HOW and WHY the system is built the way it is.
> It is a living document — update it after any architectural change.

## System Overview

What this system does and why it exists.

## Architecture Decisions

### Why This Tech Stack

**Chosen:** Python + FastAPI + PostgreSQL + Redis

**Alternatives considered:**
- Django (rejected because: over-engineered for our needs)
- Flask (rejected because: too minimal, would need to add too much)

**Why this stack:** FastAPI gives us async performance with automatic OpenAPI docs. PostgreSQL handles our relational data well. Redis provides fast caching and Celery for background jobs.

### Why This Directory Structure

```
src/
├── api/          # FastAPI routes — clean separation of HTTP layer
├── models/       # Pydantic models — input/output validation
├── services/     # Business logic — all complexity lives here
└── core/         # Config, logging, exceptions — shared infrastructure
```

**Key decisions:**
- Business logic in `services/` not in route handlers
- Models are pure data classes, no behavior
- Core contains only infrastructure, no business logic

## Data Flow

### Request Lifecycle

```
Client → FastAPI Route (/api/xxx)
      → Pydantic Validation (models/)
      → Service Layer (services/) ← Business Logic
      → Database/External APIs
      → Response
```

### Why: Services Layer

All business logic lives in services to:
1. Make it testable without HTTP layer
2. Allow multiple entrypoints (API, CLI, background jobs)
3. Keep route handlers thin

## Key Decisions

### YYYY-MM-DD: Decision Title

**Context:** What problem are we solving?

**Decision:** What we chose to do.

**Alternatives considered:**
- Option A (rejected because: reason)
- Option B (rejected because: reason)

**Consequences:** What changed as a result.
```

### 3.6 Create AGENTS.md

Copy the full AGENTS.md content from the standardized-markdown repository.

## PHASE 4: Initialize Git and Commit

```bash
git init
git add .
git commit -m "Initial project setup

- Created full directory structure (src/, tests/, docs/, research/)
- Added AI agent configuration files for Claude, Copilot, Cursor, Windsurf, Continue
- Added CLAUDE.md, CLAUDE.desktop.md for Claude Code
- Added .claude/config.json with project settings
- Created .gitignore with tests/ always excluded
- Created .env.example template
- Created docker-compose.yml with postgres and redis
- Created README.md with quick start guide
- Created TODO.md for task tracking
- Created DEEPDIVE.md as living system narrative
- Created AGENTS.md with 32 sections (all patterns from standardized-markdown)
- Created docs/AGENT_INSTRUCTIONS.md as universal fallback
- Created .github/workflows/ for CI/CD
- Created operational patterns: circuit breaker, DLQ, middleware stack
- Created security patterns: prompt injection, audit logging, key encryption
- Created Docker support with Dockerfile and Kubernetes templates"
```

---

## Summary

After completing all phases, your project will have:

| File/Folder | Purpose |
|-------------|---------|
| `AGENTS.md` | Complete project rules (32 sections) |
| `DEEPDIVE.md` | System architecture narrative |
| `CLAUDE.md` | Claude Code instructions |
| `CLAUDE.desktop.md` | Claude desktop app instructions |
| `.github/copilot-instructions.md` | GitHub Copilot instructions |
| `.cursor/rules/project-rules.mdc` | Cursor AI rules |
| `.windsurf/config.md` | Windsurf configuration |
| `.continue/config.md` | Continue.dev configuration |
| `docs/AGENT_INSTRUCTIONS.md` | Universal fallback instructions |
| `.claude/config.json` | Claude project settings |
| `docker-compose.yml` | Development environment |
| `.gitignore` | Git ignore (tests/ always excluded) |
| `.env.example` | Environment variable template |
| `README.md` | Project documentation |
| `TODO.md` | Task tracking |
| `.github/workflows/` | CI/CD pipelines |
| `src/` | Source code directory |
| `tests/` | Test directory (gitignored) |
| `docs/` | Documentation directory |
| `research/` | Research files directory |

All AI agents reading from this project will find comprehensive guidance and follow consistent patterns.

## Key Sections in AGENTS.md

1. Core Principles
2. Commit Protocol
3. Shell Execution Rules
4. Code Style (English-only)
5. Project Structure (tests/, docs/, research/ required)
6. TODO.md Standard
7. Docker/Deployment
8. Testing Requirements
9. Linting & Type Checking (vulture sweep)
10. Error Handling Patterns
11. Configuration Management
12. API Design
13. Security Best Practices
14. Logging Standards
15. Git Workflow (human-sounding commits)
16. Documentation Requirements
17. Dependency Management
18. Performance Considerations
19. Build & Deployment
20. External Integrations
21. AI Agent Instruction Guidance
22. Multi-Agent Cooperation Patterns
23. Verification Gates
24. Common Failure Modes
25. Common Gotchas
26. Getting Help
27. Code Quality Standards
28. Tech Stack Playbook
29. Operational Patterns (circuit breaker, DLQ, middleware, cache)
30. Health Endpoint Specification
31. Production Security Patterns
32. Docker Support