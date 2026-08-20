# Skill 34: AI Code Quality — Anti-Pattern Detection

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 34. AI Code Quality — Anti-Pattern Detection

AI agents produce specific failure modes that human developers rarely create. Agents MUST self-check against these patterns before submitting code.

### 34.1 Think First — Explain Before Coding

The most common AI failure mode: jumping straight to code without understanding the system.

**MANDATORY before writing any code:**
1. **Read the relevant existing code** — understand patterns, conventions, and the surrounding architecture
2. **Explain your approach** — describe the architecture and reasoning before implementation
3. **Identify the integration points** — where does this change touch existing code?
4. **Check for existing utilities** — is there already a helper/function/class that does this?

**Red flag:** If you cannot explain WHY you chose this approach over alternatives, stop and think before coding.

### 34.2 Spot the Laziness — Common LLM Shortcuts

| Laziness Pattern | What It Looks Like | Why It's Bad |
|-----------------|-------------------|--------------|
| **Trivial tests** | `assert True`, `assert result is not None`, tests with no assertions | Creates false sense of coverage without testing behavior |
| **Overly wide types** | `Optional[T]` everywhere, `Any` in function signatures | Hides real nullability contracts, defeats type checking |
| **Catch-n-log** | `except Exception: logger.error(...)` without re-raise or proper handling | Swallows errors, leaves system in undefined state |
| **Copy-paste without understanding** | Mirroring local patterns without knowing why they exist | Propagates anti-patterns, misses context-specific requirements |
| **Unnecessary helpers** | Creating small helper methods referenced only once | Adds indirection without reducing complexity |
| **Bool/flag parameters** | `foo(True, False)` — ambiguous at call site | Force callers to write hard-to-read code, hide intent |
| **Negative tests for removed logic** | Tests that check behavior that no longer exists | Tests pass vacuously, provide zero value |

### 34.3 Spot the Uncertainty — Signs the Agent Is Confused

When an agent is uncertain about the right approach, it produces code with these tells:

| Uncertainty Signal | Example | What It Means |
|-------------------|---------|---------------|
| **Numbering approaches** | "Here are 3 ways I fixed this..." | Agent tried multiple things, picked one without conviction |
| **Overly defensive code** | Checking null 5 layers deep, validating already-validated data | Agent doesn't understand the data flow invariants |
| **Excessive try/except** | Wrapping every call in try/except without specific handling | Agent doesn't know which operations can actually fail |
| **Redundant null checks** | `if x is not None` on a value that is NEVER None by construction | Agent doesn't understand the type system or data model |
| **Adding to "god objects"** | Adding methods to already-too-large classes | Agent thinks "this is where things go" without questioning the design |

**Remediation when uncertainty signs appear:**
1. Stop and read the relevant abstractions again
2. Find examples of similar patterns in the existing codebase
3. If the pattern is truly unclear, ask the user before proceeding
4. Do NOT paper over uncertainty with defensive code

### 34.4 Spot the Bloat — Unnecessary Additions

| Bloat Pattern | What It Looks Like | What to Do Instead |
|--------------|-------------------|-------------------|
| **Commenting on the change, not the code** | "Changed the timeout from 30 to 60" | Comments should explain WHY the code is the way it is, not WHAT changed |
| **Excessive tests** | 15 tests testing the same happy path with different inputs | Test boundaries: empty, single, many, error, edge cases |
| **Logging everything** | `logger.info("Entering function")`, `logger.info("Exiting function")` | Log at boundaries, log decisions, log errors — not every step |
| **Over-parameterization** | Making every constant configurable when it will never change | Default to constants, extract to config only when actually needed |
| **Future-proofing** | Adding hooks, interfaces, or extension points "for later" | YAGNI — You Aren't Gonna Need It. Add when needed, not before. |

### 34.5 You Are Responsible for the Final Code

The chain of accountability is clear:
1. The AI agent proposes code
2. The AI agent tests the code
3. The AI agent verifies the code against these anti-patterns
4. The human reviews the final output

**Do NOT:**
- Submit code you haven't tested yourself
- Blame "the model" for bad code — you ARE the model's quality filter
- Assume the human will catch what you missed — your job is to catch it first

### 34.6 Module/File Size Bounds

| Limit | Threshold | Rationale |
|-------|-----------|-----------|
| **Module max** | 500 lines (excluding tests) | Beyond 500 lines, split into sub-modules |
| **File max** | 800 lines (excluding tests) | Beyond 800 lines, add new functionality in new modules |
| **Function max** | 50 lines | Extract sub-functions for complex logic |
| **Class max** | 300 lines | Consider composition over inheritance for larger classes |

**When a file exceeds the limit:**
- Identify cohesive groups of functions — move to new module
- Do NOT just split alphabetically or arbitrarily
- Each new module should have a clear, single responsibility
- Update imports across the codebase accordingly

### 34.7 Platform Support Requirements

Unless explicitly stated otherwise for the project:
- Tests and features MUST support Linux, macOS, and Windows
- No Unix-isms in cross-platform code (no `/tmp` hardcoding, no `os.fork`, no shell-specific commands)
- Use `pathlib.Path` instead of string paths
- Use `tempfile` module for temporary files, not `/tmp/` directly
- If a feature is explicitly OS-specific, document the limitation and guard with `sys.platform` checks
- CI must run on all three platforms if the project is cross-platform

---

