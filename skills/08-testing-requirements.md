---
name: skill-08-testing-requirements
description: "Section 8 — Testing Requirements. Load when: Writing/running tests."
---
# Skill 08: Testing Requirements

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 8. Testing Requirements

- **Unit tests** for all new functions
- **Integration tests** for workflows spanning multiple components
- **Cross-service contract tests** for HTTP API interactions
- Mock external APIs (not live calls in CI)
- Use fixtures in `conftest.py` for shared setup

### Test-Driven Development (Red → Green)

For behavior changes, the default loop is **red → green → refactor**:

1. **Red** — write one test that fails for the right reason. Run it; confirm the failure
   message names the missing behavior, not a typo or import error.
2. **Green** — write the smallest production change that makes exactly that test pass. Do
   not add unrequested behavior; do not weaken the assertion.
3. **Refactor** — clean up with the test green. Refactoring belongs here or in review, not
   while the test is red ([Section 70](skills/70-two-axis-code-review.md)).

**One vertical slice at a time.** A slice is the smallest change that is demoable on its
own — schema, code, and test together. Do not write all the tests first (horizontal
slicing); a suite of red tests proves nothing until behavior exists, and the slices stop
being independently reviewable ([Section 68](skills/68-spec-and-ticket-decomposition.md)).

**Agree the seam before writing.** A test needs a place to observe behavior without
reaching into internals. If the only way to test the change is to poke private state, the
seam is wrong — fix the design first ([Section 71](skills/71-codebase-design-deep-modules.md)).

**TDD anti-patterns:**

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| **Implementation-coupled** | Test mocks every internal call | Assert observable behavior |
| **Tautological** | Test recomputes the expected value the same way | Hard-code the expected result |
| **Horizontal slicing** | Ten red tests, no production code | One slice: test + code |
| **Test after, never red** | The test never failed | Stash the fix, watch it fail |
| **Over-mocked** | Test passes when the feature is deleted | Use a real unit or an integration test |

TDD is not required for a throwaway spike ([Section 65](skills/65-time-boxed-delivery-mode.md))
or a pure rename with an existing suite, but the regression test is still required
([Section 69](skills/69-bug-diagnosis-loop.md)). See
[Section 45](skills/45-flaky-test-management.md) for keeping the new test deterministic and
[Section 46](skills/46-mutation-testing.md) for proving it can fail.

### Test Commands
```bash
pytest                           # All tests
pytest tests/test_specific.py    # Single file
pytest -k "pattern"              # Matching tests
pytest --cov=. --cov-report=term-missing  # With coverage
```

---

### End-to-End and Browser Testing

- **Use a real browser driver** for user flows (Playwright, Cypress, or Selenium) — unit tests cannot prove a form submits or a modal traps focus. Playwright is the usual default: multi-browser, auto-waiting, trace viewer.
- **Test the flow a user performs**, not the DOM structure: click, type, navigate, assert on visible outcomes. Selectors by role/label survive refactors; CSS-path selectors do not.
- **Keep E2E few and slow-tolerant.** Cover the money paths (signup, checkout, login); push everything else down to integration tests. A large E2E suite becomes the flakiest thing you own (Section 45).
- **Run against seeded data** you control, and reset state between specs; never point E2E at production.
- **Capture artifacts on failure** (screenshot, trace, video) so a red run is diagnosable without reproducing locally.
