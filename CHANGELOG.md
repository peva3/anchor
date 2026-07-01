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
- `.pre-commit-config.yaml` — pre-commit hooks (Section 37 requirement)
- `requirements-dev.txt` — pinned versions for the audit
- `pytest.ini` — pytest discovery config
- `.github/workflows/ci.yml` — CI that runs the audit on every push and PR
- `.github/workflows/release.yml` — release automation
- `.github/PULL_REQUEST_TEMPLATE.md` — HUMAN/AGENT template (Section 35)
- `.github/ISSUE_TEMPLATE/bug_report.md` — bug report template
- `.github/ISSUE_TEMPLATE/feature_request.md` — feature request template
- `.github/CODEOWNERS` — maintainer ownership
- `.github/dependabot.yml` — weekly dependency PRs

### Changed
- `.gitignore` — now allows `tests/test_agents_md_quality.py` to be committed
- `STARTUP.md` — removed duplicate `### 3.9 Create SECURITY.md` section
- All 7 platform config files — now mention Sections 33, 37, 50.1, 50.2
- `.claude/projects/anchor.json` — removed (duplicate of `.claude/config.json`)
- `tests/test_agents_md_quality.py` — efficiency: caches file content, replaces hardcoded skip list with structural rule, makes scenario test assert, enables strict mode
- `README.md` — stats now match audit output

### Fixed
- Audit script silently re-parsed AGENTS.md on every test (now loads once)
- Audit script had print-only WARN checks that never failed CI (now strict mode)
- Audit script's contradiction detector only checked one regex (now uses keyword overlap)
- Audit script's scenario walkthrough printed but never asserted (now asserts)
- README stats were stale (now match audit output)

### Removed
- `tests/test_agents_md_quality.py` from `.gitignore` (was hiding the deliverable)
- `.claude/projects/anchor.json` (duplicate of `.claude/config.json`)

## [1.0.0] - 2026-06-19

### Added
- Initial 51-section AGENTS.md template
- STARTUP.md bootstrap guide
- All 7 platform-specific AI agent config files
- Research catalog (papers, whitepapers, github analyses)
- `tests/test_agents_md_quality.py` audit script
- MIT license
- README, CONTRIBUTING, SECURITY
