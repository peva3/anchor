# Skill 03: Shell Execution Rules

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 3. Shell Execution Rules

**CRITICAL:** A plugin automatically prepends `snip` to all shell commands. `snip` requires a real executable, so it will fail if applied to shell built-ins (`cd`, `export`, `source`).

**Correct format (Subshell):**
```bash
bash -c 'cd /path/to/directory && your_command --flags'
bash -c 'export VAR=value && your_command'
```

**Incorrect format (Will fail):**
```bash
cd /path/to/directory && your_command --flags
export VAR=value && your_command
```

---

