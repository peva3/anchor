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
All checks must pass. No exceptions. (Section 9)

Pre-commit hooks (Section 37) are mandatory. Install once: `pre-commit install`.

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
- 500 lines max for complex logic
- Single feature per PR
- Use PR template with HUMAN/AGENT sections (Section 35)

## AI Code Quality (Section 34)

Self-check before submitting:
- Think first — explain architecture before coding
- Spot laziness — trivial tests, wide types, catch-n-log
- Spot uncertainty — defensive code, redundant checks, excessive try/except
- Spot bloat — commenting on changes, over-logging, future-proofing

## Pre-Commit Hooks (Section 37)

Mandatory. Install once: `pre-commit install`. Hooks run on every commit.
Catches secrets, lint, type errors, dead code before they reach the repo.

## Multi-Agent Cooperation (Sections 22-23)

When working with other agents:
- Define explicit roles (Role/Goal/Backstory pattern)
- Sequential handoffs with verification gates
- Termination criteria defined upfront
- Error recovery: retry → alternative → fallback → escalate

## Decision Ladder (Section 50.1)

Before writing any code, check each rung:
1. YAGNI — Does this need to exist?
2. Stdlib — Does the language already ship this?
3. Native — Does the platform already provide this?
4. Existing dep — Is this already in the project?
5. One line — Can one line do it?
6. Minimum — Shortest implementation that works

## Tradeoff Comments (Section 50.2)

For every intentional shortcut, document with a structured comment naming the ceiling:
```python
# ponytail: <what was skipped>
# Upgrade to <what> if <measurable trigger>
```

## Quick Checklist

- [ ] Read AGENTS.md and DEEPDIVE.md
- [ ] Understand project structure (tests/, docs/, research/)
- [ ] Run lint/vulture/mypy before any commit
- [ ] Run pre-commit hooks (Section 37)
- [ ] Write human-sounding commit messages
- [ ] Update DEEPDIVE.md after architectural changes
- [ ] Never go rogue — ask for approval for GitHub activity
- [ ] PR under 800 lines, single feature
- [ ] AI anti-pattern self-check passed
- [ ] Decision ladder applied to every implementation
- [ ] Tradeoff comments for intentional shortcuts
