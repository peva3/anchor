# Skill 50: Intentional Minimalism — The Simplicity-First Architecture

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 50. Intentional Minimalism — The Simplicity-First Architecture

This section is not about "writing less code." It's about a structured decision protocol that treats complexity as cost and maps simplicity onto concrete actions. Before reaching for a library, a pattern, or even a function, run the ladder.

### 50.1 The Decision Ladder — Stop at the First Rung That Holds

Every implementation decision must run through this ordered protocol. Start at rung 1 and descend only if the current rung does not solve the problem:

```
Rung 1: YAGNI
  Does this need to exist at all? Can the requirement be satisfied by
  removing something instead of adding something? Challenge every "should"
  — only "must" survives this gate.

Rung 2: Standard Library
  Does the language/runtime already ship with this? Before importing
  anything new, check the stdlib index for your language version.

Rung 3: Native Platform Feature
  Does the browser, OS, or runtime platform already provide this?
  Browsers ship HTML5 validation, CSS grid, Web APIs. The OS ships
  cron, log rotation, file watching. The platform is free — use it.

Rung 4: Already-Installed Dependency
  Does a dependency already in pyproject.toml / package.json provide this?
  Do not add a new dependency when an existing one covers the need.

Rung 5: One Line
  Can this be solved with a single, clear line of code?
  If one line does it, do not write a function. Do not create a class.
  Do not build an abstraction. One line is self-documenting.
  **Guard:** If the one line is also UNREADABLE — deeply nested ternary,
  chained regex, or a comprehension with 3+ conditions — it fails
  the "clear" test. Drop to Rung 6 and write it legibly.

Rung 6: Minimum Code That Works
  Write the shortest possible implementation that passes all tests.
  No extension points. No configurability. No "what if" hooks.
  Future-you can add those when future-you has the requirement.
```

**The ladder is a reflex, not a research project.** Each rung takes seconds to evaluate. If you're spending minutes debating whether stdlib covers the need, drop to the next rung and move on.

**Ladder in practice:**
```python
# Requirement: validate an email address

# Rung 1 (YAGNI): Do we actually need to validate?
# Yes — this is a trust boundary accepting user input.

# Rung 2 (stdlib): Does Python ship email validation?
# No — re.match with a simple pattern is close but not stdlib.

# Rung 3 (native): N/A for backend.

# Rung 4 (existing dep): Is pydantic already installed?
# Yes — it's in requirements.txt.

# Rung 5 (one line): Can Pydantic do it in one line?
from pydantic import EmailStr  # <- Rung 5 achieved. Stop here.

# WRONG — skips the ladder entirely:
# pip install email-validator validators py3-validate-email
# class EmailValidator(ABC):
#     @abstractmethod
#     def validate(self, email: str) -> ValidationResult: ...
```

### 50.2 Structured Tradeoff Comments — Name the Ceiling

When you intentionally accept a shortcut, document it with a structured comment that names the KNOWN LIMIT and the UPGRADE TRIGGER:

```python
# ponytail: global lock on cache writes
# Upgrade to per-key locks if write contention exceeds 10%
_cache_lock = threading.Lock()

def set_cache(key: str, value: Any) -> None:
    with _cache_lock:  # Intentional — see above
        _cache[key] = value
```

**Format:**
```
# ponytail: <what was skipped or simplified>
# Upgrade to <what to build instead> if <measurable trigger condition>
```

**Why this format:**
- Names the ceiling so it's not a hidden landmine
- Ties the upgrade to a measurable condition (not a vague "if this gets slow")
- Makes debt scannable — `grep -r "ponytail:" src/` produces an instant ledger of all intentional shortcuts
- Distinguishes intentional simplifications from bugs-in-waiting

**Examples of good tradeoff comments:**
```python
# ponytail: O(n²) dedup scan
# Upgrade to hash-set dedup if n exceeds 10,000 items

# ponytail: fixed 30s polling loop
# Upgrade to websocket push if latency matters or server load increases

# ponytail: naive heuristic for spam detection (<80% accuracy)
# Upgrade to ML classifier if false positives exceed 2% of total traffic

# ponytail: single-region deployment
# Upgrade to multi-region if p99 latency exceeds 500ms for >1% of users
```

**What this is NOT:**
- NOT a substitute for fixing real bugs
- NOT a permission slip for sloppy code
- NOT a TODO — it has a named ceiling and a specific trigger
- NOT an excuse to skip error handling where data loss is possible

### 50.3 Safety Carve-Outs — What to NEVER Be Lazy About

The pursuit of simplicity has hard boundaries. These domains are exempt from the ladder — always invest full rigor:

| Domain | Why It's Exempt | Minimum Standard |
|--------|-----------------|------------------|
| **Input validation at trust boundaries** | The outside world is hostile. Unvalidated input is the #1 attack vector. | Validate type, range, and format for every external input. Use Pydantic or equivalent. |
| **Error handling that prevents data loss** | Silent data loss is unrecoverable. Users will not forgive you. | Every write operation must handle failure. Transactions or idempotency keys. |
| **Security** | Security shortcuts compound. One "temporary" bypass becomes permanent. | Parameterized queries, no eval/exec, encrypted secrets, auth on every endpoint. |
| **Accessibility** | Excluding users is not an optimization. It's a defect. | Semantic HTML, keyboard navigation, screen reader labels, color contrast. |
| **Hardware calibration** | The platform is never the spec ideal. A clock drifts. A sensor reads off. A regulator sags under load. Real hardware needs real calibration. | Measure, don't assume. Validate against physical ground truth. Document calibration drift over time. |
| **Anything explicitly requested** | If the user explicitly asks for something, build it as specified. The ladder optimizes everything ELSE. | Build what was asked for. Name simplifications in a tradeoff comment. Let the user decide. |

### 50.4 Output Discipline — Code First, Explanation Minimal

When presenting completed work:

**Rule:** Code first. Then at most three short lines: what was skipped, when to add it. No essays, no feature tours, no design notes.

```
[code block]

Skipped: <what was intentionally omitted>
Add when: <measurable trigger condition>
```

**If the explanation is longer than the code, delete the explanation.** The code IS the explanation. Comments inside the code handle the "why." The external summary handles only what was NOT built.

**Exceptions — when longer explanation IS warranted:**
- The user explicitly asked for an explanation
- An architectural decision with non-obvious tradeoffs (the code alone doesn't convey it)
- A breaking change that downstream consumers need to understand
- A security-relevant decision where the reasoning IS the safety mechanism

**What this replaces:**
- Do NOT write a paragraph describing what the code does (the code says that)
- Do NOT list every function added (the diff shows that)
- Do NOT include benchmark numbers unless requested or the improvement was the stated goal
- Do NOT explain why you used a for-loop instead of a list comprehension (the ladder already decided that)

**What this does NOT apply to (explicit carve-outs):**
- **Commit messages** — These follow [Section 15](skills/15-git-workflow.md)'s detailed WHY format (problem → solution → context). Commit messages are not "output" — they're permanent project history.
- **User-requested explanations** — If the user asks "why did you do X?", answer fully.
- **Security decisions** — Safety override. If omitting the explanation could cause someone to reverse the security measure later, explain it.
- **Architectural decisions in DEEPDIVE.md** — These need full context for future agents.
- **When the next developer would need to understand constraints NOT visible in the code** — e.g., "we use O(n²) here because N is always < 100."

### 50.5 Over-Engineering Review Vocabulary

When reviewing code (your own or others), use this standardized vocabulary to flag complexity that should be removed. Each finding is one line:

```
L<line>: <tag> <what was found>. <what to replace it with>.
```

**Tags:**
| Tag | Meaning | Example |
|-----|---------|---------|
| `delete:` | Dead code, unused flexibility. Remove entirely. | `L42: delete: unused fallback path for Python 3.8. Remove the entire try/except block.` |
| `stdlib:` | Hand-rolled version of something in the standard library. | `L15: stdlib: custom slugify function. Use pathlib.Path.stem or re.sub with str.lower.` |
| `native:` | Code doing what the platform already does. | `L28: native: custom form validation logic. Use HTML5 constraint validation API (checkValidity, setCustomValidity).` |
| `yagni:` | Abstraction with one implementation, config nobody sets, layer with one caller. | `L55: yagni: IEmailSender interface with single SmtpSender implementation. Inline the class.` |
| `shrink:` | Same logic, fewer lines. | `L67: shrink: 12-line dict merge. Use {**a, **b}.` |

**Review ends with a net line:**
```
Net: -23 lines possible (4 findings).
```

**When to use this vocabulary:**
- During self-review before marking a task complete
- When reviewing AI-generated code for bloat
- During code review of any PR

### 50.6 Honesty Boundaries — What Agents MUST NOT Claim

Prevent agents from making invalid or misleading claims. These are NOT optional.

**NEVER print per-repo savings numbers** (e.g., "you saved 47 lines here"):
- The unbuilt version was never written, so there is no real baseline
- Claiming savings against imaginary code is hallucination, not measurement
- The decision ladder prevents code from being written — there's nothing to measure against

**NEVER claim something "improves performance" without measurements:**
- "Should be faster" is speculation, not engineering
- Show before/after measurements OR don't make the claim
- If the performance change is irrelevant (1μs difference), don't mention it

**NEVER claim "100% test coverage" based on line coverage alone:**
- Line coverage ≠ behavioral coverage (see [Section 40.5](skills/40-code-coverage-enforcement.md))
- Branch coverage + mutation score are the minimum for strong claims

**NEVER say "bug fix" when you changed behavior without confirming the old behavior was wrong:**
- State what changed and why
- Let the changelog categorize it
- "Bug fix" implies a confirmed defect; "behavior change" is the honest description when uncertain

### 50.7 Tests Are Not Bloat

The minimalism ladder exempts tests. A test is not bloat — it's the discipline that makes minimalism safe to practice.

**Rules:**
- **One runnable check per non-trivial function.** An `assert` statement, a one-function test, a small script. No test frameworks required. No fixtures. Just prove the code works.
- **Trivial one-liners need no test.** `def get_timestamp(): return time.time()` — skip it.
- **Measure test burden separately.** Track `wrote_tests_rate` but do not count tests against "lines of code" metrics. Tests are infrastructure, not bloat.
- **Every security-critical path MUST have a test.** Even if it's small. Especially if it's small.

```python
# A one-runnable-check — no framework, no class, no fixture
def test_divide_by_zero_returns_none():
    assert safe_divide(10, 0) is None
    assert safe_divide(10, 2) == 5

# Run with: python -c "from tests.test_math import test_divide_by_zero_returns_none; test_divide_by_zero_returns_none()"
```

### 50.8 Self-Referential Governance

The AGENTS.md file itself is subject to its own rules. This is not a meta observation — it's a design constraint.

**Agents working on AGENTS.md MUST:**
- Apply the decision ladder to every addition (does this section need to exist?)
- Use tradeoff comments for any intentional gaps
- Follow the same commit conventions, PR templates, and quality gates
- Never add sections that future agents would need to explain away ("we don't follow Section X because...")

**Before adding a new section, ask:**
- Is this pattern already covered by an existing section? (merge, don't duplicate)
- Will this age well? (avoid sections tied to specific tool versions or transient trends)
- Does this section reduce ambiguity or add it? (every rule should eliminate a real failure mode)

---

