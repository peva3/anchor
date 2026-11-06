---
name: skill-69-bug-diagnosis-loop
description: "Section 69 — Bug Diagnosis Loop. Load when debugging a failure, intermittent issue, regression, or any bug without a known cause."
---
# Skill 69: Bug Diagnosis Loop

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 69. Bug Diagnosis Loop

Debugging is not reading code and guessing. It is building a loop that reliably reproduces
the failure, then changing one variable at a time until the cause is proven.

### 69.1 Build the Loop Before the Theory

**The first deliverable is a command that goes red on this exact bug.** Not a hypothesis,
not a patch — a repeatable observation of the failure.

- The loop must fail **now**, for the reported reason, on your machine.
- If you cannot make it fail, you cannot know you fixed it.
- **No red-capable command → stop and say so.** Report what you tried, what you observed,
  and what you need (a repro, logs, access, a trace). Do not proceed to speculative edits.

A loop is worth more than a strong opinion: it turns "I think it's the cache" into
"removing the cache key makes the test pass."

### 69.2 Pick a Loop Type

| Loop | Use when | Minimum shape |
|------|----------|---------------|
| **Failing test** | The bug is in code you can call | One test, exact input, asserts the wrong behavior |
| **HTTP request** | The bug is in an endpoint | `curl` against a local server, assert status/body |
| **CLI snapshot** | The bug is in output formatting | Run the command, diff the output |
| **Headless browser** | The bug is in a user flow | Playwright script, assert visible outcome |
| **Replay trace** | The bug needs recorded production traffic | Replay the payload through the same path |
| **Throwaway harness** | The real entry point is too heavy | Smallest program that exercises the failing unit |
| **Property / fuzz** | The bug is an input-shape edge case | Generator that shrinks to a minimal case |
| **Bisection** | The bug appeared somewhere in history | `git bisect` with an automated good/bad check |
| **Differential** | Two implementations disagree | Run both, compare outputs on the same input |
| **Human-in-the-loop** | The bug needs a device, account, or UI judgement | Scripted steps with an explicit expected observation |

Prefer the cheapest loop that is **sharp** (fails only for this bug) and **fast** (seconds,
not minutes). A slow, noisy loop gets abandoned.

### 69.3 Tighten the Loop

- **Faster** — cut network, seed data, run one test with `-k`.
- **Sharper** — assert the exact symptom, not "no exception".
- **More deterministic** — fix the clock, seed the RNG, pin the timezone, isolate the port.
- **Non-deterministic bug** — raise the reproduction rate before theorising: loop 1,000
  times, stress the scheduler, replay the race. A 1-in-100 bug is diagnosable; a 1-in-10,000
  bug needs a better harness first.

### 69.4 Reproduce and Minimise

1. Confirm the loop fails with the reported input.
2. Remove everything not required to fail: fields, steps, config, data.
3. Keep the smallest input that still fails. That input usually names the cause.

### 69.5 Form Falsifiable Hypotheses

Write **3–5 hypotheses**, each with a prediction that can be checked:

```markdown
H1: The cache key ignores the tenant ID.
    Predicts: two tenants with the same slug share a cached response.
    Check: request tenant A then tenant B with the same slug.
H2: The query parameter is parsed as a number before validation.
    Predicts: "01" works, "1x" throws.
    Check: send both.
```

Show the list to the user when the bug is high-risk or the search is expensive. Rank by
likelihood × cost to test. Do not test them all at once — then you learn nothing about
which one was true.

### 69.6 Experiment One Variable at a Time

- Change one thing, re-run the loop, record the result.
- **Debugger beats logs** for state you can pause on; use logs for timing and production.
- **Tag temporary logs** with a unique marker (`[DEBUG-a4f2]`) so cleanup is a single grep.
- **Production regression: revert first, diagnose second.** Restoring service beats
  understanding the bug; investigate with the pressure off
  ([Section 59](skills/59-incident-response-and-runbooks.md)).
- Do not "fix" by widening a catch, retrying, or deleting the assertion. That hides the
  symptom and leaves the cause.

### 69.7 Leave a Regression Test at the Right Seam

- The regression test belongs at the **lowest seam that still fails** for this bug
  ([Section 71](skills/71-codebase-design-deep-modules.md)).
- It must fail on the old code and pass on the new code; verify both, in that order.
- If there is no seam where the bug can be tested, **that is the finding**: the design
  hides the failure. Record it and add the seam before or with the fix
  ([Section 8](skills/08-testing-requirements.md)).
- For flaky bugs, the test must be deterministic — not a `sleep`
  ([Section 45](skills/45-flaky-test-management.md)).

### 69.8 Clean Up and Name the Cause

- [ ] Remove tagged debug logs (`grep -rn "DEBUG-a4f2"`).
- [ ] Remove throwaway harnesses, fixtures, and feature flags used for diagnosis.
- [ ] Keep the regression test.
- [ ] Name the winning hypothesis in the commit message and PR: "fix: cache key omitted
      tenant ID, causing cross-tenant reads".
- [ ] Note the failed hypotheses only if they explain a near miss.

### 69.9 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Patch before repro** | You cannot prove the fix | Build the red loop first |
| **Shotgun edits** | Several changes hide which one worked | One variable at a time |
| **Log-and-pray** | No prediction, no learning | Falsifiable hypothesis first |
| **Fixing the symptom** | The cause returns | Name the cause in the commit |
| **Deleting the test** | Converts a bug into a blind spot | Fix the code, keep the test |
| **No cleanup** | Debug logs and harnesses ship | Grep the tag before commit |

### 69.10 Verification

- Does the loop fail before the fix and pass after?
- Is the cause named in one sentence, with evidence?
- Is the regression test at the lowest seam that reproduces it?
- Are debug artefacts gone and the suite green?

---

## References

- Matt Pocock, `diagnosing-bugs` skill — https://github.com/mattpocock/skills
- [Section 24.11](skills/24-common-failure-modes.md) — diagnose before patching
- [Section 8](skills/08-testing-requirements.md) — test-first and regression tests
- [Section 59](skills/59-incident-response-and-runbooks.md) — revert first in production
- [Section 71](skills/71-codebase-design-deep-modules.md) — seams make bugs testable
