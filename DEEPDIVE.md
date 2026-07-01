# DEEPDIVE.md — Anchor System Narrative

> The story of WHY this template exists and HOW it is organized.
> This is the file an AI agent reads first after AGENTS.md to understand intent.

## System Layout

Anchor is a documentation-only template. It ships rules, not code.

```
standardized-markdown/
├── AGENTS.md                # ⭐ The deliverable — 51 sections of agent rules
├── STARTUP.md               # AI bootstrap guide — phases for greenfield projects
├── README.md                # Public-facing description, stats, quick start
├── CONTRIBUTING.md          # How to add/change sections safely
├── SECURITY.md              # Vulnerability reporting and self-audit
├── LICENSE                  # MIT
│
├── tests/
│   └── test_agents_md_quality.py  # Structural audit (parses AGENTS.md, asserts)
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
2. **Audit** (`tests/test_agents_md_quality.py`) verifies section numbering, code-block validity, and workflow coverage
3. **Consumer** copies `AGENTS.md` (and platform-specific config) into their own project
4. **AI agent** in the consumer project reads `AGENTS.md` and follows it

The template is therefore optimized for two audiences simultaneously: humans who edit it (need clear authorship, no AI-shorthand) and AI agents who consume it (need explicit, actionable, contradiction-free rules).

## Key Decisions

### Why 51 sections, not fewer

Section 51.3 mandates ≤2,000 lines and ≤5,000 tokens for *project-specific* AGENTS.md files, with an explicit exception for this template repository. We exceed those limits because the value of the template is breadth — a single import gives a project access to production-readiness patterns (CI/CD, observability, secrets, mutation testing, chaos engineering) that would otherwise take a team months to assemble. The exception clause exists in 51.3 precisely so this template can serve as the reference; consumers trim on import.

### Why the audit script is Python, not Make/Node

`tests/test_agents_md_quality.py` is pure standard library (re, pathlib, collections). No dependencies to install, no version matrix to maintain. The audit runs in 0.2s on a 195KB file. Adding pytest as a runtime dep would inflate the install footprint for marginal benefit — a one-liner `python3 tests/test_agents_md_quality.py` is the contract.

### Why the deployed platform configs are lightweight

Each platform (Cursor, Windsurf, Continue, Copilot, Claude) gets a thin pointer file that says "read AGENTS.md and follow Section N." The 51 sections live in one place. If we duplicated the rules into each config, drift would be inevitable — any update to AGENTS.md would require manual mirroring to 7 other files. The trade-off: agents on platforms with very small context windows may not load AGENTS.md eagerly. Section 51.4 (model capability awareness) is the mitigation: copy only the sections you need if you cannot fit AGENTS.md.

### Why AGENTS.md is self-referential (Section 50.8)

The template cannot avoid governing itself — every section is a rule the maintainers must follow, and the audit script enforces it. If the template were exempt, future maintainers would slowly drift away from its own standards. Section 50.8 makes the constraint explicit: editing AGENTS.md requires following every rule in AGENTS.md.

## Gotchas and Landmines

1. **`tests/` in `.gitignore`** — earlier drafts of `.gitignore` ignored the entire `tests/` folder. This hid the audit script from fresh clones, defeating the purpose. The fix: only `tests/scripts/` (random tooling) and `.test-cache/` are ignored. The audit must travel with the repo.

2. **Duplicate section 3.9 in STARTUP.md** — historically had two `### 3.9 Create SECURITY.md` headings, with the first one containing the CONTRIBUTING template by mistake. Any agent following STARTUP literally would have overwritten SECURITY.md. Fixed.

3. **`research/papers/full/`** is an empty directory artifact. Either populate or remove. Kept empty for now pending full paper imports; see TODO.md.

4. **The `snip` shell wrapper** (per the agent's own runtime) prepends to every command. Direct use of `cd`, `export`, `source` will fail. Use `bash -c 'cd ... && ...'` or pass `workdir` to the tool instead. This is not in AGENTS.md because it's a runtime quirk of the agent host, not a project rule.

## Interconnections

- `AGENTS.md` → `tests/test_agents_md_quality.py` (audit target)
- `AGENTS.md` → `STARTUP.md` (bootstrap uses sections 5, 6, 37, 38)
- `AGENTS.md` → `CONTRIBUTING.md` (contribution flow uses sections 33, 34, 35, 50.8)
- `AGENTS.md` → `docs/AGENT_INSTRUCTIONS.md` (universal fallback for unknown agents)
- `AGENTS.md` → `research/index.md` (provenance per section 51.5)
- `AGENTS.md` → all 7 platform config files (single source of truth)
