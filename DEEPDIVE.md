# DEEPDIVE.md — Anchor System Narrative

> The story of WHY this template exists and HOW it is organized.
> This is the file an AI agent reads first after AGENTS.md to understand intent.

## System Layout

Anchor is a documentation-only template. It ships rules, not code.

```
anchor/
├── AGENTS.md                # ⭐ The deliverable — high-level entry point, 77 sections of agent rules
├── skills/                  # Full rule text — 77 skill files (NN-name.md), lazy-loaded by task
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
3. **Validate** — `scripts/check_structure.py` verifies the Section Index has 77 rows, every link resolves to a file in `skills/`, headings are unique, every task type references existing skills, every section is reachable by some route, and `tests/routing-benchmark.json` matches `routing.json`; `scripts/check_links.py` catches broken links. Both are local development tooling (gitignored, like `tests/`)
4. **Consumer** copies `AGENTS.md` + `skills/` (and platform-specific config) into their own project
5. **AI agent** in the consumer project reads the entry point, loads the skills its task needs, and follows the rules

The template is therefore optimized for two audiences simultaneously: humans who edit it (need clear authorship, no AI-shorthand) and AI agents who consume it (need explicit, actionable, contradiction-free rules).

## Key Decisions

### Why 77 sections, not fewer

Section 51.3 mandates ≤2,000 lines and ≤5,000 tokens for *project-specific* AGENTS.md files, with an explicit exception for this template repository. The template's value is breadth — a single import gives a project access to production-readiness patterns (CI/CD, observability, secrets, mutation testing, chaos engineering) that would otherwise take a team months to assemble.

The template reconciles breadth with constrained context windows by **splitting into an entry point + lazy-loaded skills**:

1. `AGENTS.md` stays lean (~419 lines, ~6,600 tokens, measured) — a single Section Index (routing + glossary in one) plus the core rules (Sections 1, 2, 36, 50.1/50.6, 51.3) reproduced in full, because a hard stop that only applies when a skill happens to be loaded is not a hard stop.
2. `skills/NN-name.md` holds each section's full rule text, byte-for-byte identical to the former monolith. Agents load only the skills their current task needs (Section 51.1 trigger-based loading).
3. A 32K-context model can follow all guardrails by loading the entry point plus the routed skills (~20K tokens at the 8-skill budget, about 63% of the window). The budget is enforced by `tests/bench_projects.py`; `routing.json` records the per-skill cost estimate.

Consumers trim on import: copy `AGENTS.md` + `skills/`, delete inapplicable skills, inline what remains.

### Why the delivery loop was added (Sections 67-73)

The first 66 sections are standards-shaped: they say what good code, tests, releases, and operations look like. They did not describe the work that produces those artifacts. An agent could follow every rule and still start building on a guess, slice work horizontally, theorise at a bug instead of reproducing it, review a diff without its spec, or repeat the same correction next sprint.

Sections 67-73 close that loop: elicit the requirement (67), decompose it into vertical slices (68), diagnose failures by building a red-capable loop first (69), review against Standards and Spec independently (70), choose module boundaries with a shared vocabulary (71), name the domain and record decisions (72), and run a retrospective that ends in exactly one change (73). `routing.json` gained a `plan` task type so elicitation and decomposition load before implementation skills, and `feature` now loads Section 67 as a base skill because most feature work starts with an ambiguous ask.

### Why design and audit were added (Sections 74-75)

Sections 67-73 covered the delivery loop, but two areas were still thin in a way that mattered:

- **Design.** Section 63 enforced honesty and accessibility but never said what to build the interface from. Agents could satisfy every guardrail and still produce the same generic card grid. Section 74 supplies the missing system layer: the surface mode, tokens as the contract, the material inventory, job-led structure, a Hard Floor / Reflex / Finish severity split, and a refused-defaults list. Section 63.7 adds the judgement pass that a checklist cannot provide.
- **Security auditing.** Section 13 lists the controls to write, but no section described how to establish coverage or how confident a finding is. Section 75 adds the coverage ledger, source-to-sink evidence, adversarial validation, and tri-state verdicts, so "no findings" becomes a claim with a scope instead of a guess.

Routed where the work starts: `ui` loads 74; `audit` loads 75-77; `security` keeps the implementation controls. `feature` stays at the 8-skill cap, so UI work routes through `ui` rather than stretching every feature load.

### Why security became two more sections (Sections 76-77)

Section 75 covered the loop but assumed two things it never produced: a unit list and a trustworthy record. Growing it further would have made one file carry reconnaissance, testing, validation, and reporting — four different jobs with different failure modes. The split keeps each file precise:

- **76 — reconnaissance and attack classes**: the `architecture.md` map, target-type class packs, the high-yield classes scanners miss, a wildcard unit, and the obvious-things pass. It answers "what should we even test?"
- **77 — validation and reporting**: independent record verification, prior-run state handling, findings as validated data, native-interface reproduction, and the report's honesty rules. It answers "is this true, and can someone act on it?"

The new `audit` task type owns the audit triggers (`security audit`, `attack surface`, `penetration test`, `pentest`, `vulnerability audit`, `security review`) and loads 75-77 plus the controls, secrets, supply-chain, production, and prompt-injection skills — exactly 8 scoped, so the budget holds. `security` now covers implementing a control; `audit` covers proving which controls hold.

### Why validation tooling is local, not shipped

Nothing structural ships as a script — `scripts/` and `tests/` are gitignored (see "Gotchas"). The **structural invariant** is still enforced, by local tooling: `scripts/check_structure.py` checks index ↔ skill parity, unique headings, routing integrity and reachability, core drift, and benchmark alignment; `scripts/check_links.py` checks links; `tests/bench_projects.py` routes 133 project scenarios through the map and asserts budget, reachability, decoys, and phase adds/drops. A fresh clone has none of them, so a contributor without the local tooling verifies manually: the Section Index has 77 rows, every link resolves, and every skill referenced by `routing.json` exists. The pre-commit hook skips these checks when the scripts are absent rather than failing on a missing file.

### Why the deployed platform configs are lightweight

Each platform (Cursor, Windsurf, Continue, Copilot, Claude) gets a thin pointer file that says "read AGENTS.md and follow Section N." The 77 sections live in one canonical place (the skills/ library). If we duplicated the rules into each config, drift would be inevitable — any update to AGENTS.md would require manual mirroring to 7 other files. The trade-off: agents on platforms with very small context windows may not load the full rule corpus eagerly. The mitigation is the entry-point index (Section 51.4 model capability awareness): agents read the lean index and load only the skills they need.

### Why AGENTS.md is self-referential (Section 50.8)

The template cannot avoid governing itself — every section is a rule the maintainers must follow, and the structure (entry-point ↔ skill files) enforces it. If the template were exempt, future maintainers would slowly drift away from its own standards. Section 50.8 makes the constraint explicit: editing AGENTS.md requires following every rule in AGENTS.md.

## Gotchas and Landmines

1. **`tests/` and `scripts/` are gitignored** — by design (Section 1: tests are scratch; the structural scripts are local development tooling). The benchmark suites, routing benchmark, audit scripts, and link checker live locally during development but are **not shipped**. A fresh clone has neither directory — any config or doc that invokes `python3 tests/...` or `python3 scripts/...` must tolerate their absence; the pre-commit hook does. Contributors without the tooling verify the structural invariant manually (Section Index has 77 rows, every link resolves).

2. **Duplicate section 3.9 in STARTUP.md** — historically had two `### 3.9 Create SECURITY.md` headings, with the first one containing the CONTRIBUTING template by mistake. Any agent following STARTUP literally would have overwritten SECURITY.md. Fixed.

3. **`research/papers/full/` is not empty** — it holds the full text of the cited papers (AgentBench, CAMEL, and others), with `agentbench.md` as a shorter excerpt. Earlier notes calling it an empty artifact were wrong; the catalog is `research/index.md`.

4. **Historical note (no longer applicable):** an earlier agent host wrapped every command in a `snip` shim that broke `cd`/`export`/`source`. That host is gone; current harnesses run shell commands directly and support a `workdir` parameter. The gotcha is recorded only so future maintainers recognize old references to it.

## Interconnections

- `AGENTS.md` → `STARTUP.md` (bootstrap uses sections 5, 6, 37, 38)
- `AGENTS.md` → `CONTRIBUTING.md` (contribution flow uses sections 33, 34, 35, 50.8)
- `AGENTS.md` → `docs/AGENT_INSTRUCTIONS.md` (universal fallback for unknown agents)
- `AGENTS.md` → `research/index.md` (provenance per section 51.5)
- `AGENTS.md` → all 7 platform config files (single source of truth)
- `AGENTS.md` ↔ `skills/` (entry-point links to every skill; skills hold full rule text)
- `AGENTS.md` → `routing.json` (the deterministic task-type → skill map; Section 64 protocol)
- `AGENTS.md` → `PROJECT.md` (per-project identity; gitignored, each consumer writes its own)
- `tests/routing-benchmark.json` → `routing.json` (local, gitignored benchmark of routing quality)
- `docs/SKILL_MAP.md` → `routing.json` (generated human-readable view of the map; the JSON wins on conflict)
