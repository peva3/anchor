# Contributing to Standardized AGENTS.md

This project follows its own rules (Section 50.8). Before contributing, read AGENTS.md — the file governs itself and its contributors.

## Quick Reference for Contributors

| Rule | Section |
|------|---------|
| PR size limit: 800 lines max | Section 33.1 |
| Single feature per PR | Section 33.3 |
| Use the PR description template | Section 35 |
| Follow the decision ladder | Section 50.1 |
| Human-sounding commit messages | Section 15 |
| Never go rogue — ask before creating PRs | Section 2 |

## What to Contribute

### Good contributions:
- Rules that eliminate a **specific, observed failure mode** — something that happened in the wild, not a hypothetical
- Cross-references between related sections — an agent should not need to read every section to know they're connected
- Research backing for existing or new rules — citations to papers, standards, or production incidents
- Section trim suggestions — if a section can be merged into another without losing fidelity
- Test examples that demonstrate correct behavior under the rules
- Corrections to code examples that don't parse or don't follow their own advice

### Bad contributions:
- Rules without a demonstrated failure mode they prevent
- "Nice to have" sections that duplicate existing coverage
- Tool-version-specific trivia (pin those in pyproject.toml, not AGENTS.md)
- General advice already covered by PEP 8, Google Style Guide, or standard references
- Opinion-based preferences (use TypeScript vs Python, tabs vs spaces) — if it's not backed by standards or observed failures, it doesn't belong
- Formatting-only changes — raise a bug if ruff/ruff-format fails, don't hand-edit formatting
- Sections that future agents would need to explain away ("we don't follow Section X because...")

## Before Submitting

1. **Run the quality audit:** `python3 tests/test_agents_md_quality.py`
2. **Verify your PR stays under 800 lines** (Section 33.1)
3. **Use the PR template** (Section 35) — include both HUMAN and AGENT sections
4. **Self-check against the anti-patterns** (Section 34) — no laziness, uncertainty, or bloat
5. **Follow the commit style** (Section 15) — WHY-focused, human-sounding

## Adding New Sections

Before adding a new section, verify ALL of these:

- [ ] The pattern is NOT already covered by an existing section (search for keywords)
- [ ] The pattern addresses a specific, observed failure mode (not a hypothetical)
- [ ] The pattern is universal enough to belong in a template (not project-specific)
- [ ] Research or citations back the claim
- [ ] The section includes concrete implementation guidance (not just principles)
- [ ] Cross-references to related sections are included
- [ ] The Change Log is updated (bottom of AGENTS.md)

## Style Guide for AGENTS.md

- Code blocks use correct language tags (` ```python`, ` ```yaml`, ` ```bash`, ` ```json`, etc.)
- Examples show both CORRECT and WRONG patterns, clearly labeled
- Every MUST/REQUIRED rule has a cross-reference to HOW to implement it
- Sections are self-contained — an agent should be able to read one section and understand it without jumping around
- Structure: explanation → DO example → DON'T example → edge cases → when NOT to apply

## Questions

If you're unsure whether a contribution is appropriate:
1. Check if a relevant research paper or standard supports the change
2. Check if the pattern has been observed in production failures
3. Open an issue to discuss before writing code

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
