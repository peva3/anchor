# Skill 01: Core Principles

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 1. Core Principles

- **No dead code.** Every function must be called by a production path. Remove unused imports, variables, and definitions immediately. *(How: [Section 9](skills/09-linting-type-checking.md) — vulture sweep before commit)* Carve-out: test helpers, public library exports, `__init__.py` re-exports, and `console_scripts` entry points are legitimate — whitelist them for vulture rather than deleting.
- **No stubs.** Every function, module, component, and endpoint must have a real implementation. *(How: [Section 8](skills/08-testing-requirements.md) — test execution validates real output)* `...`/`pass` is allowed only for abstract methods, Protocols, and interface definitions.
- **No silent failures.** Wrapped exception handlers (`except Exception: pass`) must have a comment explaining why the failure is non-critical. Log before swallowing. *(How: [Section 10](skills/10-error-handling-patterns.md) — error handling patterns)*
- **Test-first.** Every module should have corresponding tests. Tests must pass before moving on. *(How: [Section 8](skills/08-testing-requirements.md), [Section 40](skills/40-code-coverage-enforcement.md) — coverage enforcement)*
- **Proven integration.** After building any component, verify it works end-to-end. Do not mark a task complete without verification. *(How: [Section 23](skills/23-verification-gates.md) — verification gates)*
- **Cross-service contract tests.** When building features spanning multiple services, write integration tests that exercise the actual HTTP contracts between them. *(How: [Section 48](skills/48-contract-testing-pact.md) — contract testing)*
- **Trace every function call.** Before marking a module complete, verify every public function is called by a production path. *(How: [Section 9](skills/09-linting-type-checking.md) — vulture identifies uncalled functions)*
- **Navigate efficiently.** This document is long by design (universal template). Jump to [Section Index](#section-index) or [Quick-Navigation Cheatsheet](#quick-navigation-cheatsheet) instead of reading sequentially. For project-specific use, trim to ≤2,000 lines. *(How: [Section 51.3](skills/51-instruction-architecture-context-economy-self-improvement.md))*

---

