# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Sections 54-62** — nine new agent-focused skills: MCP usage & guardrails, prompt-injection defenses, agent memory & state management, tool-call permission & safety, supply-chain security & SBOM, incident response & runbooks, property-based testing, snapshot/golden-file testing, and retries/backoff/idempotency
- **Section 53.6** — AI/agentic applications project type (agents, RAG, MCP, LLM backends)
- **Section 63** — UI Quality & Anti-Slop Guardrails: no fabricated content/placeholders, no dead controls, required empty/loading/error states, WCAG AA accessibility minimums, and the ENERGY/RHYTHM/MOTION dials mechanism for enforceable visual liveliness (adapted from https://github.com/miqdadbadjuber/anti-slop)
- Section 36.9 — Prompt-Injection & Untrusted Input NEVER list

### Changed
- AGENTS.md restructured from a ~6,700-line monolith into a ~500-line entry-point plus a `skills/` library (63 lazy-loaded skill files, one per section); core rules (Sections 1, 2, 36 and selected subsections of 50/51) stay inline
- Every skill cross-reference is now a self-contained link to the referenced skill file, so a lazily-loaded skill can pull in what it points to without the always-loaded index
- Stale tooling modernized across skills: Pact v2→v3/v4, trufflehog3/safety/detect-secrets→TruffleHog/pip-audit/gitleaks, removed obsolete compose `version:` key, current mutmut config schema, bcrypt→Argon2id, OTel env-var config, bumped pre-commit hook revisions
- Contradictions fixed: duplicate 36.6 heading, 51.1 core-set claim, skill 05 tests/-gitignore conflict, PR-template AI-attribution clash

### Fixed
- Broken references to the deleted `scripts/check_structure.sh` in README, CONTRIBUTING, and DEEPDIVE (structural validation is now a documented manual check)

### Removed
- `scripts/` (structural validator) — removed from the tree, gitignored, and purged from git history
- `Dockerfile`, `docker-compose.yml`, `requirements-dev.txt` — audit container (only existed to run the now-unshipped test)
- `tests/` from the shipped tree (scratch, gitignored by design)

## [2.0.0] - 2026-08-20

### Added
- **Sections 52-62** — Rule Enforcement Architecture, Project Type Patterns (incl. AI/agentic 53.6), and nine agent-focused skills (MCP usage & guardrails, prompt-injection defenses, agent memory & state, tool-call permission & safety, supply-chain security & SBOM, incident response & runbooks, property-based testing, snapshot testing, retries/backoff/idempotency)
- Section 36.9 — Prompt-Injection & Untrusted Input NEVER list
- `skills/` — lazy-loaded library of 62 per-section skill files

### Changed
- AGENTS.md restructured from a ~6,700-line monolith into a ~500-line entry-point whose Section Index and Skills Directory link out to the 62 skill files; core rules (Sections 1, 2, 36; selected subsections of 50/51) stay inline so constrained-context models can follow the framework
- Every skill cross-reference is now a self-contained link to the referenced skill file
- Stale tooling modernized: Pact v2→v3/v4, trufflehog3/safety/detect-secrets→TruffleHog/pip-audit/gitleaks, compose `version:` key removed, mutmut config schema updated, bcrypt→Argon2id, OTel env-var config, pre-commit hook revisions bumped
- Contradictions fixed: duplicate 36.6 heading, 51.1 core-set claim, skill 05 tests/-gitignore conflict, PR-template AI-attribution clash

### Removed
- Audit toolchain from the shipped tree: `tests/` (scratch, gitignored by design), `Dockerfile`, `docker-compose.yml`, `requirements-dev.txt`, `pytest.ini`, `.github/workflows/*`, `.github/dependabot.yml` (never shipped or created without approval)

## [1.0.0] - 2026-06-19

### Added
- Initial 51-section AGENTS.md template
- STARTUP.md bootstrap guide
- All 7 platform-specific AI agent config files
- Research catalog (papers, whitepapers, github analyses)
- `tests/test_agents_md_quality.py` audit script
- MIT license
- README, CONTRIBUTING, SECURITY
