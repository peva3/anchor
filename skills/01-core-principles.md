# Skill 01: Core Principles

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 1. Core Principles

- **No dead code.** Every function must be called by a production path. Remove unused imports, variables, and definitions immediately. *(How: Section 9 — vulture sweep before commit)*
- **No stubs.** Every function, module, component, and endpoint must have a real implementation. *(How: Section 8 — test execution validates real output)*
- **No silent failures.** Wrapped exception handlers (`except Exception: pass`) must have a comment explaining why the failure is non-critical. Log before swallowing. *(How: Section 10 — error handling patterns)*
- **Test-first.** Every module should have corresponding tests. Tests must pass before moving on. *(How: Section 8, Section 40 — coverage enforcement)*
- **Proven integration.** After building any component, verify it works end-to-end. Do not mark a task complete without verification. *(How: Section 23 — verification gates)*
- **Cross-service contract tests.** When building features spanning multiple services, write integration tests that exercise the actual HTTP contracts between them. *(How: Section 48 — contract testing)*
- **Trace every function call.** Before marking a module complete, verify every public function is called by a production path. *(How: Section 9 — vulture identifies uncalled functions)*
- **Navigate efficiently.** This document is long by design (universal template). Jump to [Section Index](#section-index) or [Quick-Navigation Cheatsheet](#quick-navigation-cheatsheet) instead of reading sequentially. For project-specific use, trim to ≤2,000 lines. *(How: Section 51.3)*

---

