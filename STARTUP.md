# STARTUP.md — Project Bootstrap Guide

> This file guides an AI agent to fully populate a new project with all required files and structures.
> Read all instructions and execute them in order.

## PHASE 1: Create Directory Structure

First, create the required folder structure:

```bash
mkdir -p src/api src/models src/services src/core tests/unit tests/integration tests/scripts docs/adr docs/workflows research papers github whitepapers scripts docker .github .cursor/rules .windsurf .continue .claude
```

## PHASE 2: Create All Agent Configuration Files

### 2.1 Create CLAUDE.md

```markdown
# CLAUDE.md — Claude Code Agent Instructions

> This file provides instructions to Claude Code (Anthropic's CLI agent).
> For full project guidance, see AGENTS.md.

**All project rules, patterns, and requirements are defined in AGENTS.md.**

Read AGENTS.md before making any changes. Follow every section:
- Section 1-9: Core principles, commit protocol, shell execution, code style, project structure, TODO.md, Docker, testing, linting
- Section 15: Human-sounding commits (WHY-focused, not AI-sounding)
- Section 27: Code Quality Standards (Python idioms, anti-patterns, security, performance)
- Section 28: Tech Stack Playbook (FastAPI, Next.js, Gin, databases, decision tree)
- Section 29-32: Operational patterns, health endpoints, production security, Docker/K8s
- Section 33-36: PR size standards, AI anti-pattern detection, PR template, NEVER list
- Section 37-40: Pre-commit hooks, CI/CD, semantic versioning, coverage enforcement
- Section 41-44: Observability, Infrastructure as Code, database backups, secrets management
- Section 45-49: Flaky tests, mutation testing, benchmarks, contract tests, chaos engineering
- Section 50: Intentional Minimalism (decision ladder, tradeoff comments, safety carve-outs)
- Section 51: Instruction Architecture (lazy loading, self-maintenance, context budgets)

**Never go rogue.** Do not create PRs, issues, or GitHub activity without explicit user approval.

For system architecture details, see DEEPDIVE.md in the project root.
```

### 2.2 Create CLAUDE.desktop.md

```markdown
# CLAUDE.desktop.md — Claude Desktop App Instructions

> Loaded automatically when this repo is opened in the Claude desktop app.

## Required Reading

**You MUST read these files before working:**
1. `AGENTS.md` — All project rules and conventions (51 sections, mandatory)
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
Human-sounding, WHY-focused messages. See Section 15.

### PR Standards (Section 33)
- Max 800 lines per PR, 500 for complex logic
- Single feature per PR
- Use the PR template (Section 35)

### AI Code Quality (Section 34)
Self-check against anti-patterns: think first, spot laziness, uncertainty, bloat.

### Decision Ladder (Section 50)
Every implementation: YAGNI → stdlib → native → existing dep → one line → minimum code.

### Prohibited (Section 36 — NEVER List)
- NO PRs, issues, or GitHub activity without explicit user approval
- NO dead code or unused imports
- NO commits without passing full lint/vulture sweep
- NO mutable default arguments, circular imports, bare excepts
- NO eval()/exec() on user input
- NO force push to shared branches

## Architecture Context

See DEEPDIVE.md for detailed system narrative including:
- Why the project is structured this way
- Key architectural decisions and trade-offs
- Known failure modes and gotchas
- Data flow through the system
```

### 2.3 Create .github/copilot-instructions.md

```markdown
# GitHub Copilot Instructions

> All project rules are defined in `AGENTS.md`. Read it before writing any code.

## Required Reading

**Before any task, read these files:**
- `AGENTS.md` — All project rules and conventions (51 sections)
- `DEEPDIVE.md` — System architecture narrative
- `docs/` — Project documentation

## Critical Rules

1. **No dead code** — Remove unused functions, imports, variables immediately (Section 1)
2. **Test-first** — Write tests before code, verify all pass before committing (Section 8)
3. **Full cleanup sweep** before every commit: `ruff check . && ruff format . && vulture . && mypy .` (Section 9)
4. **tests/ folder** — All tests and random scripts go here; always in `.gitignore` (Section 5)
5. **docs/ and research/** — Create for every new project (Section 5)
6. **Human-sounding commits** — Explain WHY changes were made (Section 15)
7. **DEEPDIVE.md** — Update after any architectural change (Section 5)
8. **PR size limit** — 800 lines max, 500 for complex logic (Section 33)
9. **Decision ladder** — YAGNI → stdlib → native → existing dep → one line → minimum (Section 50)
10. **Tradeoff comments** — Name the ceiling and upgrade trigger for intentional shortcuts (Section 50.2)

## Prohibited Actions

- **NEVER** create PRs, issues, or GitHub activity without explicit user approval (Section 2)
- **NEVER** leave dead code, stubs, or silent exception handlers (Section 1)
- **NEVER** commit without running the full lint/vulture sweep first (Section 9)
- **NEVER** use mutable defaults, bare excepts, eval/exec, or circular imports (Section 27.2)
- **NEVER** submit code you haven't tested (Section 34.5)

## Project Structure

```
project/
├── src/              # Source code
├── tests/            # All tests (gitignored)
├── docs/             # Architecture docs
├── research/         # Research files
├── DEEPDIVE.md       # System narrative
├── AGENTS.md         # This file (51 sections)
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
- [ ] PR under 800 lines, single feature
- [ ] AI anti-pattern self-check passed (Section 34)
```

### 2.4 Create .cursor/rules/project-rules.mdc

```markdown
# Cursor AI Rules

> These rules are loaded automatically for this project. See `AGENTS.md` for full details.

## Core Directives

1. **Read AGENTS.md before any task** — All rules are defined there (51 sections)
2. **Read DEEPDIVE.md** — System architecture narrative
3. **Follow every section** — Core principles, commit protocol, testing, linting, CI/CD, security, etc.

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
Human-sounding, WHY-focused messages (Section 15).

### PR Standards
- 800 lines max, 500 for complex logic (Section 33)
- Single feature per PR (Section 33.3)
- Use the PR template (Section 35)

### AI Code Quality (Section 34)
Self-check: think first, spot laziness, uncertainty, bloat.

### DEEPDIVE.md
Update after ANY architectural change. Document:
- Why the system is built this way
- Key decisions and trade-offs
- Gotchas and failure modes

## Prohibited
- No PRs/issues/GitHub activity without explicit user approval
- No dead code, unused imports, silent exception handlers
- No commits without running lint/vulture sweep first
- No mutable default arguments, bare excepts, eval/exec (Section 27.2)
- No force push to shared branches (Section 36.2)

## Validation
Before marking complete:
- [ ] Tests pass
- [ ] No vulture findings
- [ ] Type check clean
- [ ] DEEPDIVE.md updated if needed
- [ ] Human commit message
- [ ] PR under 800 lines
- [ ] AI anti-pattern self-check passed
```

### 2.5 Create .windsurf/config.md

```markdown
# Windsurf AI Configuration

> Project-level rules for the Windsurf IDE agent.
> See `AGENTS.md` (51 sections) for complete guidelines.

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
├── AGENTS.md      # Project rules (51 sections)
└── TODO.md        # Task tracking
```

## Critical Rules

| Rule | Section |
|------|---------|
| No dead code | 1 |
| Test-first | 8 |
| Full lint/vulture sweep before commit | 9 |
| Human-sounding commits (WHY-focused) | 15 |
| PR under 800 lines, single feature | 33 |
| AI anti-pattern self-check | 34 |
| Pre-commit hooks mandatory | 37 |
| CI/CD pipeline standards | 38 |
| Semantic versioning + changelog | 39 |
| Code coverage enforcement (80% floor) | 40 |
| Decision ladder (YAGNI → minimum) | 50 |
| Tradeoff comments with named ceilings | 50.2 |
| Auto-push after validation | 2 |
| Never rogue (no GitHub without approval) | 2 |
| Update DEEPDIVE after arch changes | 5 |

## Prohibited Actions

- Creating PRs, issues, comments without explicit user approval
- Leaving dead code or unused imports
- Committing without lint/vulture sweep passing
- Skipping tests or validation
- Force pushing to shared branches
- Mutable default arguments, bare excepts, eval/exec
```

### 2.6 Create .continue/config.md

```markdown
# Continue.dev Configuration

> Config for Continue.dev AI assistant. See `AGENTS.md` (51 sections) for full rules.

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

Human-sounding commit messages that explain WHY (Section 15):
```
<type>: <what changed>

<problem>: Why this needed fixing
<solution>: What the change does and why
<context>: Decisions, trade-offs, gotchas
```

## PR Standards (Section 33)
- 800 lines max, 500 for complex logic
- Single feature per PR
- Use PR template (Section 35)

## Decision Ladder (Section 50)
Before writing code: YAGNI → stdlib → native → existing dep → one line → minimum.

## Prohibited

- GitHub PRs/issues without explicit user approval
- Dead code or unused imports
- Skipping lint/vulture sweep
- Skipping tests
- Force push to shared branches
- Mutable defaults, bare excepts, eval/exec, circular imports

## Quick Reference

| Command | Purpose | Section |
|---------|---------|---------|
| `ruff check .` | Lint check | 9 |
| `ruff format .` | Format code | 9 |
| `vulture .` | Find dead code | 9 |
| `mypy .` | Type check | 9 |
| `pre-commit install` | Install git hooks | 37 |
| `pytest --cov=. --cov-fail-under=80` | Tests + coverage | 8, 40 |
| `mutmut run --paths-to-mutate=src/` | Mutation testing | 46 |
```

### 2.7 Create docs/AGENT_INSTRUCTIONS.md

```markdown
# AGENT_INSTRUCTIONS.md — Universal AI Agent Instructions

> This file provides a fallback reference for any AI agent that doesn't have
> a native configuration mechanism. All agents should read AGENTS.md first.

## For Any AI Agent

1. **Read `AGENTS.md`** before starting any work — it contains all project rules (51 sections)
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

## Prohibited Actions (Section 36 — NEVER List)

1. **No GitHub activity** without explicit user approval (PRs, issues, comments)
2. **No dead code** — Remove unused functions/imports immediately
3. **No silent failures** — No `except Exception: pass`
4. **No commits** without passing full lint/vulture sweep
5. **No mutable defaults** — Use `None` + create new, or `field(default_factory=...)`
6. **No bare excepts** — Catch specific exception types
7. **No eval()/exec()** on user input
8. **No force push** to shared branches

## Commit Message Style

Human-sounding, WHY-focused (Section 15).

## PR Standards (Section 33)
- 800 lines max per PR
- Single feature per PR
- Use PR template with HUMAN/AGENT sections (Section 35)

## AI Code Quality (Section 34)
Self-check before submitting:
- Think first — explain architecture before coding
- Spot laziness — trivial tests, wide types, catch-n-log
- Spot uncertainty — defensive code, redundant checks, excessive try/except
- Spot bloat — commenting on changes, over-logging, future-proofing

## Multi-Agent Cooperation (Sections 22-23)

When working with other agents:
- Define explicit roles (Role/Goal/Backstory pattern)
- Sequential handoffs with verification gates
- Termination criteria defined upfront
- Error recovery: retry → alternative → fallback → escalate

## Decision Ladder (Section 50)

Before writing any code, check each rung:
1. YAGNI — Does this need to exist?
2. Stdlib — Does the language already ship this?
3. Native — Does the platform already provide this?
4. Existing dep — Is this already in the project?
5. One line — Can one line do it?
6. Minimum — Shortest implementation that works

## Quick Checklist

- [ ] Read AGENTS.md and DEEPDIVE.md
- [ ] Understand project structure (tests/, docs/, research/)
- [ ] Run lint/vulture/mypy before any commit
- [ ] Write human-sounding commit messages
- [ ] Update DEEPDIVE.md after architectural changes
- [ ] Never go rogue — ask for approval for GitHub activity
- [ ] PR under 800 lines, single feature
- [ ] AI anti-pattern self-check passed
- [ ] Decision ladder applied to every implementation
- [ ] Tradeoff comments for intentional shortcuts
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
    "no_rogue_github_activity": true,
    "enforce_pr_size_limits": true,
    "enforce_decision_ladder": true,
    "enforce_tradeoff_comments": true,
    "enforce_precommit_hooks": true
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
    ],
    "pr_size_limit_lines": 800,
    "coverage_threshold_percent": 80
  }
}
```

## PHASE 3: Create Core Project Files

### 3.1 Create .gitignore

The template includes:
```
.env, *.pem, __pycache__/, *.pyc, venv/, .vscode/, tests/ (always gitignored),
logs/, .coverage, docker-compose.override.yml, .mypy_cache/, .terraform/, pacts/
```
See `.gitignore` in the Anchor repo for the complete template.

### 3.2 Create .env.example

```
APP_NAME=CHANGE_ME
APP_ENV=development
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

### 3.3 Create docker-compose.yml

Use the template from Section 32.2 or the Anchor repo's template
with PostgreSQL, Redis, healthchecks, and named volumes.

### 3.4 Create README.md

Minimal template:
```markdown
# PROJECT_NAME

Brief description.

## Quick Start
\```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && cp .env.example .env
pytest
\```

## Docs
- [AGENTS.md](AGENTS.md) — Full project rules (51 sections)
- [DEEPDIVE.md](DEEPDIVE.md) — System architecture narrative
- [CONTRIBUTING.md](CONTRIBUTING.md) — Contribution guide
- [SECURITY.md](SECURITY.md) — Security policy

## License
MIT
```

### 3.5 Create TODO.md

Use the standard template from Section 6 with `✅ Complete`, `🔄 In Progress`, `⬜ Not Started` legend.

### 3.6 Create DEEPDIVE.md

Use the template from Section 5 covering system overview, architecture decisions, data flow, key decisions with dates, and gotchas.

### 3.7 Create AGENTS.md

Copy AGENTS.md from the Anchor repository (51 sections). Delete sections that don't apply to this project. Target ≤2,000 lines for project-specific use.

### 3.8 Create CONTRIBUTING.md

Minimal or copy from the Anchor repo:

```markdown
# Contributing
See [AGENTS.md](AGENTS.md) Sections 33-36 for PR standards.
- PRs under 800 lines, single feature
- Run ruff/vulture/mypy before committing
- Human-sounding, WHY-focused commits (Section 15)
```

### 3.9 Create SECURITY.md

Minimal or copy from the Anchor repo:
```markdown
# Security Policy
Do NOT open public issues for vulnerabilities. Use GitHub Security Advisories.
```

## PHASE 4: Initialize Git and Commit

```bash
git init
git add .
git commit -m "Initial project setup

- Created full directory structure (src/, tests/, docs/, research/)
- Added AI agent configs for Claude, Copilot, Cursor, Windsurf, Continue
- Added CLAUDE.md, CLAUDE.desktop.md, .claude/config.json
- Created .gitignore with tests/ always excluded
- Created .env.example, docker-compose.yml, README.md
- Created TODO.md, DEEPDIVE.md, CONTRIBUTING.md, SECURITY.md
- Created AGENTS.md with 51 sections (standardized template)" && \
git push origin main
```

---

## Summary

After completing all phases, your project will have:

| File/Folder | Purpose |
|-------------|---------|
| `AGENTS.md` | Complete project rules (51 sections) |
| `DEEPDIVE.md` | System architecture narrative |
| `CLAUDE.md` | Claude Code instructions |
| `CLAUDE.desktop.md` | Claude desktop app instructions |
| `.github/copilot-instructions.md` | GitHub Copilot instructions |
| `.cursor/rules/project-rules.mdc` | Cursor AI rules |
| `.windsurf/config.md` | Windsurf configuration |
| `.continue/config.md` | Continue.dev configuration |
| `docs/AGENT_INSTRUCTIONS.md` | Universal fallback instructions |
| `.claude/config.json` | Claude project settings |
| `CONTRIBUTING.md` | Contribution guidelines |
| `SECURITY.md` | Security policy |
| `LICENSE` | MIT License |
| `docker-compose.yml` | Development environment |
| `.gitignore` | Git ignore (tests/ always excluded) |
| `.env.example` | Environment variable template |
| `README.md` | Project documentation |
| `TODO.md` | Task tracking |
| `src/` | Source code directory |
| `tests/` | Test directory (gitignored) |
| `docs/` | Documentation directory |
| `research/` | Research files directory |

## Key AGENTS.md Sections (51 Total)

| Sections | Domain |
|----------|--------|
| 1-9 | Core Principles, Commit Protocol, Shell Execution, Code Style, Project Structure, TODO.md, Docker, Testing, Linting |
| 10-14 | Error Handling, Configuration, API Design, Security, Logging |
| 15 | Git Workflow — human-sounding, WHY-focused commits |
| 16-20 | Documentation, Dependencies, Performance, Build/Deployment, External Integrations |
| 21-26 | AI Agent Guidance, Multi-Agent Cooperation, Verification Gates, Failure Modes, Gotchas, Getting Help |
| 27 | Code Quality Standards — Python idioms, anti-patterns, security, performance |
| 28 | Tech Stack Playbook — FastAPI, Next.js, Gin, databases, decision tree |
| 29-32 | Operational Patterns, Health Endpoints, Production Security, Docker/K8s |
| 33-36 | PR Size Standards, AI Anti-Pattern Detection, PR Template, NEVER List |
| 37-41 | Pre-commit Hooks, CI/CD, Semantic Versioning, Code Coverage, Observability |
| 42-44 | Infrastructure as Code, Database Backup/Recovery, Secrets Management |
| 45-49 | Flaky Tests, Mutation Testing, Benchmarks, Contract Testing, Chaos Engineering |
| 50 | Intentional Minimalism — decision ladder, tradeoff comments, safety carve-outs |
| 51 | Instruction Architecture — lazy loading, self-maintenance, context budgets |
