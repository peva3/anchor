# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.6.5] - 2026-11-08

### Added
- **Section 76: Security Reconnaissance & Attack Classes.** Section 75 assumed the unit list already existed. Section 76 produces it: a one-page `architecture.md` (principals, protected resources, entry surfaces, trust boundaries, starting paths, known limits), attack-class packs selected by target type rather than language, the high-yield classes scanners miss (state machines, races, numeric manipulation, export/import abuse, search oracles, preview leakage, callback SSRF), one unclassified wildcard unit, and a literal obvious-things pass.
- **Section 77: Security Finding Validation & Reporting.** Candidate validation and record verification are separate. Section 77 adds the fresh-reviewer check of every `file:line`, precondition, and impact; a prior-run state table (same source, changed source, unresolved, rejected, deferred, missing ledger); findings as validated data with three verdict branches and stable fingerprints; reproduction in the target's native interface; and a report structure where zero confirmed findings is a valid, stated result.
- **`audit` task type** — a 21st route for security audit work, owning `security audit`, `attack surface`, `penetration test`, `pentest`, `vulnerability audit`, and `security review`. It loads Sections 75–77 plus the controls, secrets, supply-chain, production, and prompt-injection skills (8 scoped).

### Changed
- **Section 75 now states a quick/deep scope profile, points to Section 76 before building the ledger and to Section 77 before writing the report, and replaces the sandbox sentence with five explicit controls** (no external network, sanitized environment, read-only target, scratch-only writes, resource limits).
- **Security audit triggers moved from `security` to `audit`**, so implementing a control and auditing a codebase resolve to different skill sets.
- **Benchmark coverage** — routing cases now cover 21 task types; the project benchmark has 133 scenarios, including a firmware pen-test that exercises the native attack classes.
- **STARTUP.md section map extended through 77**, so the bootstrap guide matches the index again.

## [2.6.0] - 2026-11-07

### Changed
- **STARTUP.md refreshed to the 75-section layout.** The bootstrap guide had drifted two releases behind: it still advertised 66 sections in twelve places and its "Key AGENTS.md Sections" table stopped at Section 51. All counts now match `AGENTS.md`, and the table covers 52–75 (rule enforcement, MCP guardrails, supply chain, property tests, UI quality, the delivery loop, design systems, and the security audit loop).
- **Starter bundle includes STARTUP.md again.** It was excluded from 2.5.0 because the stale section map would have misled new projects.

### Fixed
- **STARTUP.md no longer tells new projects to gitignore `tests/`.** Sections 8 and 40 require committed tests; the bootstrap advice now says to ignore local scratch, build artifacts, and secrets, and the summary table matches.

## [2.5.0] - 2026-11-07

### Added
- **Section 74: Design Systems & Visual Craft.** Section 63 said what a UI must not fake; nothing said what to build it from or how to judge the rendered result. Section 74 adds surface modes (Persuade / Operate / Read / Experience), tokens as the contract, the inner-radius rule, material inventory (real / pictures / absent), job-led structure with the mirror test, a Hard Floor / Reflex / Finish severity split, a refused-defaults table, copy rules, the rendered-surface ship checklist, `PRODUCT.md` and `DESIGN.md`, and deterministic detection before prose review. Routed with `ui`.
- **Section 75: Security Audit Loop.** Section 13 lists controls; Section 75 is the method that proves which are present. It adds the coverage ledger (entry point × attack class), source-to-sink traces with `file:line` evidence, adversarial validation by a fresh verifier, tri-state verdicts (confirmed / needs validation / rejected), severity as likelihood × impact with hardening notes kept separate, the sandbox gate, and additive re-audits. Routed with `security`.
- **Section 63.7 Design Critique** — critique and audit are separate passes; P0–P3 findings versus ranked observations; the reviewer must have a fresh context and the builder acts on the verdict.
- **Benchmark batch 32** — design-system page, security audit, and design-critique scenarios. The project benchmark now has 132 scenarios.

### Changed
- **Section 50.2 debt sweep** — `# ponytail:` comments are harvested into `TODO.md` at sprint close or retro, with their triggers, so the ledger is reviewed rather than merely greppable.
- **Section 50.6 evidence classes** — claims are tagged `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`, and every report ends with what was not checked.
- **Section 70 review depth** — read the callers of changed public surfaces, sequence Spec before Standards, cite a consequence for every finding, and verify received review points before complying.
- **Section 67 elicitation** — offer 2–4 concrete options per question, state the inferences behind a blanket "go ahead", and play the brief back in short chunks.
- **Section 16 living specs** — `SPEC.md` beside the module, changed in the same commit as the contract, plus a documentation drift check.
- **Section 72 maintenance** — contract changes update `SPEC.md` and the governing ADR in the same commit; a rename is not done until code, tests, glossary, and ADR agree.
- **Section 15.1 parallel agents** — one worktree, one branch, one task per agent; no overlapping files; a recorded green baseline; explicit merge / keep / discard.
- **Section 22.2** — handoff rules now require worktree isolation for parallel agents.
- **Section 51.6** — index-first navigation for large corpora: index → linked page, never re-parse the whole store.
- **Routing** — `ui` gains 74 (and a `screen` trigger); `security` gains 75 (and `security audit` / `attack surface` triggers). `feature` stays at the 8-skill cap, so UI work routes through `ui`.

## [2.4.0] - 2026-11-06

### Added
- **Sections 67–73: the delivery loop the ruleset was missing.** Anchor covered standards well and workflow barely at all — nothing said how to elicit an ambiguous ask, slice an agreed outcome, diagnose a bug that will not reproduce, review a diff against its spec, choose a module boundary, name the domain, or learn from a sprint.
  - **67 Requirements Elicitation (Grilling)** — walk a design tree, ask only frontier questions whose prerequisites are settled, give each question a recommended answer, treat facts as the agent's job and decisions as the user's, and stop only when the frontier is empty and the user confirms alignment
  - **68 Spec & Ticket Decomposition** — a spec shape, vertical tracer-bullet slices sized to one fresh context window and demoable alone, blocking edges, S/M/L/XL sizing, and the expand → migrate → contract exception for wide refactors
  - **69 Bug Diagnosis Loop** — build a loop that goes red on this exact bug before theorising; ten loop types; tighten for speed and determinism; 3–5 falsifiable hypotheses; one variable at a time; regression test at the lowest seam (and if there is no seam, that is the finding)
  - **70 Two-Axis Code Review** — Standards and Spec reviewed independently, each with its own evidence, and no cross-axis reranking. Includes the twelve Fowler smell names as a judgement baseline
  - **71 Codebase Design** — module, interface, implementation, depth, seam, adapter, leverage, locality; the deletion test; one adapter is a hypothetical seam, two make it real
  - **72 Domain Modeling & Glossary** — GLOSSARY.md as the ubiquitous language, invariants and state transitions modeled explicitly, and numbered immutable ADRs that record rejected options
  - **73 Retrospective** — evidence-first retro categories, a severity ladder that prefers a deterministic check over prose, and one change per retro
- **`plan` task type** — elicitation and decomposition now have a route. Twenty task types total. Planning loads 67 as its base, plus 68, 28, 50, 6, 64.
- **Skill frontmatter on every skill file** — `name` and `description` in YAML, so the library is loadable by Claude Code-style skill loaders without a separate manifest. The AGENTS.md index remains the source of truth for descriptions.
- **Benchmark batch 31** — seven scenarios covering spec writing, decomposition, intermittent-bug diagnosis, two-axis review, seam-driven refactoring, domain documentation, and retrospectives. The project benchmark now has 129 scenarios.

### Changed
- **Section 8 now teaches TDD** — the red → green → refactor loop, one vertical slice at a time, seams agreed with the user before writing, and the anti-patterns (implementation-coupled, tautological, horizontal slicing). Refactoring belongs to review.
- **Section 24.11 is now a pointer** — the short diagnosis advice delegates to the full Section 69 loop instead of duplicating it.
- **Section 35.5 Merge Danger** — reversibility (one-way vs two-way door), blast radius, approval, rollback, evidence, canary, and a post-deploy check. Do not bundle a risky change with cleanup.
- **Section 56.6 The Handoff Artifact** — a fixed Goal / State / Decisions / Facts / Constraints / Next-action template for long sessions.
- **Section 51.6 Writing for Agents** — context pointer, context load vs cognitive load, information hierarchy, co-location, completion criteria as clarity plus demand, leading words, positive phrasing, and the no-op test. Negation is a failure mode.
- **Section 64.1** — the task-type list is current, and the cap is 8 task-scoped skills, matching what `routing.json` enforces.
- **Routing budget recalibrated** — each skill costs roughly 1,800 tokens, so 8 slots plus the ~6,000-token entry point lands near 20,000 tokens (~63% of a 32K window). The plan phase now adds only Section 50; Section 28 is dropped at build instead of lingering.

### Fixed
- **Section 64 claimed a 7-skill cap while the router enforced 8** — one number now, in both places.
- **README statistics** — section count, skill-file count, entry-point size, Python-block count, and the validation section all match what the scripts actually check.

## [2.3.0] - 2026-10-21

### Added
- **Round 6 benchmark: 20 fresh domains (122 scenarios total)** — returns portal, restaurant reservations, fitness tracking, inventory forecasting, helpdesk sync, two-way calendar sync, invoice PDFs, nightly scraping, recommendations, call transcription, multi-tenant billing, admin dashboards, search relevance, notification preferences, audit trails, data anonymization, API gateway, push campaigns, localization QA, accessibility statements
- **Substance rules the round exposed**: money is never a float (integer minor units or `Decimal`, explicit rounding, test the rounding cases); store instants in UTC and convert at the edge, with DST-aware scheduling; two-way sync needs an explicit **conflict resolution** rule rather than retries alone; crawlers must honour `robots.txt`, terms, and a real rate limit; **multi-tenant scoping is a data-layer rule** taken from the session, with a cross-tenant access test; audit records need retention and tamper evidence; an empty state is a state, not a blank panel

### Fixed
- **Vocabulary, round two** — reservations/bookings/availability, invoices and PDF generation, notification preferences → `feature`; fitness/workout/tracker, admin and internal dashboards, onboarding → `ui`; forecast/demand/inventory, relevance/ranking, anonymization, data quality → `data`; transcription, recommendations, personalization, audio → `ai`; calendar sync, helpdesk, scrapers, gateways → `integration`; audit trail, tenant isolation, JWT validation → `security`; ingress/reverse proxy/nginx → `infra`; accessibility statement → `docs`
- **Over-broad triggers pruned again**: `settings page` and `profile page` were stealing WordPress plugin work from `feature`; `summarize` sent a confidential-document request to `ai`; singular `notification` pulled mobile push work out of `ui`
- **`feature` now loads code quality instead of project structure** (money, time, tenant rules), and `refactor` picked up project structure so section 5 stays reachable

### Added
- **Vocabulary harvest across all 19 task types** — the routing map grew from 277 to 533 triggers in one pass instead of discovering words one scenario at a time, covering the phrasing people actually use for debugging, integration, data, security, AI, infrastructure, CLI and device work
- **Section 64.9 (keep the vocabulary honest)** — one owner per trigger, phrases over abstract nouns, weak verbs never outrank a domain noun, a fallback is a reported gap, and generic words that fit every domain own none of them
- **Vocabulary suite and map hygiene checks** — trigger ownership, minimum vocabulary per type, and normalized form are now validated, so a future edit cannot quietly create two owners for one word

### Changed
- **Bulk vocabulary measurement** — a 97-phrase suite scored **43/97 before the harvest and 97/97 after** (35 fallbacks eliminated), while the 102-scenario project benchmark stayed green

### Fixed
- **Four over-broad triggers pruned** — `button`, `command`, `retry` and `rewrite` were pulling unrelated work into the wrong type; `mutation` alone meant GraphQL in one context and mutation testing in another, so it became `mutation testing`

### Added
- **Benchmark round five (100 new scenarios → 102 total)** — project scopes drawn from what people actually point coding agents at: object-storage uploads, transactional email, background queues, WebSockets, error tracking, product analytics, slow-query and index work, full-text search, OAuth and RBAC, dark mode, sortable data tables, GitHub Actions authoring, npm publishing, monorepos, and one-command local dev environments
- **`integration` task type** — connecting to anything outside the process boundary (S3, SES, queues, webhooks, WebSockets) now loads Section 20 as its base skill. Previously Section 20 was reachable only from `embedded`, so timeouts, backoff, idempotency keys, webhook signatures and SSRF guidance were unavailable for the most common integration work
- **End-to-end testing guidance in Section 8** — real browser drivers (Playwright/Cypress), flow-level selectors, keeping the E2E suite small, seeded data, and failure artifacts. Browser E2E had no coverage anywhere

### Fixed
- **Trigger coverage for common asks** — email, queues, uploads, WebSockets, explain-this-codebase, dead-code removal, error tracking, analytics events, query/index tuning, full-text search, OAuth, dark mode, data tables, GitHub Actions and monorepos all previously fell through to a generic route or the wrong one
- **Whitespace in requests broke phrase triggers** — "how  does" (double space) silently rerouted to a different task type; matching now normalises whitespace, which the 408-variant stability check caught
- Contract testing moved to `integration` (it is an interface concern) so `test` can carry the testing-requirements skill

### Added
- **A/B harness: Anchor-guided vs rule-free output** (local, `tests/ab_bench.py`). One project timeline of six tasks — feature, test, fix, ui, security, release — is run through two arms: the entry point plus the routed skills, and a generic "helpful coding assistant" with no rules. Each answer is scored against a task rubric. Drivers are pluggable: `stub` (context-echo proxy for pipeline checks), `emit` (writes exact per-arm prompts), and `files` (scores real recorded answers, e.g. from subagents). First recorded run: **Anchor 10/10 rubric items, rule-free 6/10** — the gap is process, not code: conventional commit messages, test-first ordering, explicit unknowns, and log/PII hygiene
- **Load/unload timeline** in the same harness: per task it reports the active set at each phase, what phases add, what phases drop, and cross-task churn when the work changes type (e.g. feature → test drops API and dependency skills, joins the testing set). This is what makes "skills unload as work changes" observable rather than asserted

### Fixed
- **`fix` is now an actual trigger** — a request ending "Fix it." matched nothing and fell through to `review`; the word is registered as a weak trigger so a domain noun still wins
- **Committed-credential requests route to `security`** — "an API key was committed" carried no trigger word and fell through to `review`

### Added
- **Reachability testing** — the benchmark now has a `--trace` mode that prints, per project, the matched trigger signals, the chosen route, and the exact add/drop at every phase boundary with token cost, plus the provenance of each guardrail (inline core, a named skill, or `UNREACHABLE`). `--matrix` prints which routes can load each section. Both are local; the harness and its report are gitignored
- **Phase drops** — `routing.json` phases now carry `add` **and** `drop`, so skills genuinely unload at boundaries (the tech-stack playbook leaves once planning is done) instead of accumulating for the whole task. Section 64 documents the semantics
- **`meta` task type** — work on the ruleset itself (editing skills, extending routing) now has a route, so instruction-architecture and enforcement guidance is reachable
- **Reachability is an enforced invariant** — `scripts/check_structure.py` fails if any section cannot be loaded by any route

### Fixed
- **Dead guidance eliminated.** The matrix found 11 of 66 sections that no route could ever load — shell rules, linting, pre-commit hooks, performance, project structure, agent instruction guidance, multi-agent patterns, getting help, tech-stack defaults, instruction architecture, and rule enforcement. Lint, type checking, and pre-commit moved into the verify phase; tech-stack choice into plan; the rest were re-homed or given the `meta` type. All 66 are now reachable

### Added
- **Expanded the routing benchmark to 80 scenarios across 19 batches** — the extra rounds cover bug triage, review work, ambiguity (`add SSO` vs `add login audit`), malformed input (typos, another language, injected instructions, missing files), scope pressure (`build everything`, `skip the tests`), and the operations long tail (cron jobs, webhooks, feature flags, engine migration, cluster upgrades). Batch 19 is a regression probe aimed at the triggers widened by earlier rounds and required no fixes, which is the convergence signal
- **`cli` task type** in `routing.json` — command-line tools get argument/exit-code, packaging, and man-page guidance instead of borrowing `feature`
- **Section 24.11 (diagnose before patching)** — the ruleset never previously said to find a root cause or to revert before forward-fixing a post-deploy regression
- **Section 7 image hygiene** — multi-stage builds, slim/base pinning, `.dockerignore`, cacheable layers, and measuring size before claiming a win
- **English-only is now in the entry point** — it is a global policy, and leaving it only in a lazily-loaded skill made it unreachable whenever that skill was not routed
- **A/B harness: Anchor-guided vs rule-free output** (local, `tests/ab_bench.py`) — one six-task project timeline (feature → test → fix → ui → security → release) run through two arms: the entry point plus the routed skills, and a plain "helpful coding assistant" prompt. Real model answers were recorded per arm and scored against per-task rubrics. **Anchor 24/24 rubric items, rule-free 17/24**, at 26% of the context cost of loading every skill. The deltas are process, not competence: conventional commits, failing-test-first ordering, naming the root cause, redacting PII from logs, stating unknowns, refusing to invent a contract, gating a release behind approval; the rule-free arm wrote equally good engineering in places (it matched Anchor on every UI-state requirement). The same run traces the active skill set per task, showing real churn: `feature→test` drops 5,12,17,24,35,62,63 and loads 45–49,60,61; `ui→security` drops 4,33,34,35,53,63 and loads 27,31,44,55,58; each task also drops section 28 at the build boundary
- **`embedded` task type** in `routing.json` — firmware, microcontrollers, MQTT/IoT and OTA get device constraints, OTA practice, connectivity retries, health endpoints, and observability instead of being spread across `infra`

### Fixed
- **"without review" no longer routes to `review`** — bare `review` matched negations; the trigger now requires a deliberate review phrase
- **`feature` was blind to hallucinated packages** — it now loads dependency management and failure modes (coverage arrives at the verify phase)
- **Chaos experiments route to `test`, Dockerfile work stays in `infra`** — the two needs were competing for the same budget slots
- **Release work loads incident basics** for rollback and revert-after-bad-release
- **Generic verbs no longer outrank domain nouns.** "Implement an auth service" routed to `feature` because "implement" is longer than "auth"; `weakTriggers` in `routing.json` now marks add/build/implement/feature/support-for as weak so a domain noun wins
- **Trigger matching is whole-word.** Substring matching sent "build" to the `ui` type (b**ui**ld); triggers now match on word boundaries
- **The active-skill budget counts task skills only** — the always-loaded core and the routing skill itself no longer consume the 7-slot budget, which previously made several task types look over-budget
- **Coverage gaps found by the benchmark**: `ui` now loads security for permission-scoped surfaces, `data` loads config validation and property testing, `infra` swaps build docs for benchmark methodology, `feature` swaps testing (supplied at verify) for UI quality, `security` swaps the niche MCP skill for password hashing, `ai` swaps SBOM for agent failure modes
- **Skill drift**: Section 50 was missing the three honesty rules that only existed inline in the entry point (no superlatives without evidence, name the model, say "unknown")
- **Skill 13** gained least-privilege, output-encoding, no-dynamic-code, and SSRF guidance; **skill 54** gained least-privilege credentials for database-exposing MCP servers
- `tests/routing-benchmark.json` regenerated against the updated map and extended to the `embedded` type

### Fixed
- **Core and skill copies could drift apart** — sections 1, 2, 36, 50.6, 51.3 and 64 exist both inline and as skills, and nothing compared them. The structure check now fails when the entry point states a rule its skill lacks (70% word-overlap tolerance for rewording), and it immediately found real drift: 36.10 was missing from the skill entirely, 36.2 lost its branch-policy rules, 36.4a lost three approval rules, and 51.3 still carried a pre-rebrand exception paragraph that claimed a different project name
- **A fallback was silent** — an unmatched request quietly became `review`. Section 64.6 now requires reporting the fallback, asking which area the work belongs to, and recording the phrase as a vocabulary gap
- **Two harvested triggers were stealing work** — `endpoint`/`endpoints` from `feature` and bare `query`/`queries` from `data`; both pruned, with the specific phrases (`slow query`, `query tuning`, `index tuning`) kept

### Changed
- **Active-skill budget raised 7 → 8** and the **commit phase now drops the domain corpus**: a commit is a write-up, not a build. Commit-time context fell from ~27.6K tokens (86% of a 32K window) to ~14.0K (44%), which pays for the extra slot (each skill costs ~955 tokens)
- The A/B evaluator checks artifacts rather than words: python blocks must parse, code-producing task types must include runnable test code, outputs may not contain credentials, and commits must use a conventional prefix; it also supports n>=3 samples per task
## [2.2.0] - 2026-08-21

### Added
- **Section 64 — Skill Routing & Checkpoints**: classify the task at start, load only the matching skills, re-check at plan→build→verify→commit boundaries, state a one-line `ROUTE:` checkpoint naming active/dropped/added skills, cap active skills, follow cross-references instead of guessing, and take the safer route when ambiguous
- **`routing.json`** — a declarative, logic-free map of task type → trigger phrases → skills, plus an always-loaded core set and per-phase additions, so the same request always resolves to the same skills. `AGENTS.md` and `routing.json` are a pair: the entry point states the guardrails and requires the map to be read on every task, and the map decides which of those guardrails the task loads. Routing is never improvised from memory, and a missing map is a stop condition rather than a fallback
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
