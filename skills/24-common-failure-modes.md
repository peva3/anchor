# Skill 24: Common Failure Modes

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 24. Common Failure Modes

Based on AgentBench (arXiv:2308.03688) findings on LLM agent failures.

### 24.1 Invalid Format (IF)

**Cause:** Agent doesn't follow output format instructions.

**Prevention:**
- Provide explicit schema with examples
- Use JSON schema validation
- Give exactly one valid output format

**Recovery:**
- Show example of correct format
- Retry with stricter constraints

### 24.2 Invalid Action (IA)

**Cause:** Format correct but action is invalid for current state.

**Prevention:**
- Validate state before suggesting actions
- Provide explicit list of valid actions
- Include state machine documentation

**Recovery:**
- Report current state and valid actions
- Suggest valid alternative

### 24.3 Task Limit Exceeded (TLE)

**Cause:** No solution found after maximum iterations/rounds.

**Prevention:**
- Define clear completion criteria upfront
- Set maximum iteration count
- Implement early termination when progress stalls

**Recovery:**
- Save current state for manual review
- Report what was tried and why it failed
- Ask user for guidance on alternative approach

### 24.4 Context Limit Exceeded (CLE)

**Cause:** Interaction history exceeds max context.

**Prevention:**
- Summarize context periodically (every ~50% of context)
- Snapshot key decisions to external storage
- Start fresh session with summary if needed

**Recovery:**
- Save all context to file
- Start new session with summarized state
- Resume from checkpoint

### 24.5 Hallucination Failures

**Cause:** Agent generates plausible but incorrect information.

**Prevention:**
- Require source citations in research tasks
- Validate against known facts before accepting
- Use tool outputs as ground truth, not agent memory

**Recovery:**
- Cross-check with authoritative source
- Flag as uncertain if cannot verify

---

