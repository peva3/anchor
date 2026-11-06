---
name: skill-56-agent-memory-and-state-management
description: "Section 56 — Agent Memory & State Management. Load when: Long-running sessions, compaction."
---
# Skill 56: Agent Memory & State Management

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 56. Agent Memory & State Management

Agent state lives in several places with different lifetimes. Knowing what survives — and what does not — prevents agents from losing work, re-doing work, or trusting stale context.

### 56.1 What Survives What

| Store | Survives compaction? | Survives new session? | Notes |
|-------|--------------------|----------------------|-------|
| Conversation context | No | No | The working set; compaction summarizes it |
| Project file (AGENTS.md / CLAUDE.md / DEEPDIVE.md) | Yes | Yes | Reloaded at session start |
| Auto memory (project/user memory) | Yes | Yes | Written by the agent between tasks |
| Skills listing | Yes | Yes | Individual skill content loads lazily |
| Subagent context | No | No | Isolated from the parent by design ([Section 22](skills/22-multi-agent-cooperation-patterns.md)) |
| TODO.md / task file | Yes | Yes | Durable task state — update it as you go |
| /tmp scratch | No | No | Never store anything important there |

### 56.2 MEMORY.md Discipline

- Keep persistent memory files short: aim for ~200 lines / ~25KB or less — enough for durable facts, not a log.
- Record: project-specific decisions, conventions, gotchas, where things live, and the current task's durable state.
- Prefer updating the project's own files (AGENTS.md, DEEPDIVE.md, TODO.md) over a parallel memory file so the knowledge ships with the repo.
- Purge entries once they're captured in code, docs, or tests — memory that duplicates the repo drifts.

### 56.3 Compaction Awareness

- After compaction, the agent must re-establish state from durable sources (project files, memory, TODO.md) — never from memory of the conversation.
- If compacting mid-task, write the task's current state to a durable file FIRST.
- Subagents get a fresh context; give them a self-contained brief with all facts they need ([Section 22](skills/22-multi-agent-cooperation-patterns.md)).

### 56.4 Session & Resume

- When resuming an interrupted task, read TODO.md + the relevant files before acting; do not assume prior context survived.
- State that must survive a reboot belongs in the repo (code, config, tests), not in the conversation.

### 56.5 Multi-Agent Memory Isolation

- Each subagent has isolated memory; the parent owns durable state.
- Handoffs pass a written context, not a reference to "what we discussed" ([Section 22](skills/22-multi-agent-cooperation-patterns.md)).
- Never let one agent's untrusted reading ([Section 55](skills/55-prompt-injection-defenses-for-agents.md)) leak into another agent's instructions.

### 56.6 The Handoff Artifact

A handoff is a written packet, not a conversation summary. Write it to a file (or the task
body) so it survives compaction, a new session, and a different agent.

```markdown
# Handoff — <task / slice>

## Goal
One sentence: the outcome, not the activity.

## State
- Done: <what is verified, with the command/output>
- In progress: <the exact file and line, or the failing test>
- Not started: <the next slice>

## Decisions
| Decision | Choice | Why | Reversible? |
|----------|--------|-----|-------------|

## Facts the next agent must not rediscover
- Where the relevant code lives
- The command that reproduces the failure
- The constraint that ruled out the obvious approach

## Constraints
Deadline, approvals needed, files that must not be touched.

## Next action
The single next step, with its verification.
```

Rules:

- **Self-contained.** A fresh context must be able to act without reading this conversation.
- **State the verification, not just the claim.** "Tests pass" is weaker than the command
  and its output ([Section 23](skills/23-verification-gates.md)).
- **Record rejected paths** so the next agent does not retry them.
- **Name the owner** if a decision needs a human ([Section 67](skills/67-requirements-elicitation-grilling.md)).
- **Keep it short.** A handoff longer than the work is sediment; link to the code instead.

---

## References

- Claude Code Memory (CLAUDE.md + auto memory) — https://code.claude.com/docs/en/memory
- Claude Code Context Window — https://code.claude.com/docs/en/context-window
