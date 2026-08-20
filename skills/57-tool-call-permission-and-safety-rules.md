# Skill 57: Tool-Call Permission & Safety Rules

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 57. Tool-Call Permission & Safety Rules

Tool execution is where an agent can cause real damage — filesystem writes, network calls, cloud changes, money. Permissions are the enforcement layer; prompt rules are not.

### 57.1 Permission Model — Deny-First Precedence

- **Deny wins over allow.** You cannot carve exceptions out of a deny with an allowlist ([Section 52](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md)).
- Precedence: `deny` → `ask` → `allow`. When in doubt, ask.
- Default posture is least privilege: allow only what the task needs, ask or deny everything else.

### 57.2 Permission Modes

| Mode | Behavior | Use for |
|------|----------|---------|
| **allow** | Runs without prompting | Read-only, safe, high-frequency tools |
| **ask** | Prompts the human before running | Writes, deletes, network egress, anything paid |
| **deny** | Blocks outright | Destructive ops, secrets access, bypasses |
| **defer** | Schedules/queues the decision | Multi-step flows needing review |

Examples:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Grep",
      "Glob",
      "Bash(npm test:*)"
    ],
    "ask": [
      "Bash(git push:*)",
      "Edit",
      "Write"
    ],
    "deny": [
      "Bash(git push --force:*)",
      "Bash(rm -rf:*)",
      "mcp__*__delete_*",
      "Bash(curl | bash:*)"
    ]
  }
}
```

### 57.3 PreToolUse Hooks for Enforcement

Hooks intercept tool calls before execution ([Section 52](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md)):

- PreToolUse receives the tool name + input; return `hookSpecificOutput.permissionDecision` of `deny`, `allow`, `ask`, or `defer` (not a top-level `decision` field).
- Exit code 0 = no decision (fall through), exit 2 = block.
- Use hooks to enforce structural rules (e.g. block `curl | bash`, block pushes to protected branches, block paid API calls without approval).

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by Section 57.2"
  }
}
```

### 57.4 Sandboxing

- The strongest enforcement layer is OS-level: run the agent in a container, bubblewrap, or VM with an egress policy ([Section 52.10](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md)). This survives prompt injection.
- Even with sandboxing, keep the permission deny list — defense in depth.
- Never disable sandboxing or permission checks to "speed up" a run. **NEVER** launch with `--dangerously-skip-permissions` or bypass permissions ([Section 36.9](skills/36-explicit-prohibitions-the-never-list.md)).

### 57.5 Rules for the Agent

- Before every tool call: is this within the task? Does it modify anything outside the task's scope? If yes → ask.
- **NEVER** bypass a denied permission, retry a blocked command with different spelling to dodge the deny, or modify tool inputs to avoid the permission check.
- **NEVER** paste secrets into tool arguments ([Section 36.9](skills/36-explicit-prohibitions-the-never-list.md)).
- Log tool calls and inputs (redacted) so abuse is detectable ([Section 54.3](skills/54-mcp-usage-and-guardrails.md)).
- Batch destructive changes behind a single explicit human-approved step rather than several `ask` prompts.

---

## References

- Claude Code Permissions — https://code.claude.com/docs/en/permissions
- Claude Code Hooks Guide — https://code.claude.com/docs/en/hooks-guide
- Claude Code Hooks Reference — https://code.claude.com/docs/en/hooks
