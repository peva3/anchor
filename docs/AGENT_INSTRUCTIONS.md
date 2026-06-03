# AGENT_INSTRUCTIONS.md — Universal AI Agent Instructions

> This file provides a fallback reference for any AI agent that doesn't have
> a native configuration mechanism. All agents should read AGENTS.md first.

## For Any AI Agent

1. **Read `AGENTS.md`** before starting any work — it contains all project rules
2. **Read `DEEPDIVE.md`** for system architecture context
3. **Follow all sections** in AGENTS.md, including:
   - Core principles (no dead code, test-first, proven integration)
   - Commit protocol (auto-push after validation if gh works)
   - Project structure (tests/, docs/, research/ required)
   - Linting (vulture sweep before every commit)
   - Human-sounding commits (WHY-focused)
   - Multi-agent patterns, verification gates, failure modes
   - Common gotchas, getting help

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

Human-sounding, WHY-focused:
```
api: Added rate limiter to prevent API overload

The API had no rate limiting, allowing clients to spam requests and
cause 503 errors. Added Redis-backed rate limiter with per-IP limits.
Returns 429 when exceeded.
```

## Multi-Agent Cooperation

When working with other agents:
- Define explicit roles (Role/Goal/Backstory pattern)
- Sequential handoffs with verification gates
- Termination criteria defined upfront
- Error recovery: retry → alternative → fallback → escalate

## Failure Mode Handling

| Mode | Cause | Prevention |
|------|-------|------------|
| Invalid Format | Output schema unclear | Explicit schema with examples |
| Invalid Action | State machine violation | Validate before acting |
| Task Limit Exceeded | No solution after max tries | Early termination + escalate |
| Context Limit | Context overflow | Summarize/snapshot state |

## Quick Checklist

- [ ] Read AGENTS.md and DEEPDIVE.md
- [ ] Understand project structure (tests/, docs/, research/)
- [ ] Run lint/vulture/mypy before any commit
- [ ] Write human-sounding commit messages
- [ ] Update DEEPDIVE.md after architectural changes
- [ ] Never go rogue — ask for approval for GitHub activity