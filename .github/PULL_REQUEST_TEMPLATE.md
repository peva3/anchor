<!-- See AGENTS.md Section 35 for the full PR template -->
<!-- This file is read by GitHub when a contributor opens a PR. -->
<!-- HUMAN reviewers MUST fill in the "HUMAN:" section before merging. -->

## Description

### What Changed

<Describe what this PR does in plain language. Focus on behavior, not code.>

### Why

<Explain the problem this solves. Who benefits? What was broken or missing?>

### How

<High-level approach. Mention key decisions: "Chose X over Y because Z.">

### Testing

- [ ] `python3 tests/test_agents_md_quality.py --strict` passes
- [ ] `pytest tests/` passes
- [ ] Manual verification performed (describe what was tested)

### Breaking Changes

<Write "None." if no breaking changes — never leave blank.>

---

## HUMAN: Reviewer Verification

<!-- HUMAN: The human reviewer MUST check this box after personal verification. -->
<!-- AI agents MUST NOT check this box. -->

- [ ] I have personally read the diff, run the audit locally, and verified the change is correct.

---

## AI Agent Disclosure

### Agent Decision Log

<Document any non-obvious decisions the agent made. Why were these choices made?>

### Areas Needing Human Review

<Point out specific code sections, architectural decisions, or edge cases the human should scrutinize.>

### Agent Self-Check

- [ ] Code follows project conventions (checked existing patterns)
- [ ] No dead code (vulture clean)
- [ ] No unused imports (ruff clean)
- [ ] Tests cover new behavior
- [ ] Change size is within limits (under 800 lines per Section 33)
- [ ] No "laziness" anti-patterns (Section 34.2)
- [ ] No "uncertainty" signals (Section 34.3)
- [ ] No "bloat" additions (Section 34.4)
