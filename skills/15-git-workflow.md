# Skill 15: Git Workflow

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 15. Git Workflow

**Commit Messages — Sound Human, Not AI:**

Write commits as if explaining to a colleague why this change exists:

```
Good (human-sounding):
"Prevented race condition in token refresh by adding mutex lock around 
auth state mutation. Previously, concurrent requests could cause the 
refresh callback to fire twice, resulting in a 401 loop."

Bad (AI-sounding):
"fix: fixed race condition in auth service"
```

**The WHY matters most:**
- Explain the problem that existed before this change
- Explain what the change does and why it solves the problem
- If there were alternatives considered, note why you picked this one
- Include any context that future developers (or agents) need to understand

**Pattern:**
```
<type>: <what changed>

<problem>: Why this needed fixing
<solution>: What the change does and why
<context>: Any important decisions, trade-offs, or gotchas
```

**Examples:**
```
api: Added JWT refresh endpoint to eliminate 401 loops

The token refresh had a race condition where concurrent requests could
trigger multiple refresh calls. Added mutex lock around auth state.
Ref: https://github.com/org/repo/issues/1234
```

```
frontend: Rewired timeline scrubber to use IntersectionObserver

GSAP physics caused dot highlighting to desync when scrolling fast.
IntersectionObserver 1px center tripwire provides reliable sync without
third-party dependencies. Removed all physics, reduced bundle by 47KB.
```

```
db: Added content_hash unique constraint to prevent duplicate ingestion

Two scrapers could race and insert the same article from different RSS 
feeds. Added unique constraint on content_hash with NULLS NOT DISTINCT.
Migration 010 adds constraint with deduplication pass.
```

**Small commits with big explanations are fine.** A 3-line change can have a 10-line commit message explaining the problem it solves.

**Note on brevity:** Section 50.4's output discipline (≤3 lines) applies to task-completion reports, NOT to commit messages. Commit messages follow THIS section's format (problem → solution → context). The rules do not conflict — they govern different domains.

---

- **Small, focused commits.** One logical change per commit.
- **Descriptive messages.** First line <72 chars, optional body for detail.
- **Never force push** to shared branches
- **Branch naming:** `feature/name`, `fix/name`, `sprint-n`

---

