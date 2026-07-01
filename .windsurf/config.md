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
Clean = commit. Dirty = fix first. (Section 9)

Pre-commit hooks (Section 37) are mandatory. Install once: `pre-commit install`.

## Required Project Structure

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

| Rule | Section | Description |
|------|---------|-------------|
| No dead code | 1 | Remove unused functions/imports immediately |
| Test-first | 8 | Write tests before code |
| Full lint/vulture sweep | 9 | Before every commit |
| Human commits | 15 | WHY-focused, not "fix: bug" |
| PR size 800 lines | 33 | 500 for complex logic, single feature |
| AI anti-pattern check | 34 | Self-check: laziness, uncertainty, bloat |
| Pre-commit hooks | 37 | Mandatory, install once |
| CI/CD standards | 38 | ci.yml, release.yml, deploy.yml |
| SemVer + changelog | 39 | Keep a Changelog format |
| Coverage 80% | 40 | Hard floor, branch coverage preferred |
| Decision ladder | 50.1 | YAGNI → stdlib → native → existing dep → one line → minimum |
| Tradeoff comments | 50.2 | `# ponytail:` for every shortcut, name the ceiling |
| Auto-push | 2 | After validation, if `gh` works, push |
| Never rogue | 2 | No GitHub activity without user approval |
| Update DEEPDIVE | 5 | After any architectural change |

## Prohibited Actions

- Creating PRs, issues, comments without explicit user approval (Section 2)
- Leaving dead code or unused imports (Section 1)
- Committing without lint/vulture sweep passing (Section 9)
- Skipping pre-commit hooks (Section 37)
- Skipping tests or validation (Section 8)
- Force pushing to shared branches (Section 36.2)
- Mutable default arguments, bare excepts, eval/exec (Section 27.2)
- PRs over 800 lines (Section 33)

## Decision Ladder (Section 50.1)

Before any implementation, stop at the first rung that holds:
1. **YAGNI** — Does this need to exist at all?
2. **Stdlib** — Does the language already ship this?
3. **Native** — Does the platform already provide this?
4. **Existing dep** — Is it already in pyproject.toml?
5. **One line** — Can one clear line do it?
6. **Minimum** — Shortest implementation that works.

## Tradeoff Comments (Section 50.2)

For any intentional shortcut, add a structured comment:
```
# ponytail: <what was skipped>
# Upgrade to <what to build> if <measurable trigger>
```

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
