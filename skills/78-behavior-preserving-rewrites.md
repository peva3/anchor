---
name: skill-78-behavior-preserving-rewrites
description: "Section 78 — Behavior-Preserving Rewrites. Load when porting, migrating, or reimplementing a working system without changing observable behavior."
---
# Skill 78: Behavior-Preserving Rewrites

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 78. Behavior-Preserving Rewrites

A rewrite is risky because it fails quietly: the new code compiles, the happy path passes,
and a changed edge case ships. The work is not translation — it is proving equivalence
against the system that already runs.

### 78.1 When This Applies

- Porting a module or service to another language or runtime.
- Reimplementing a library, parser, or engine behind the same interface.
- Replacing a subsystem incrementally (strangler pattern).
- Rewriting for performance while the observable contract must not move.

**Not this section:** a rewrite that also changes requirements. That is a new specification
([Section 68](skills/68-spec-and-ticket-decomposition.md)) and the old behavior is not the
reference. Greenfield work has nothing to preserve.

### 78.2 Record the Original Before Writing the Replacement

The recording is the specification. Build it from four sources, in this order:

1. **Existing tests** — import their inputs and expected results rather than re-deriving them.
2. **Generated edge cases** — empty, null, zero, negative, maximum, boundary, duplicate,
   malformed, and unusually large inputs.
3. **Semantic traps** — Unicode, case folding, collation, time zones, numeric precision,
   overflow, and ordering.
4. **Real inputs** — sampled production shapes with secrets and PII removed.

Write the cases to a reviewable file (`cases.jsonl` or a table) with the input, the expected
result, and the source of the expectation. Run it against the **original** first: a recording
that fails on the original is a bad recording, not a bug to port.

### 78.3 Port One Unit at a Time

- Choose the smallest callable unit, not the smallest file.
- Keep the public API stable; callers should not change during the port.
- The original stays runnable as the reference until the gate passes.
- Do not rewrite a caller and its callee in the same step; you lose the ability to tell
  which change caused a mismatch.

### 78.4 A Mismatch Is a Behavior Difference

**Fix the port, never the recording.** Editing the expectation to match the new output
deletes the evidence.

Intentional differences are recorded, not hidden:

```json
{"fn": "format_price", "args": [1299, "USD"], "actual": "$12.99", "reason": "drops trailing zero per new design"}
```

- Keep known differences in `known-diffs` with a reason and an owner.
- The gate fails when a known difference disappears, so stale exceptions cannot accumulate.
- Numeric tolerance is a decision, not a convenience: exact for integers and strings;
  floats only with explicit user consent and a stated epsilon. Never widen tolerance to
  make a mismatch pass.

### 78.5 Record Effects, Not Just Output

Two implementations can return the same value and behave differently: one sends an email,
writes a row, appends a log, or calls a third party twice. Matching output is not matching
behavior.

- Record side effects alongside return values: writes, messages, external calls, ordering,
  and duplicate suppression.
- A rewrite that produces the right answer and an extra side effect is a regression.
- Where effects cannot be observed directly, record them at the boundary (queue, outbox,
  test double) rather than inferring them from the return value.

### 78.6 Stale Recordings and Stalled Ports

- **Original changed?** Re-record before porting further. A stale recording certifies the
  wrong behavior.
- **No progress?** Three edits with no new matching case means stop. Show the remaining
  mismatches and ask: is a rule missing from the recording, or should this function stay in
  the original? Continuing to guess is how a port drifts.
- Keep a coverage map of ported, verified, and still-original units so scope is visible.

### 78.7 Shadow, Enable, Disable

Run the port beside the original before trusting it:

1. **Shadow** — send real or replayed traffic to both, compare results and effects, and
   report mismatches without changing what callers see.
2. **Enable** — switch the call site only after the shadow run is clean.
3. **Disable** — keep a revert path that restores the original byte-for-byte.

Ask before editing the original's call sites or deleting it. A port that cannot be turned
off is a one-way door ([Section 35.5](skills/35-pr-description-format-template.md)).

### 78.8 The Equivalence Gate

Do not call the port done until all of these hold:

- [ ] Every exported symbol exists with the same signature and error contract
- [ ] Every recorded case matches, or is listed in `known-diffs` with a reason
- [ ] Every deliberate failure is reached by a failing case, not assumed
- [ ] No `unimplemented`, stub, or panic where the original returned an error
- [ ] Side effects match, including count and order
- [ ] Language-appropriate lint and format pass, warnings treated as errors
- [ ] Unsafe or FFI blocks carry a safety justification
- [ ] Performance is within the agreed factor, measured on the same workload
- [ ] Size is proportionate — a port several times the original's size needs a reason
- [ ] The shadow run is clean and the revert path is tested

### 78.9 Language and Runtime Traps

| Trap | What changes | Check |
|------|--------------|-------|
| **String indexing** | UTF-16 vs UTF-8 vs bytes; grapheme clusters | Slice at the same logical boundary |
| **Numbers** | Integer width, overflow, float formatting, `-0` | Boundary and round-trip cases |
| **Error mapping** | Exception types, messages, exit codes | Same category and actionable text |
| **Unicode** | Case folding, normalization, collation | Accented, emoji, and RTL inputs |
| **Map ordering** | Insertion vs sorted vs hash order | Cases that depend on iteration |
| **Regex** | Engine-specific syntax, greediness, Unicode classes | Port each pattern with tests |
| **Null/undefined** | Absent, empty, and falsy are three states | Distinguish all three |
| **Time** | Zones, DST, leap seconds, monotonic vs wall clock | Fixed clocks and zone boundaries |
| **Concurrency** | Ordering, atomicity, retries, idempotency | Effects under interleaving |
| **FFI/layout** | Struct padding, ownership, lifetime | Round-trip through the boundary |

### 78.10 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Port now, test later** | The recording becomes whatever the port does | Record first ([78.2](#782-record-the-original-before-writing-the-replacement)) |
| **Updating expectations to pass** | Erases the behavior difference | Fix the port ([78.4](#784-a-mismatch-is-a-behavior-difference)) |
| **Big-bang rewrite** | No reference, no rollback, no diagnosis | One unit, shadow, revert ([78.3](#783-port-one-unit-at-a-time)) |
| **Output-only equivalence** | Misses duplicate effects | Record effects ([78.5](#785-record-effects-not-just-output)) |
| **Widening float tolerance** | Hides a real mismatch | Exact, or a stated epsilon with consent |
| **Deleting the original early** | Removes the only oracle | Keep it until the gate passes |
| **Stale cases** | Certifies yesterday's behavior | Re-record after any original change |

### 78.11 Verification

- Does a recording exist, and did it pass against the original before any port code?
- Was the work done in units small enough to attribute a mismatch?
- Is every non-matching case either fixed or in `known-diffs` with a reason?
- Were side effects compared, not just return values?
- Did the shadow run complete, and is the revert path tested?
- Does the equivalence gate pass in full, including lint, exports, and performance?

---

## References

- erkamyaman, `rust-anything` — https://github.com/erkamyaman/rust-anything
