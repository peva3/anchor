# Skill 06: TODO.md — Task Tracking Standard

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 6. TODO.md — Task Tracking Standard

Use this structure for tracking project tasks:

```markdown
# TODO.md — Project Name

## Legend
- ✅ Complete
- 🔄 In Progress
- ⬜ Not Started

## Current Sprint / Phase

| # | Status | Description |
|---|--------|-------------|
| 1 | ✅ | Completed task |
| 2 | 🔄 | Active task |
| 3 | ⬜ | Upcoming task |

## Completed Sprints

| Sprint | Status | Deliverable |
|--------|--------|-------------|
| 1   | ✅ | Feature A |
| 2   | ✅ | Feature B |

## Notes
- Document architectural decisions made during task completion
- Record any deviations from original plan and why
- Track build size delta for firmware/binary projects
```

**For multi-phase projects**, also track sub-tasks:
```
| 5a | ✅ | Sub-task A |
| 5b | ✅ | Sub-task B |
```

### Definition of Done

A task is only marked ✅ when **all** of the following are true:
- Code is written and passes tests, lint, and type check (Sections 8/9)
- Tests were added for the new behavior (they fail without the fix)
- Docs/TODO/DEEPDIVE were updated in the same change
- The change is within PR size limits ([Section 33](skills/33-pr-change-size-standards.md)) or split appropriately
- The work is committed (a task is not "done" until it's committed and pushed)

### Task → Commit Linkage

Mark a task complete in the **same commit/PR** that implements it — the commit message references the task: `feat: add pagination (TODO item 12)`. This keeps history and TODO.md in sync and makes it easy to find which commit shipped what.

### Drift Rule

If you change scope or approach mid-task, update the TODO.md row at that moment (same commit), not at the end. Never let TODO.md describe work that no longer matches the code.

---

