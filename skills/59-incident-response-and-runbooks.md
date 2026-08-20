# Skill 59: Incident Response & Runbooks

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 59. Incident Response & Runbooks

Outages are inevitable. The difference between a bad incident and a manageable one is preparation: defined severities, runbook-first recovery, and blameless learning.

### 59.1 Severity Taxonomy

| Severity | Definition | Examples | Response |
|----------|-----------|----------|----------|
| **SEV-1** | Total outage / data loss / security breach | Service down, prod data corrupted, credentials leaked | Immediate, 24/7 escalation, human owner |
| **SEV-2** | Major degradation, core feature broken | Payments failing, login broken, DB slow | Same-day, on-call owner |
| **SEV-3** | Minor degradation, workaround exists | Cosmetic bug, one region slow | Next-business-day, normal sprint |
| **SEV-4** | Noticeable but non-impacting | Log noise, minor metric dip | Track, fix in normal flow |

- Define the threshold per project before the incident; do not define severity while panicking.
- Ties to [Section 41](skills/41-observability-standards.md) (alerting): alerts map to severities so pages only fire for SEV-1/2.

### 59.2 Runbook-First Recovery

- Every critical service has a runbook: how to confirm health, common failure signatures, and the **rollback path**.
- **Rollback before debugging.** If a change caused it, revert (`git revert`) or flip the feature flag first, then investigate. Speed to safe beats speed to root cause.
- Runbooks must live in the repo (`docs/runbooks/`), versioned, and referenced from the health/ops docs ([Section 16](skills/16-documentation-requirements.md)).

### 59.3 The Response Timeline

1. **Detect** — alert fires ([Section 41](skills/41-observability-standards.md)), human or agent pages on-call.
2. **Triage** — classify severity, confirm it is real, decide: rollback vs fix-forward.
3. **Mitigate** — execute the runbook step; restore service; freeze unrelated changes.
4. **Communicate** — status update with: what's affected, what's being done, ETA.
5. **Investigate** — after stabilization, find root cause (don't do deep investigation mid-fire).
6. **Postmortem** — blameless writeup (below), action items with owners.

### 59.4 Blameless Postmortems

- Written within ~5 business days; focused on **systems, not people** — the goal is preventing recurrence, not blame.
- Contents: timeline, impact (users/cost/data), root cause, what worked, what didn't, action items (each with owner + deadline).
- **Blameless** = the author can be fully honest. No "who did this"; ask "what allowed this to happen?"
- Escalate systemic items into TODO.md / [Section 52](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md) enforcement so they don't recur silently.

### 59.5 Escalation & On-Call

- Named on-call owner per service, documented rotation, and a clear escalation tree (primary → secondary → manager).
- Agents escalating for help must bring evidence: `file:line`, logs, and what they tried ([Section 26](skills/26-getting-help.md), [Section 52.5](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md)).
- Production experiments/Game Days require explicit human approval and a documented window ([Section 49](skills/49-chaos-engineering.md), [Section 36.4](skills/36-explicit-prohibitions-the-never-list.md)).

### 59.6 Incident Rules (NEVER additions)

- **NEVER** make unrelated changes during an incident — they get reverted with the rollback.
- **NEVER** lie or omit in status updates; say "investigating" when that's the truth.
- **NEVER** do a postmortem as punishment — blameless or nothing.
- **NEVER** skip the restore drill for backups ([Section 43](skills/43-database-backup-recovery.md)) and then discover in an incident that restore doesn't work.

---

## References

- Principles of Chaos Engineering (game days) — https://principlesofchaos.org/
