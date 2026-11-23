---
name: skill-79-design-verification-and-motion
description: "Section 79 — Design Verification & Motion. Load when reviewing or finishing a rendered UI surface, auditing motion, or adapting a third-party component."
---
# Skill 79: Design Verification & Motion

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 79. Design Verification & Motion

Building a design system ([Section 74](skills/74-design-systems-and-visual-craft.md)) and
keeping it honest ([Section 63](skills/63-ui-quality-and-anti-slop-guardrails.md)) are not the
same as verifying the rendered result. This section is the proof step: what was measured, what
was judged, and what still fails.

### 79.1 Measured vs Judged

Separate what a script can prove from what a person decided. Never present the second as the
first.

| Measured | Judged |
|----------|--------|
| Contrast ratios per role pair | Mood and atmosphere |
| Motion safety and reduced-motion behavior | Reference fit and originality |
| Glyph coverage for the declared languages | Brand voice |
| Font licence and tabular figures | "Looks AI-made" |
| Logo legibility at 16 and 32 px | Hierarchy and emphasis |
| Console errors, blank canvases, overflow | Whether the page does its job |

State the split in the report: "Contrast matrix: 18 pairs, all pass. Taste: one reviewer, not a
measurement." A number with no method is worse than an honest judgment.

### 79.2 The Contrast Matrix

One spot check is not a contract. Enumerate every foreground/background role pair the interface
actually uses, and label what each pair is allowed to do:

| Role pair | Use | Floor (WCAG AA) |
|-----------|-----|-----------------|
| body text on surface | text | 4.5:1 |
| muted text on surface | text | 4.5:1 |
| link on surface | text | 4.5:1 |
| button label on button | text | 4.5:1 |
| border on surface | UI component | 3:1 |
| focus ring on surface and on control | UI component | 3:1 |
| disabled text on surface | decorative, but must stay readable | 3:1 |
| icon on surface | graphics | 3:1 |
| large heading on surface (≥24 px, or ≥18.66 px bold) | large text | 3:1 |

- **Solve the palette, do not sample it.** Adjust lightness (OKLCH keeps hue and chroma stable)
  until every pair clears its floor by construction; then the matrix is a verification, not a
  repair.
- **Record the matrix** with the token values and labels in `DESIGN.md`
  ([Section 74.9](skills/74-design-systems-and-visual-craft.md)). Re-run it whenever a token
  changes; a palette edit invalidates the old result.
- **Contrast certifies legibility, not taste.** Passing every pair says nothing about whether the
  page is any good. Say so.

### 79.3 Render, Score, Revise

Verification is a loop, not a single pass:

1. **Render the real surface** headless at 390, 768, 1024, and 1440 px
   ([Section 74.8](skills/74-design-systems-and-visual-craft.md)). Markup that was never rendered
   is not done.
2. **Score it** against the project's rules: failed checks, failed contrast pairs, tells found,
   motion violations, console errors, blank regions, overflow. A 0–100 score is fine if the
   weights are written down; a count of blocking failures is simpler and harder to game.
3. **Revise below threshold, then re-render.** The threshold is the project's; the default is
   "no fixable FAIL remains". Do not lower the threshold to pass.
4. **Stop after three rounds** and report the score, the rounds used, and what remains. A fourth
   round usually means the structure is wrong, not the spacing.

The point is not the number. An enforced loop changes delivery in a way prose does not: in
styleseed's published comparison, raw rules alone moved two models in opposite directions
(+1.6 and −3.7 points), while the enforced render-and-revise gate improved both by about 5.3
points across 120 rendered cells. Treat that as their measurement on their task, not a universal
effect size — but do not replace the loop with a paragraph.

### 79.4 Tells Scan

A banned-pattern table does not scan anything. Run a search over the project and report
`file:line` for each tell:

| Tell | Why it reads as generated |
|------|---------------------------|
| Numbered eyebrow above a heading (`01 — About`) | Decorative sequence with no meaning |
| Three equal cards as the default section | Structure chosen before content |
| Hero metric pulled from nowhere | Invented proof |
| `01 / 02 / 03` section labels | Same, at page scale |
| Invented `ESTD. 2018` or founding year | Fabricated fact ([Section 63.1](skills/63-ui-quality-and-anti-slop-guardrails.md)) |
| Gradient text; purple-to-blue gradients | Default palette, not a brand decision |
| Emoji as icons; icon + tile + heading cards | Placeholder visual language |
| Glass, blur, or glow as decoration | Effect before reason |
| Same-size card grid for unequal content | Template over hierarchy |
| Placeholder copy or a fake logo strip | Unfinished content shipped as real |
| Decorative status dots with no state | Noise that looks like data |

Report counts and locations, fix them or waive each with a reason. Then run the mirror test from
[Section 74.4](skills/74-design-systems-and-visual-craft.md): would a neighbouring prompt produce
this same combination? If yes, change one structural decision.

### 79.5 Motion Audit

Motion is part of the interface, not a finishing layer. Durations and easings are tokens
([Section 74.2](skills/74-design-systems-and-visual-craft.md)); ad-hoc milliseconds and
`cubic-bezier()` values outside the token block are a finding.

Flag and fix:

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| `transition: all` | Animates properties nobody intended, including layout | Name the properties |
| `ease-in` for UI feedback | Starts slow; the response feels late | Use the token for enter/exit |
| `scale(0)` entrances | Content appears from nothing; no spatial origin | Start near the final scale |
| UI feedback slower than ~300 ms | Reads as lag, not polish | Shorten; reserve long timings for narrative |
| Animating `width`, `height`, `top`, `left` | Layout thrash and jank | Transform or grid/flex techniques |
| Hover motion without pointer gating | Fires on touch and on keyboard focus | Gate with `@media (hover: hover)` |
| Missing `prefers-reduced-motion` | Ignores an accessibility setting | Provide a reduced variant |
| Parallax or scroll-jacking | Hijacks navigation | Remove, or make it opt-in |
| Autoplay longer than ~5 s | Traps attention; often unstoppable | Pause control or no autoplay |

Reduced motion must keep the **function**: replace movement with opacity or an instant state
change, do not remove the feedback entirely. Motion should communicate state or space; if it
communicates neither, delete it.

Run the audit against the rendered page, not the source alone — a library can inject transitions
you never wrote.

### 79.6 Adapting Third-Party Components

A copied component is a dependency with a visual contract. Before adopting it:

- **Inherit the project's palette, spacing, and type.** Replace hardcoded hex, px, font families,
  radii, and shadows with tokens.
- **Preserve behavior:** `prefers-reduced-motion`, pause when `document.hidden`, CSS and JS
  namespacing, semantic HTML, focus handling, and keyboard operation.
- **Minimise dependencies.** Remove unused variants and the animation library if one transition
  remains.
- **Check the licence** and keep the required attribution.
- **Never redraw a logo or screenshot.** Use the supplied file
  ([Section 74.3](skills/74-design-systems-and-visual-craft.md)).
- **Verify after adaptation:** contrast pairs still pass, motion audit still passes, the component
  still works with the keyboard and at 200% zoom.

### 79.7 Identity Assets

Only when the task produces a logo, wordmark, type system, or palette — not for ordinary UI work.

- Present **2–3 distinct directions** and stop. The human chooses; never auto-pick.
- At least one direction must avoid the model-default tells in 79.4.
- Gate each direction on measurement:
  - contrast for every text/background pair it introduces;
  - colour-blindness simulation (deuteranopia, protanopia, tritanopia);
  - glyph coverage for every language the brand actually uses;
  - font licence that permits the intended use;
  - tabular figures if the brand shows numbers in tables or prices;
  - a render at 16 and 32 px, where logos actually live.
- A failed measurement blocks the set; a heuristic concern is a warning; taste is a judgment.
- **Trademark clearance is out of scope.** Say so; do not imply the name or mark is cleared.

### 79.8 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Taste reported as measurement** | Unfalsifiable and misleading | Label measured vs judged (79.1) |
| **One-pair "matrix"** | Misses the pair that ships | Enumerate every role pair (79.2) |
| **Scored once, never re-rendered** | The fix is unverified | Loop until threshold (79.3) |
| **Motion checked by eye** | Misses injected transitions and reduced-motion | Audit the rendered page (79.5) |
| **Copied component with hardcoded values** | Breaks theming and drift | Adapt to tokens (79.6) |
| **Auto-picked identity** | Removes the human decision that matters | Present options and stop (79.7) |
| **"Looks fine" with no render** | No evidence | Render, score, report |

### 79.9 Verification

- Does the contrast matrix cover every role pair, with labels and floors?
- Is the score recorded, with the threshold and the number of rounds?
- Does the tells scan report locations, not just a count?
- Did the motion audit run on the rendered page, including reduced-motion behavior?
- Does every adapted component inherit tokens and preserve keyboard, focus, and pause behavior?
- For identity work: were multiple directions shown, and did the human choose?
- Is every claim labeled measured or judged?

---

## References

- tastemaker — contrast matrix and motion audit: https://github.com/codeswithroh/tastemaker
- styleseed — enforced render/score/revise loop: https://github.com/bitjaru/styleseed
- genjutsu — tells field guide: https://github.com/AThevon/genjutsu
- brand-identity-skill — identity measurement gates: https://github.com/fatihaydost/brand-identity-skill
- forever-ai-components — adaptation rules: https://github.com/isas1/forever-ai-components
