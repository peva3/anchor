# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0] - 2026-08-21

### Added
- **Section 64 — Skill Routing & Checkpoints**: classify the task at start, load only the matching skills, re-check at plan→build→verify→commit boundaries, state a one-line `ROUTE:` checkpoint naming active/dropped/added skills, cap active skills, follow cross-references instead of guessing, and take the safer route when ambiguous
- **`routing.json`** — a declarative, logic-free map of task type → trigger phrases → skills, plus an always-loaded core set and per-phase additions, so the same request always resolves to the same skills
- **Section 65 — Time-Boxed Delivery Mode**: the demo path keeps full rigor, every shortcut carries a `# HACKATHON:` marker that greps into a cleanup list, and the bright-line rules never relax
- **Section 66 — Presentation Decks**: one idea per slide, readable type, speaker notes, accessible contrast, honest labeling of illustrative numbers, and an optional deck-as-code approach with design tokens, a grid, a type scale, and a render-and-inspect loop
- **Section 36.10 — Sensitive-Data Hard Stop** (always loaded): check headers and paths for confidentiality markings and personal identifiers before printing, copying, summarizing, or importing; a "synthetic" label never overrides a marking; stop and ask who owns the data
- **`PROJECT.md`** documented as the per-project identity file (gitignored here — every consumer writes their own)
- **`docs/SKILL_MAP.md`** — a generated, human-readable overview of the routing map, the always-loaded core, the phase additions, and every task type
- **Guarded pre-commit hooks** — link resolution plus JSON validity, and a full structural check (sections, index, routing map). Both hooks skip cleanly when `scripts/` is absent, so a fresh clone never fails on tooling it does not have

### Changed
- `AGENTS.md` slimmed from 513 to ~407 lines (~7,913 → ~6,057 tokens): the Section Index and Skills Directory merged into one routing-and-glossary index, the Quick-Navigation Cheatsheet removed as a duplicate routing source, optional subsections reduced to pointers, and the section 51.3 budget exception restated with measured numbers
- Branch policy split into solo vs shared cases: shared/team repos always branch and review, solo repos may commit and push directly to `main`, an experiments-only branch doesn't make a repo shared, and "private" doesn't mean "solo" (36.2, plus skills 02 and 15 and `.ruler/rules/02`)
- Approval discipline tightened: a general request is never file-level approval, second-hand approval doesn't count, and secrets are never placed in example files even when asked for convenience
- Honesty boundaries extended: no superlative claims without measurement, always name the model/provider/version behind a result, always say "unknown" when evidence is missing
- AI/agentic guidance (53.6) now requires evidence-first answers — citations with provenance, "unknown" when retrieval is weak, an eval set before claiming improvement, and redacted prompt/output logging
- UI guardrails (63.4) now require respecting `prefers-reduced-motion`
- Project structure tree documents `PROJECT.md`; docs updated from 63 to 66 sections

### Fixed
- `SECURITY.md` no longer describes removed tooling (regex prompt-injection detection, `safety`, auto-issue creation, detect-secrets) and now covers Sections 54, 55, and 58
- `README.md` badge and stats table reported 51 sections and a stale entry-point size; now 66 sections and the measured ~407 lines / ~6,000 tokens
- `TODO.md` items that contradicted the no-GitHub-automation policy, the already-shipped release, and Sections 16–20 being merged
- `DEEPDIVE.md` claimed a shipped validator script that no longer exists and presented a harness-specific `snip` shell quirk as a current rule
- Removed the change log from `AGENTS.md` — history lives only in this file

### Removed
- `pytest.ini` from git tracking (it is local development configuration, ignored like `tests/` and `scripts/`)

## [2.1.0] - 2026-08-20

### Added
- **Section 63** — UI Quality & Anti-Slop Guardrails: no fabricated content/placeholders, no dead controls, required empty/loading/error states, WCAG AA accessibility minimums, and the ENERGY/RHYTHM/MOTION dials mechanism for enforceable visual liveliness (adapted from the universal engineering subset of https://github.com/miqdadbadjuber/anti-slop). Brings the library to 63 sections.

### Changed
- AGENTS.md entry-point (Section Index, Skills Directory, Quick-Navigation Cheatsheet) and all docs updated from 62 to 63 sections

### Fixed
- Broken references to the deleted `scripts/check_structure.sh` in README, CONTRIBUTING, and DEEPDIVE (structural validation is now a documented manual check: 63 index rows, every link resolves to a file in skills/)

### Removed
- `scripts/` (structural validator) — removed from the tree, gitignored, and purged from git history

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
