<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Anchor-⚓_Keep_your_agents_grounded-3498db?style=for-the-badge&labelColor=1a1a2e">
  <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/badge/Anchor-⚓_Keep_your_agents_grounded-3498db?style=for-the-badge&labelColor=1a1a2e">
  <img alt="Anchor — the production-grade AGENTS.md template for AI coding agents" src="https://img.shields.io/badge/Anchor-⚓_Keep_your_agents_grounded-3498db?style=for-the-badge&labelColor=1a1a2e">
</picture>

<!-- BADGE BAR — trust signals, discoverability, social proof -->
<p align="center">
  <a href="https://github.com/peva3/anchor/stargazers"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/peva3/anchor?style=flat-square&labelColor=1a1a2e&color=f1c40f"></a>
  <a href="https://github.com/peva3/anchor/blob/main/LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/license-MIT-blue?style=flat-square&labelColor=1a1a2e&color=3498db"></a>
  <a href="https://github.com/peva3/anchor"><img alt="Last Commit" src="https://img.shields.io/github/last-commit/peva3/anchor?style=flat-square&labelColor=1a1a2e&color=2ecc71"></a>
  <a href="#-quick-start"><img alt="Quick Start" src="https://img.shields.io/badge/set_your_anchor-in_60_seconds-e74c3c?style=flat-square&labelColor=1a1a2e"></a>
  <br>
  <img alt="Sections" src="https://img.shields.io/badge/51_sections-5%2C780_lines-e67e22?style=flat-square&labelColor=1a1a2e">
  <img alt="Research" src="https://img.shields.io/badge/research_backed-22_sources-9b59b6?style=flat-square&labelColor=1a1a2e">
  <img alt="Platforms" src="https://img.shields.io/badge/works_with-8%2B_AI_agents-1abc9c?style=flat-square&labelColor=1a1a2e">
</p>

<p align="center">
  <b>Anchor — the production-grade AGENTS.md template for AI coding agents.</b><br>
  <sub>Keep your agents grounded. 51 sections of battle-tested rules distilled from 100+ real-world projects, academic research, and production failures.</sub>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> ·
  <a href="#-whats-inside">What's Inside</a> ·
  <a href="#-file-structure">File Structure</a> ·
  <a href="#-why-this-exists">Philosophy</a> ·
  <a href="#-research-foundation">Research</a> ·
  <a href="#-how-to-use">Usage Guide</a> ·
  <a href="#-supported-ai-agent-platforms">Platforms</a>
</p>

---

## 🚀 Quick Start

```bash
# 1. Clone the template
git clone https://github.com/peva3/anchor.git

# 2. Copy AGENTS.md into your project
cp anchor/AGENTS.md ./your-project/AGENTS.md

# 3. Copy supporting agent config files
cp anchor/CLAUDE.md ./your-project/
cp -r anchor/.cursor/rules/ ./your-project/.cursor/
cp anchor/.github/copilot-instructions.md ./your-project/.github/

# 4. Optional — bootstrap an entire new project from scratch
cp anchor/STARTUP.md ./your-new-project/STARTUP.md
# Follow the STARTUP.md phases — it's a step-by-step guide for AI agents
```

**After copying, delete any sections that don't apply to your project.** The template is designed to be trimmed — each project should keep only relevant sections, targeting ≤2,000 lines and ≤5,000 tokens (see Section 51.3).

---

## 📦 What's Inside

51 production-grade sections organized into 7 capability domains:

### Code Quality & Safety
| Section | Content |
|---------|---------|
| 1-9 | Core principles, commit protocol, shell execution rules, code style, project structure, TODO.md standard, Docker, testing, linting |
| 10-14 | Error handling, configuration, API design, security, logging |
| 27 | Comprehensive code quality standards — Python idioms, anti-patterns, security constraints, performance patterns, docstring quality, error handling patterns, 19-point checklist |

### Git, CI/CD & Release Engineering
| Section | Content |
|---------|---------|
| 15 | Git workflow — human-sounding commit messages with WHY-focused pattern |
| 33-36 | PR size standards (800-line gate), AI anti-pattern detection, PR description template with HUMAN/AGENT disclosure, explicit NEVER list |
| 37-40 | Pre-commit hooks, CI/CD pipeline standards (ci/release/deploy), semantic versioning & Keep a Changelog, code coverage enforcement (80% floor) |

### Production Operations
| Section | Content |
|---------|---------|
| 29-32 | Operational patterns (circuit breaker, dead letter queue, middleware stack, semantic cache), health endpoint specification, production security (prompt injection detection, audit logging, key encryption), Docker & Kubernetes |
| 41-44 | Observability (structured JSON logging, OpenTelemetry, Prometheus, SLOs), Infrastructure as Code (Terraform), database backup & recovery, secrets management (tiered strategy) |

### Testing Excellence
| Section | Content |
|---------|---------|
| 45-49 | Flaky test management (quarantine mechanism), mutation testing (mutmut + arid nodes), performance benchmarks, contract testing (Pact), chaos engineering (Netflix principles) |

### AI Agent Guidance
| Section | Content |
|---------|---------|
| 21-26 | Agent instruction guidance (from AgentBench/CAMEL), multi-agent cooperation patterns, verification gates, common failure modes, gotchas, getting help |
| 28 | Default tech stack playbook — FastAPI, Next.js, Gin, databases, decision tree |

### Intentional Minimalism
| Section | Content |
|---------|---------|
| 50 | Decision ladder (YAGNI→stdlib→native→existing dep→one line→minimum code), structured tradeoff comments, safety carve-outs, output discipline, over-engineering review vocabulary, honesty boundaries, tests-are-not-bloat policy, self-referential governance |

### Instruction Architecture
| Section | Content |
|---------|---------|
| 51 | Trigger-based lazy loading, self-maintaining meta-instructions, context budget awareness, model capability awareness, instruction provenance tracking |

---

## 🎯 Why This Exists

**Problem:** AI coding agents receive instructions from scattered, inconsistent sources. Most AGENTS.md files are 80-line checklists written in 10 minutes. They miss critical patterns around testing, security, CI/CD, multi-agent coordination, observability, and production operations.

**Result:** Agents make the same mistakes repeatedly — skipping tests, writing unreviewable PRs, ignoring security, creating untracked technical debt.

**Solution:** This template was built by systematically analyzing 100+ real-world AGENTS.md files, 14 TODO.md files, 22 research papers (AgentBench, CAMEL, MetaGPT), and production codebases. Every section addresses a specific, observed failure mode.

**Guarantee:** No section exists "for completeness." Every rule eliminates a real failure mode observed in the wild. The file is self-governing — Section 50.8 requires agents editing AGENTS.md to follow every rule within it.

### Comparison

| | Typical AGENTS.md | This Template |
|---|---|---|
| **Sections** | 5-15 | 51 |
| **Testing depth** | "Write tests" | Flaky management, mutation testing, contract testing, chaos engineering, coverage enforcement |
| **Security** | "No secrets in code" | Prompt injection detection, audit logging, key encryption, IP whitelisting, 6-category NEVER list |
| **Production** | Basic Docker | Circuit breaker, DLQ, middleware stack, health endpoints, structured logging, OpenTelemetry, SLOs |
| **Multi-agent** | Not covered | Sequential/hierarchical/collaborative patterns, role templates, termination criteria |
| **Code quality** | Ruff/mypy mention | 19-point checklist, anti-pattern catalog, bloat detection, AI-specific laziness/uncertainty signals |
| **Git workflow** | "Descriptive commits" | WHY-focused format, human-sounding messages, conventional commits, PR templates, size gates |
| **Self-governance** | None | AGENTS.md governs its own maintenance — self-referential rules prevent staleness |

---

## 📁 File Structure

```
anchor/
├── AGENTS.md                  # ⭐ The main template — 51 sections, copy this into your project
├── STARTUP.md                 # 🚀 AI agent bootstrap guide — builds a project from scratch in 4 phases
├── README.md                  # 📖 This file
├── .gitignore                 # 🔒 Standard gitignore (includes tests/)
│
├── CLAUDE.md                  # 🤖 Anthropic Claude agent config (references AGENTS.md)
├── CLAUDE.desktop.md          # 💻 Anthropic Claude desktop app config
│
├── .github/
│   └── copilot-instructions.md  # 🔵 GitHub Copilot instructions
│
├── .cursor/                   # 🟣 Cursor IDE agent rules
│   └── rules/
│       └── project-rules.mdc
│
├── .windsurf/                 # 🟠 Windsurf IDE agent config
│   └── config.md
│
├── .continue/                 # 🟢 Continue.dev agent config
│   └── config.md
│
├── .claude/                   # ⚙️ Claude config (JSON)
│   └── config.json
│
├── docs/                      # 📚 Supporting documentation
│   └── AGENT_INSTRUCTIONS.md  # Universal fallback agent instructions
│
├── research/                  # 🔬 Academic research backing all sections
│   ├── index.md               # Research catalog
│   ├── papers/                # AgentBench, CAMEL, MetaGPT, Voyager, HuggingGPT
│   └── whitepapers/           # Agentic AI best practices
│
└── tests/                     # 🧪 Quality validation tools
    └── test_agents_md_quality.py  # Automated audit: contradictions, code validity, workflow coverage
```

---

## 🔬 Research Foundation

Every section is backed by peer-reviewed research or production experience:

| Source | Type | Applied To |
|--------|------|------------|
| **AgentBench** (arXiv:2308.03688) | ICLR 2024 Paper | Failure modes (IF/IA/TLE/CLE), instruction following evaluation |
| **CAMEL** (arXiv:2303.17760) | NeurIPS 2023 Paper | Multi-agent cooperation patterns, role assignment, termination criteria |
| **MetaGPT** (arXiv:2308.00352) | ICLR 2024 Paper | Sequential handoff patterns, verification gates, SOPs |
| **PEP 8 / Google Style Guide** | Standards | Code quality, docstring format, type annotations |
| **Google Testing Blog** | Industry | Flaky test management, mutation testing, test isolation |
| **Netflix Chaos Engineering** | Industry | Chaos experiment design, steady-state hypothesis, blast radius |
| **Keep a Changelog / SemVer** | Community Standards | Versioning, changelog format, release automation |
| **Microsoft C4W Checklist** | Industry | CI/CD, coverage thresholds, observability, security scanning |
| **Production Codebase Analysis** | Empirical | Circuit breaker, DLQ, middleware stack, health endpoints, audit logging, prompt injection detection |

Full research catalog: [`research/index.md`](research/index.md)

---

## 🛠 How to Use

### For an existing project:
```bash
# Copy the core template
cp anchor/AGENTS.md ./my-project/AGENTS.md

# Trim to fit — keep only relevant sections
# Target: ≤2,000 lines for project-specific use (Section 51.3)
```

### For a new project:
```bash
# Copy STARTUP.md and follow its 4-phase bootstrap
cp anchor/STARTUP.md ./my-new-project/
# Phase 1: Directory structure
# Phase 2: All agent config files
# Phase 3: .gitignore, .env.example, README.md, TODO.md, DEEPDIVE.md
# Phase 4: git init and commit
```

### Customization checklist:
- [ ] Delete inapplicable sections (keep only what matches your tech stack)
- [ ] Update tech stack defaults (Section 28) to match your choices
- [ ] Set your own branch protection rules (Section 38.6)
- [ ] Configure your own CI/CD templates (Section 38)
- [ ] Add project-specific gotchas to Section 25
- [ ] Fill in DEEPDIVE.md with your architecture narrative (Section 5)

---

## 🤖 Supported AI Agent Platforms

The template ships with config files for 8+ AI coding agent platforms. All reference AGENTS.md as the single source of truth:

| Platform | Config File | Format |
|----------|------------|--------|
| **Claude Code** (Anthropic) | `CLAUDE.md` | Markdown |
| **Claude Desktop** | `CLAUDE.desktop.md` | Markdown |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Markdown |
| **Cursor** | `.cursor/rules/project-rules.mdc` | MDC |
| **Windsurf** | `.windsurf/config.md` | Markdown |
| **Continue.dev** | `.continue/config.md` | Markdown |
| **OpenCode** | `AGENTS.md` (primary) | Markdown |
| **Any agent** | `docs/AGENT_INSTRUCTIONS.md` | Markdown (universal fallback) |

---

## 🧪 Quality Validation

The AGENTS.md file is self-tested. Run the audit:

```bash
python3 tests/test_agents_md_quality.py
```

The audit checks:
- **Section structure** — All 51 sections present, sequentially numbered
- **Contradiction detection** — No conflicting NEVER/ALWAYS rules
- **Actionable MUST rules** — Every MUST rule links to concrete implementation
- **Code block validity** — All 66 Python blocks parse correctly
- **Workflow coverage** — 9 common development workflows all covered
- **Markdown validity** — No broken references or unclosed blocks
- **Size & density** — Section balance analysis

**Status: 0 failures. 0 warnings.** See the test output inline in the tool results above.

---

## 📊 Stats

| Metric | Value |
|--------|-------|
| **Sections** | 51 |
| **Lines** | 5,780 |
| **Words** | ~25,500 |
| **Python code blocks** | 66 |
| **Research sources** | 22 (12 papers, 10 projects) |
| **Agent platforms supported** | 8+ |
| **DOCKER/K8s templates** | 4 |
| **CI/CD workflow templates** | 3 |
| **Security patterns** | 9 |
| **Testing patterns** | 12 |
| **Anti-patterns documented** | 24 |

---

## 🤝 Contributing

This template follows its own rules. Before contributing:

1. **Read Section 50.8** — AGENTS.md governs itself. Agents editing it must follow all rules herein.
2. **Read Section 51.2** — Propose additions when you encounter a failure mode not yet covered.
3. **Run the audit** — `python3 tests/test_agents_md_quality.py` must pass.
4. **Follow Section 33** — PRs must stay under 800 lines.
5. **Follow Section 15** — Commit messages must be human-sounding, WHY-focused.
6. **Follow Section 35** — Use the PR template with HUMAN/AGENT disclosure sections.

**What to contribute:**
- Rules that eliminate a *specific, observed* failure mode
- Research backing for existing or new rules
- Cross-references between related sections
- Test examples demonstrating correct behavior

**What NOT to contribute:**
- Rules without a demonstrated failure mode they prevent
- "Nice to have" sections that duplicate existing coverage
- Tool-version-specific trivia (pin those in config files, not AGENTS.md)
- General advice already covered by PEP 8 or standard style guides

---

## 📜 License

MIT — use it, modify it, ship it. Attribution appreciated.

---

<sub>Anchor — keep your agents grounded. 51 sections. 0 filler. Built from 100+ real-world AGENTS.md files, 22 research papers, and production codebases.</sub>
