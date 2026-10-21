# Skill 64: Skill Routing & Checkpoints

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 64. Skill Routing & Checkpoints

The always-loaded core (this entry point) is deliberately small. Everything else is loaded on demand. That only works if the agent *deliberately chooses* which skills are active — and re-checks that choice as the task moves. Loading nothing is a routing decision; so is loading everything.

### 64.1 Route at Task Start

Before the first edit, name the task type and load what matches.

1. **Read `routing.json` — always, every task.** It is the single source of routing truth and pairs with `AGENTS.md`: `AGENTS.md` states the guardrails, `routing.json` says which of them a given task loads. Never route from memory or from an impression of what seems relevant.
2. **Classify the task** — one of the task types in `routing.json` (fix, feature, refactor, test, review, docs, release, incident, ui, data, infra, security, deck, hackathon).
3. **Load the core set** — Sections 1, 2, and 36 are already inline and do not count against the budget; add any skill `routing.json` lists under that task type's `always` list.
4. **Load the matched skills** — the union of `always` and `skills` for the chosen task type.
5. **Cap it** — keep at most **7** task-scoped skills on top of the always-loaded core (Sections 1, 2, 36). If a task needs more, it is multiple tasks; split it.

**If `routing.json` is missing or unreadable, stop.** It ships beside `AGENTS.md`; restore it before working. Improvising a route from the Section Index alone is a guardrail failure, not a reasonable fallback — the index tells you what exists, only the map tells you what applies.

Routing is deterministic: the same request maps to the same skills. Do not invent a skill that isn't in the index, and do not skip one that plainly fits.

### 64.2 Re-check at Phase Boundaries

`routing.json` gives each phase an `add` and a `drop` list. Additions bring in what the boundary needs (testing and gates at verify, PR and commit rules at commit); drops remove what the boundary no longer needs — a planning-only skill such as the tech-stack playbook has no business occupying context while you are writing code. A dropped skill is genuinely unloaded: if a later step needs it again, load it again.

Re-evaluate the active set at every boundary:

| Boundary | Re-check question |
|----------|-------------------|
| **Plan → build** | Do the skills I picked actually cover the work I'm about to do? |
| **Build → verify** | Do I now need the testing/CI/security skills I skipped? |
| **Verify → commit** | Are commit, PR, and changelog skills active? |
| **Commit → done** | Is anything still active that no longer applies? |
| **Any direction change** | The user changed the goal — re-route from scratch. |

Also re-check when you discover the task is not what it looked like (a "docs fix" that becomes an API change is a re-route, not a footnote).

### 64.3 State a One-Line Checkpoint

At each boundary, emit exactly one line:

```
ROUTE: active=[02,15,27,45] dropped=[63] added=[40] why="moved from UI work into test hardening"
```

- **active** — skill numbers currently loaded
- **dropped** — skills that no longer apply, and they stop applying
- **added** — newly loaded skills
- **why** — the reason for the change, in a few words

No essay. One line, then continue working. If nothing changed, say so once (`ROUTE: unchanged`) rather than repeating it every turn.

### 64.4 Drop What No Longer Applies

A skill that stopped being relevant is context you are paying for on every request. When the work moves on — UI polish finished, migration applied, incident closed — drop the skill and say so. Keeping a stale skill active is how agents start applying rules to the wrong layer (for example enforcing the UI dials while editing a database migration).

### 64.5 Follow the Pointers

When a loaded skill points at another section, load that section's file. Guessing at what the referenced rule says is how contradictions get introduced. Every reference in `skills/` is a real link to a real file — follow it. See [Section 51](skills/51-instruction-architecture-context-economy-self-improvement.md) for why this matters for context economy.

### 64.6 When Routing Is Ambiguous

If two routes are plausible and you cannot tell which the user means:

1. Pick the **safer** route — the one with more verification, stricter security, or the smaller change.
2. Say which one you picked and why, in the checkpoint line.
3. Do not silently load both "just in case" — that defeats the budget.

**If nothing matches at all, that is a fallback, not a default.** A fallback means the map
has no vocabulary for this kind of work. Do not quietly treat it as `review` and carry on:

1. **Say it out loud** in the checkpoint: `ROUTE: fallback — no task type matched`.
2. **Ask the user which area this belongs to** if the answer changes which rules load
   (auth vs UI vs data are different guardrails). One short question beats loading the wrong set.
3. **If you cannot ask, take the safer route and name the assumption** — more verification,
   stricter security, smaller change — and say it was a fallback.
4. **Record the missing phrase** as a vocabulary gap ([Section 64.9](skills/64-skill-routing-and-checkpoints.md)) so the next run recognises it.
   A fallback that is never reported is a gap nobody can fix.

### 64.7 The Routing Map Is Data, Not Logic

`routing.json` at the repo root is a plain table: task type → trigger phrases → skills, plus the core set. It has no scoring, no weights, and no code. Both humans and agents read the same file, and the same request always resolves the same way. When you add a skill, add its route in the same change — a skill with no route is a skill nobody loads.

### 64.8 Verification

Before finishing a task, check the route, not just the code:

- [ ] Every skill you actually relied on was loaded, not guessed at
- [ ] No skill is still active that the finished work no longer touches
- [ ] Cross-references you followed resolved to real files
- [ ] The checkpoint line reflects the final state of the task

---

## References

- Routing map (shipped): `routing.json`
- Routing benchmark (local scratch): `tests/routing-benchmark.json`
- Section Index in `AGENTS.md` — every section, its trigger, and its file

### 64.9 Keep the Vocabulary Honest

The map fails in one specific way: the words you use do not appear in any trigger, so the task falls back to a default route. Fix the vocabulary, not the skill sets.

- **One owner per trigger.** If two task types claim the same word, routing depends on list order — that is luck, not design. Pick the type whose rules actually apply.
- **Prefer the phrase people type.** `presigned url`, `backup plan`, `error rate` beat abstract nouns. Whole-word matching means a truncated stem (`deprecat`) never fires.
- **Weak verbs never outrank a noun.** `fix`, `add`, `build`, `implement` are signals of intent, not of subject; list them under `weakTriggers`.
- **A fallback is a reported gap.** If a request matches nothing, note the phrase and add it — do not widen a type's `skills` to compensate.
- **Prune words that are too generic.** `button`, `command`, `retry`, `rewrite` each pulled unrelated work into the wrong type; a word that appears in every domain owns none of them.
- **Re-measure in bulk.** A phrase suite (short requests with expected types) finds in one run what project scenarios find one at a time.
