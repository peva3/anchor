# Skill 33: PR & Change Size Standards

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 33. PR & Change Size Standards

Hard numeric boundaries prevent unreviewable changes from being submitted. These limits apply to all changes, whether human or AI-authored.

### 33.1 Size Limits — Hard Gates

| Change Type | Max Lines | Rationale |
|------------|-----------|-----------|
| **All changes** | 800 lines total | Hard cap. Canonical studies suggest keeping reviews even smaller: SmartBear found ~400 LOC is the optimal review size, Google's practice is "~100 lines is reasonable, ~1000 lines is too large." Prefer smaller PRs when the change can be split naturally. |
| **Complex logic** | 500 lines | Architectural changes, algorithm rewrites, security-sensitive code — requires deeper review |
| **Simple/mechanical** | 800 lines | Renames, formatting, type annotation additions — still must not exceed 800 |
| **Single file** | 500 lines | If a file exceeds 500 lines of change, split into multiple PRs |

**What counts as a "line of change":**
- Added lines count
- Modified lines count
- Deleted lines count (deletions are still review burden)
- Test files count toward the limit

**What does NOT count:**
- Generated code (OpenAPI clients, protobuf stubs, migration files)
- Lockfiles (poetry.lock, package-lock.json, uv.lock)
- Snapshot files (.snap, __snapshots__/)
- Auto-formatted changes (run `ruff format` separately, commit separately)

### 33.2 When Changes Exceed the Limit

**DO NOT submit the oversized change.** Instead:

1. **Split by concern.** Separate refactoring from feature work. Mechanical changes go in their own PR.
2. **Split by layer.** Database migration in one PR → API changes in another → frontend in another.
3. **Stack PRs.** PR #1 adds the API → merge → PR #2 adds the UI on top.
4. **Pre-extract.** Do preparatory refactoring in a separate PR before the feature PR.

**Example of splitting a 1,200-line feature:**
```
Original: 1,200 lines (new API + refactoring + tests)
Split into:
  PR #1: 350 lines — extract shared utilities (no behavior change)
  PR #2: 280 lines — add database migration and model
  PR #3: 420 lines — add API endpoints + tests
  PR #4: 150 lines — wire into frontend
```

### 33.3 Single Feature Rule

Each PR addresses exactly ONE concern:
- One feature, one fix, one refactor, or one mechanical change
- Do NOT mix "fix bug while I'm in the file" changes
- Do NOT include "while I was here" formatting changes in a feature PR
- If you find an unrelated bug, open a separate issue/PR

**Good PR scopes:**
```
fix: Corrected token refresh race condition
feat: Added pagination to search endpoint
refactor: Extracted validation logic into shared module
chore: Upgraded httpx to 0.27.0
```

**Bad PR scopes:**
```
fix: Corrected token refresh race condition AND refactored auth middleware AND updated logging format
^--- Three unrelated changes, impossible to review or revert independently
```

### 33.4 Draft PR Conventions

If code is evolving but useful for discussion:
- Open PR in **draft mode** (GitHub "Create draft pull request")
- Draft PRs are for discussion, not just unfinished work — use them to get early feedback on architecture
- Mark as "Ready for review" only when all checks pass and change size is within limits
- If the branch is not ready for any review, keep it local — do not open a PR

### 33.5 FIRST-TIME CONTRIBUTOR PATH (for AI agents joining a project)

When an agent starts work on a new project:
1. First contribution should be a **small bug fix** (under 200 lines)
2. This establishes understanding of project conventions and builds trust
3. Do NOT submit a large feature as a first contribution
4. Reputation matters — reviewers calibrate scrutiny based on contributor history
5. If your first PR gets closed for being too large, do not take it personally — split and resubmit

---

