# Skill 23: Verification Gates

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 23. Verification Gates

Before proceeding to the next step, verify explicitly.

### 23.1 Format Validation

Output must match expected schema:

```python
# Validate structured output
import jsonschema
jsonschema.validate(instance=output, schema=expected_format)
```

### 23.2 Action Validation

Action must be valid for current state:

```python
# Check state before acting
if not is_valid_action(current_state, proposed_action):
    raise InvalidActionError(f"Cannot {action} in state {current_state}")
```

### 23.3 Context Validation

No context limit exceeded:

```
Before each major step:
- Estimate tokens needed for remaining work
- If remaining context < 20%, summarize/snapshot current state
- If context limit would be exceeded, flush and resume fresh
```

### 23.4 Termination Validation

Completion criteria must be met:

```
completion_checklist:
  - [ ] Output matches expected format
  - [ ] All functions have production call paths
  - [ ] No unused imports/variables (vulture clean)
  - [ ] Tests pass
  - [ ] Lint clean
  - [ ] Type check clean
  - [ ] Documentation updated (DEEPDIVE.md if needed)
```

### 23.5 Error Recovery Hierarchy

When validation fails:

1. **Retry** (max 3 attempts, exponential backoff: 1s, 2s, 4s)
2. **Alternative approach** — Try different method to achieve same goal
3. **Fallback** — Degrade gracefully (skip non-critical, continue core)
4. **Escalate** — Report detailed error with what was attempted, let user decide

---

