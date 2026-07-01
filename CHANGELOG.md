# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `DEEPDIVE.md` — living system narrative (Section 5 requirement)
- `TODO.md` — task tracking (Section 6 requirement)
- `CHANGELOG.md` — this file (Section 39 requirement)
- `Dockerfile` and `docker-compose.yml` — reproducible audit container
- `.env.example` — environment variable template (Section 11 requirement)
- `.pre-commit-config.yaml` — pre-commit hooks (Section 37 requirement, local only)
- `requirements-dev.txt` — pinned versions for the audit
- `pytest.ini` — pytest discovery config
- `.github/PULL_REQUEST_TEMPLATE.md` — HUMAN/AGENT template (Section 35, static markdown, no Actions)
- `.github/ISSUE_TEMPLATE/bug_report.md` — bug report template (static markdown)
- `.github/ISSUE_TEMPLATE/feature_request.md` — feature request template (static markdown)
- `.github/CODEOWNERS` — maintainer ownership (static file, no Actions)
- **Section 36.4a** — explicit GitHub Automation NEVER (no Actions, no bot PRs, no dependabot) without per-file user approval

### Changed
- `.gitignore` — now allows `tests/test_agents_md_quality.py` to be committed
- `STARTUP.md` — removed duplicate `### 3.9 Create SECURITY.md` section
- All 7 platform config files — now mention Sections 33, 37, 50.1, 50.2
- `.claude/projects/anchor.json` — removed (duplicate of `.claude/config.json`)
- `tests/test_agents_md_quality.py` — efficiency: caches file content, replaces hardcoded skip list with structural rule, makes scenario test assert, enables strict mode
- `README.md` — stats now match audit output
- Section 2 — softened the auto-push-permission language to require explicit user approval for GitHub-side automation
- Section 38 — added header explicitly deferring to Section 36.4a (no Actions without approval)

### Fixed
- Audit script silently re-parsed AGENTS.md on every test (now loads once)
- Audit script had print-only WARN checks that never failed CI (now strict mode)
- Audit script's contradiction detector only checked one regex (now uses keyword overlap)
- Audit script's scenario walkthrough printed but never asserted (now asserts)
- README stats were stale (now match audit output)
- Section 36.4 only forbade paid Actions; new Section 36.4a explicitly forbids all GitHub-side automation without per-file approval

### Removed
- `tests/test_agents_md_quality.py` from `.gitignore` (was hiding the deliverable)
- `.claude/projects/anchor.json` (duplicate of `.claude/config.json`)
- `.github/workflows/ci.yml` — created without explicit user approval, removed
- `.github/workflows/release.yml` — created without explicit user approval, removed
- `.github/dependabot.yml` — created without explicit user approval, removed

## [1.0.0] - 2026-06-19

### Added
- Initial 51-section AGENTS.md template
- STARTUP.md bootstrap guide
- All 7 platform-specific AI agent config files
- Research catalog (papers, whitepapers, github analyses)
- `tests/test_agents_md_quality.py` audit script
- MIT license
- README, CONTRIBUTING, SECURITY
