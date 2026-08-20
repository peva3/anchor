# Skill 61: Snapshot / Golden-File Testing

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 61. Snapshot / Golden-File Testing

Snapshot tests capture output (rendered HTML, serialized JSON, CLI text) and fail when it changes. Powerful for locking in complex output — and easy to misuse by blindly accepting changes.

### 61.1 When to Use

- Rendering / serialization output: HTML, JSON responses, CLI output, AST dumps, generated configs.
- Output too large or too detailed to assert field-by-field (but prefer explicit assertions for the *important* fields and snapshot the rest).
- Cross-language snapshot: jest snapshots, `pytest-snapshot`, syrupy.

### 61.2 The Never-Blindly-Accept Rule

**NEVER run `--snapshot-update`/`--ci` blindly.** Every snapshot change must be reviewed line-by-line before being accepted:

```bash
# Review the diff first
pytest tests/ -k snapshot

# Only after confirming the change is intentional:
pytest tests/ -k snapshot --snapshot-update
```

- A snapshot "update" that silently swallows a regression is the worst kind of false green ([Section 24.10](skills/24-common-failure-modes.md)).
- In CI, run snapshots in read-only mode (syrupy `--ci`) so a changed snapshot FAILS rather than self-updating.

### 61.3 Matchers for Dynamic Fields

Snapshots fail on incidental churn (timestamps, UUIDs, random IDs). Use matchers instead of accepting the whole output:

```python
# syrupy
def test_response(snapshot):
    assert json.dumps(render()) == snapshot(matcher=snapshot.matcher.fs.path_sorted)

# or mask dynamic fields
def test_response(snapshot):
    assert redact_dynamic_fields(render()) == snapshot
```

- Common patterns: sort keys, mask timestamps/ids, ignore unstable ordering (dict ordering, set order).
- Only use matchers where the field genuinely varies; don't mask a field that should be stable — that hides real regressions.

### 61.4 Keep Snapshots Reviewable

- Keep snapshot files small; a giant snapshot is as unreadable as a giant PR ([Section 33](skills/33-pr-change-size-standards.md)).
- Split snapshots per test; don't accumulate one file for everything.
- Review snapshot diffs during code review exactly like code diffs ([Section 35](skills/35-pr-description-format-template.md)).
- When the underlying library/format bumps intentionally, update snapshots in a dedicated change so the review is isolated.

### 61.5 Snapshot Rules (NEVER additions)

- **NEVER** `--snapshot-update` to "make CI pass" — that's deleting evidence of a change you didn't check.
- **NEVER** snapshot secrets, tokens, or PII in test output ([Section 14](skills/14-logging-standards.md)).
- **NEVER** let generated snapshot files bloat the PR beyond the change-size limit (they count toward [Section 33](skills/33-pr-change-size-standards.md) unless generated).

---

## References

- syrupy (snapshot testing) — https://github.com/syrupy-project/syrupy
- pytest-snapshot — https://pypi.org/project/pytest-snapshot/
