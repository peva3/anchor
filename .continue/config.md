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

All must pass before committing. (Section 9)

Pre-commit hooks (Section 37) are mandatory: `pre-commit install`.

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
- Use the PR template (Section 35)

## Decision Ladder (Section 50.1)

Before writing code, check each rung:
1. YAGNI — Does this need to exist?
2. Stdlib — Does the language already ship this?
3. Native — Does the platform already provide this?
4. Existing dep — Is this already in the project?
5. One line — Can one line do it?
6. Minimum — Shortest implementation that works

## Tradeoff Comments (Section 50.2)

For every intentional shortcut, document with:
```python
# ponytail: <what was skipped>
# Upgrade to <what> if <measurable trigger>
```

## Pre-Commit Hooks (Section 37)

Mandatory. `pre-commit install` once. Hooks run on every commit.

## Prohibited

- GitHub PRs/issues without explicit user approval (Section 2)
- Dead code or unused imports (Section 1)
- Skipping lint/vulture sweep (Section 9)
- Skipping pre-commit hooks (Section 37)
- Skipping tests (Section 8)
- Force push to shared branches (Section 36.2)
- Mutable defaults, bare excepts, eval/exec, circular imports (Section 27.2)
- PRs over 800 lines (Section 33)

## Quick Reference

| Command | Purpose | Section |
|---------|---------|---------|
| `ruff check .` | Lint check | 9 |
| `ruff format .` | Format code | 9 |
| `vulture .` | Find dead code | 9 |
| `mypy .` | Type check | 9 |
| `pre-commit install` | Install git hooks | 37 |
| `pre-commit run --all-files` | Run all hooks | 37 |
| `pytest --cov=. --cov-fail-under=80` | Tests + coverage | 8, 40 |
| `python3 tests/test_agents_md_quality.py --strict` | Run audit (Anchor) | 50.8 |
