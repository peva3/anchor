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
