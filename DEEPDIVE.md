# DEEPDIVE.md — Anchor System Narrative

> The story of WHY this template exists and HOW it is organized.
> This is the file an AI agent reads first after AGENTS.md to understand intent.

## System Layout

Anchor is a documentation-only template. It ships rules, not code.

```
standardized-markdown/
├── AGENTS.md                # ⭐ The deliverable — high-level entry point, 53 sections of agent rules
├── skills/                  # Full rule text — 53 skill files (NN-name.md), lazy-loaded by task
├── STARTUP.md               # AI bootstrap guide — phases for greenfield projects
├── README.md                # Public-facing description, stats, quick start
├── CONTRIBUTING.md          # How to add/change sections safely
├── SECURITY.md              # Vulnerability reporting and self-audit
├── LICENSE                  # MIT
│
├── docs/
│   └── AGENT_INSTRUCTIONS.md      # Universal fallback for agents without native config
│
├── research/                # Backing evidence — papers, whitepapers, repo analyses
│   ├── index.md             # Catalog of sources
│   ├── papers/              # AgentBench, CAMEL, MetaGPT, Voyager, HuggingGPT
│   ├── whitepapers/         # Agentic AI best practices
│   └── github/              # AutoGPT, LangChain, Microsoft AI Agents analyses
│
├── .claude/                 # Claude Code & Claude Desktop config
├── .cursor/rules/           # Cursor AI rules
├── .windsurf/               # Windsurf IDE config
├── .continue/               # Continue.dev config
└── .github/copilot-instructions.md  # GitHub Copilot config
```

## Data Flow

There is no runtime data flow. The data flow is **rule distribution**:

1. **Author** writes a section in `AGENTS.md` addressing a specific observed failure mode
2. **Extract** the section's full text into `skills/NN-name.md` (one skill per section)
3. **Audit** (scratch `tests/test_agents_md_quality.py`, run during development, not shipped) verifies section numbering, skill-file completeness, code-block validity, and workflow coverage
4. **Consumer** copies `AGENTS.md` + `skills/` (and platform-specific config) into their own project
5. **AI agent** in the consumer project reads the entry point, loads the skills its task needs, and follows the rules

The template is therefore optimized for two audiences simultaneously: humans who edit it (need clear authorship, no AI-shorthand) and AI agents who consume it (need explicit, actionable, contradiction-free rules).

## Key Decisions

### Why 53 sections, not fewer

Section 51.3 mandates ≤2,000 lines and ≤5,000 tokens for *project-specific* AGENTS.md files, with an explicit exception for this template repository. The template's value is breadth — a single import gives a project access to production-readiness patterns (CI/CD, observability, secrets, mutation testing, chaos engineering) that would otherwise take a team months to assemble.

The template reconciles breadth with constrained context windows by **splitting into an entry point + lazy-loaded skills**:

1. `AGENTS.md` stays lean (~470 lines, ~7K tokens) — a high-level index plus the core rules (Sections 1, 2, 36, 50.1/50.3/50.6, 51) reproduced in full so the non-negotiable guardrails always apply.
2. `skills/NN-name.md` holds each section's full rule text, byte-for-byte identical to the former monolith. Agents load only the skills their current task needs (Section 51.1 trigger-based loading).
3. A 32K-context model can follow all guardrails by loading the entry point plus 7-12 relevant skills (~16-19K tokens total), verified during development by the scratch constrained-context test suite (`tests/`, not shipped).

Consumers trim on import: copy `AGENTS.md` + `skills/`, delete inapplicable skills, inline what remains.

### Why the audit script is Python, not Make/Node

`tests/test_agents_md_quality.py` is pure standard library (re, pathlib, collections). No dependencies to install, no version matrix to maintain. The audit runs in under a second over the entry point plus 53 skill files. Adding pytest as a runtime dep would inflate the install footprint for marginal benefit. It is a **scratch development tool, not a shipped deliverable** — per Section 1, `tests/` is gitignored and does not ship with the template (see "Gotchas" below).

### Why the deployed platform configs are lightweight

Each platform (Cursor, Windsurf, Continue, Copilot, Claude) gets a thin pointer file that says "read AGENTS.md and follow Section N." The 53 sections live in one canonical place (the skills/ library). If we duplicated the rules into each config, drift would be inevitable — any update to AGENTS.md would require manual mirroring to 7 other files. The trade-off: agents on platforms with very small context windows may not load the full rule corpus eagerly. The mitigation is the entry-point index (Section 51.4 model capability awareness): agents read the lean index and load only the skills they need.

### Why AGENTS.md is self-referential (Section 50.8)

The template cannot avoid governing itself — every section is a rule the maintainers must follow, and the structure (entry-point ↔ skill files) enforces it. If the template were exempt, future maintainers would slowly drift away from its own standards. Section 50.8 makes the constraint explicit: editing AGENTS.md requires following every rule in AGENTS.md.

## Gotchas and Landmines

1. **`tests/` is entirely gitignored** — by design (Section 1: tests are scratch). The audit script and all test suites live locally during development but are **not shipped** in the template. A fresh clone has no `tests/` directory — any config or doc that invokes `python3 tests/...` will fail and must be kept out of the repo. The guardrails ship as the entry-point + skills structure itself.

2. **Duplicate section 3.9 in STARTUP.md** — historically had two `### 3.9 Create SECURITY.md` headings, with the first one containing the CONTRIBUTING template by mistake. Any agent following STARTUP literally would have overwritten SECURITY.md. Fixed.

3. **`research/papers/full/`** is an empty directory artifact. Either populate or remove. Kept empty for now pending full paper imports; see TODO.md.

4. **The `snip` shell wrapper** (per the agent's own runtime) prepends to every command. Direct use of `cd`, `export`, `source` will fail. Use `bash -c 'cd ... && ...'` or pass `workdir` to the tool instead. This is not in AGENTS.md because it's a runtime quirk of the agent host, not a project rule.

## Interconnections

- `AGENTS.md` → `STARTUP.md` (bootstrap uses sections 5, 6, 37, 38)
- `AGENTS.md` → `CONTRIBUTING.md` (contribution flow uses sections 33, 34, 35, 50.8)
- `AGENTS.md` → `docs/AGENT_INSTRUCTIONS.md` (universal fallback for unknown agents)
- `AGENTS.md` → `research/index.md` (provenance per section 51.5)
- `AGENTS.md` → all 7 platform config files (single source of truth)
- `AGENTS.md` ↔ `skills/` (entry-point links to every skill; skills hold full rule text)
