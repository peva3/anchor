---
name: skill-74-design-systems-and-visual-craft
description: "Section 74 — Design Systems & Visual Craft. Load when building or restyling a UI surface, choosing type/colour/spacing, or judging whether a rendered design is finished."
---
# Skill 74: Design Systems & Visual Craft

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 74. Design Systems & Visual Craft

[Section 63](skills/63-ui-quality-and-anti-slop-guardrails.md) says what a surface must not
fake. This section says what to build it from and how to judge the rendered result. It is
stack-agnostic: the rules apply to CSS, Tailwind, SwiftUI, Compose, or a canvas.

### 74.1 Name the Surface Mode

Choose the mode per **surface**, not per product. A marketing page and the dashboard behind
it are different modes even when they share a brand.

| Mode | Surfaces | Default posture |
|------|----------|-----------------|
| **Persuade** | Landing, pricing, launch, campaign | One action, bold hierarchy, deliberate pacing |
| **Operate** | Dashboard, admin, editor, internal tool | Density, precision, stable layout, fast scanning |
| **Read** | Docs, blog, report, changelog | Measure 60–75 characters, quiet rhythm, linked structure |
| **Experience** | Portfolio, game, immersive story | Motion and media earn their place; performance is part of the design |

- State the mode in `DESIGN.md` before choosing colours or type.
- A screen may borrow a second mode, but one is dominant. Mixed modes are a decision, not a default.
- **Operate and Read fail loudly, Persuade fails quietly.** A slow dashboard or an unreadable
  doc is a defect; a landing page that merely underwhelms is a critique item.

### 74.2 Tokens Are the Contract

Every visual value comes from a token defined once. Components consume tokens; they do not
invent values.

- **Colour, type, space, radius, shadow, and motion** each live in one token block
  (`:root`, a theme file, or the platform equivalent).
- **No literal colour, font family, or spacing value outside the token block.** A `#hex`,
  `font-family: "Inter"`, or `padding: 13px` in a component is a defect, not a shortcut.
- **Named text styles, not ad-hoc sizes.** Define `Heading 1` … `Caption` from one scale and
  use the names. A surface that needs an eighth heading size needs fewer headings.
- **One spacing scale.** Pick a base (4 or 8) and use multiples; do not add a value because
  one gap looked wrong.
- **Radius composes.** When a child sits inside a parent with a gap smaller than 32px, set
  `inner radius = outer radius − gap` (never below 2px). Equal radii on nested boxes look
  wrong at every size.
- **Adding a token is a design decision.** Add it with a name and a reason in `DESIGN.md`;
  never inline the value and call it a one-off.

A token audit is mechanical: grep the source for colour literals and font stacks outside the
token file. If the grep finds them, the design system is not real yet.

### 74.3 Declare the Material Inventory

Before laying out a surface, list what you actually have for each content slot:

| State | Meaning | Layout consequence |
|-------|---------|--------------------|
| **Real** | Supplied by the user, a real dataset, or the repo | Use it, including its awkward length |
| **Pictures** | Supplied imagery that carries mood, not claims | Use as texture; never as evidence |
| **Absent** | Nothing supplied | Design for absence — omit, or use a typographic substitute |

- **An unsupplied number, quote, logo, testimonial, avatar, or screenshot is absent.** It is
  not an invitation to invent one ([Section 63.1](skills/63-ui-quality-and-anti-slop-guardrails.md)).
- Real content sets the layout: test the longest name, the empty table, the one-item list.
- A stock photo is "pictures", not "real". It cannot stand in for a product screenshot or a
  customer logo.
- Record the inventory in the task notes or `PRODUCT.md`. It is the first thing a reviewer
  should be able to check.

### 74.4 Structure Follows the Job

- **Name the visitor's one action** — start a trial, find a record, read the reference, play
  the demo. If you cannot name it, the page has no job.
- **Read the anatomy from the category**, then decide what this instance needs. A pricing
  page, a changelog, and a case study have different natural shapes.
- **End the page on the action.** The last screen should not be a unrelated newsletter band.
- **Do not default to figures → steps → testimonial → email capture** because it is the
  template you have seen most. That sequence is a result of a specific argument, not a law.
- **Mirror test:** imagine a neighbouring prompt — a different product in the same category.
  Would it produce this exact section order, hero, and card grid? If yes, change one
  structural decision and say why.

### 74.5 Hard Floor, Reflex, and Finish

Separate rules by what they are allowed to block:

| Tier | Meaning | Examples |
|------|---------|----------|
| **Floor** | Never ships | Contrast below AA, unlabeled controls, broken focus, invented content, dead buttons, unreadable measure |
| **Reflex** | Default; waivable on record | Centered hero, three-card feature grid, eyebrow label, one accent gradient, rounded-2xl everywhere |
| **Finish** | Never blocks; do when cheap | Optical alignment, hover polish, consistent icon stroke, last 2px of spacing |

- A **Reflex** waiver is written down: "used a centered hero because the product has one
  message and no visual material; revisit when screenshots exist."
- A **Floor** item is not waivable. Fix it or do not ship.
- Do not spend a review on **Finish** while a **Floor** item is open.

### 74.6 Refused Defaults

These read as generated because they are the model's most likely continuation. Refuse them
by default; if one is genuinely right, name the reason in the change.

| Default | Why it reads generic | Do instead |
|---------|----------------------|------------|
| Gradient text | Decoration standing in for hierarchy | Solid token colour; earn emphasis with size or weight |
| Purple-to-blue gradient | The default "AI product" palette | Choose a palette from the material or brand |
| Card inside a card | Depth without meaning | One surface; use spacing for grouping |
| Icon + tile + heading as page structure | Turns every section into the same object | Let content choose its own shape |
| Hero metric template | Number without a decision attached | State the decision, then the evidence |
| Section numbers 01 / 02 / 03 | Order that carries no information | Remove, or use real sequence only when order matters |
| Eyebrow above every heading | Adds a label nobody needs | Let the heading do the work |
| Emoji as icons | Platform-dependent, tone-deaf in Operate | One icon set with consistent stroke |
| Glass / blur as decoration | Costs contrast and performance | Solid surface with a real elevation token |
| Hard offset shadows | Fashionable, not hierarchical | One elevation scale, used sparingly |
| Monospace as costume | Signals "technical" without being code | Monospace for code and data only |
| Tracked-caps labels everywhere | Shouts; hurts readability | Sentence case at normal tracking |
| Decorative status dots | Implies live state that does not exist | Real status text, or nothing |
| Same-size card grid for everything | Flattens unequal importance | Vary size by importance, or use a list |
| Modal for a non-interrupting task | Steals focus for no reason | Inline panel or progressive disclosure |

A refused default is not a ban. It is a claim that must be justified, the same way a
`# ponytail:` shortcut names its ceiling ([Section 50.2](skills/50-intentional-minimalism-the-simplicity-first-architecture.md)).

### 74.7 Copy Is Part of the Design

- **The headline says what it is and who it is for.** Cleverness that hides the offer is a
  Floor problem, not a tone preference.
- **One primary call to action, labeled with a verb.** "Start free trial", not "Learn more"
  as the only path.
- **No lorem ipsum, no placeholder claims, no invented metrics.** See the material inventory.
- **Error and empty copy tells the user the next action** ([Section 63.3](skills/63-ui-quality-and-anti-slop-guardrails.md)).
- **Copy length is a layout constraint.** Test the longest real string, not the shortest
  placeholder.
- Read the page aloud once. If a sentence exists only to fill a slot, delete the slot.

### 74.8 The Ship Checklist

Run this against the rendered surface, not the source:

- [ ] Stated mode and material inventory match what is on screen
- [ ] No colour, font, or spacing literal outside the token block
- [ ] Renders at 320, 768, and 1440 without overlap or clipped text
- [ ] Keyboard-only pass: visible focus, logical order, no traps
- [ ] Zoom to 200%: no content lost
- [ ] Reduced-motion preference respected
- [ ] Every control does something ([Section 63.2](skills/63-ui-quality-and-anti-slop-guardrails.md))
- [ ] Loading, empty, error, and success states exist ([Section 63.3](skills/63-ui-quality-and-anti-slop-guardrails.md))
- [ ] Contrast and labels pass WCAG AA ([Section 63.4](skills/63-ui-quality-and-anti-slop-guardrails.md))
- [ ] No refused default survived without a written reason
- [ ] `DESIGN.md` reflects every token and component used

### 74.9 PRODUCT.md and DESIGN.md

Two short living documents prevent design drift:

```markdown
# PRODUCT.md
Audience: <who this is for>
One action: <the action the surface exists to cause>
Constraints: <brand, legal, platform, performance>
Non-goals: <what this surface deliberately does not do>
Material: <real | pictures | absent, per slot>
```

```markdown
# DESIGN.md
Mode: <Persuade | Operate | Read | Experience>
Tokens: <colour, type, space, radius, shadow, motion — the actual values>
Type scale: <named styles and sizes>
Components: <name, purpose, states>
Motion: <what moves, why, and the reduced-motion fallback>
```

- Read both before changing a UI surface.
- Update them **in the same commit** as the change that invalidates them. A token added in
  code and missing from `DESIGN.md` is drift.
- A component that exists only in one screen is a pattern waiting to drift; name it or inline it.
- For a small project, one file with two sections is enough. The point is that the values
  are written once.

### 74.10 Prefer Deterministic Detection

Prose review misses what a tool catches every time. Before handing off a UI change:

| Check | Catches | Typical tool |
|-------|---------|--------------|
| Token/style lint | Literal colours, unknown tokens, duplicate values | stylelint, custom grep |
| Accessibility scan | Contrast, labels, landmarks, focus order | axe, pa11y, Lighthouse |
| Rendered screenshots | Overflow, overlap, layout shift | Playwright screenshots |
| Link check | Dead navigation and CTAs | [Section 37](skills/37-pre-commit-hook-standards.md) hooks |
| Content check | Lorem ipsum, placeholder text, empty alts | grep / lint rule |

- Fix every FAIL. A waiver records the reason and the owner.
- If a rule can be checked mechanically, add the check instead of another paragraph
  ([Section 52](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md)).
- Say what the checks cannot see: taste, hierarchy, and whether the page has a job.

### 74.11 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Inventing content to fill a layout** | Ships false claims | Declare the slot absent and design for it |
| **Tokens in name only** | Literals creep back and drift | Mechanically forbid literals outside the token file |
| **One mode for the whole product** | Marketing boldness in a dashboard, or dashboard density on a landing page | Choose mode per surface |
| **Copying the category's default page** | Every competitor looks the same | Run the mirror test and change one decision |
| **Finishing before the floor** | Polished but inaccessible | Fix Floor items first |
| **Prose-only quality review** | Misses what a linter catches deterministically | Run the mechanical checks |
| **DESIGN.md updated "later"** | Never updated; becomes fiction | Update in the same commit |

### 74.12 Verification

- Is the surface mode stated, and does the design match it?
- Are all visual values tokens, with no literals outside the token block?
- Is the material inventory recorded, and is every unsupplied slot absent rather than invented?
- Does the page name and end on one action?
- Did a refused default survive without a written reason?
- Did the mechanical checks run, and is every waiver recorded?
- Are `PRODUCT.md` and `DESIGN.md` current as of this change?

---

## References

- Paul Bakaus, `impeccable` — https://github.com/pbakaus/impeccable
- Nutlope, `hallmark` — https://github.com/Nutlope/hallmark
- elayadesign, `ai-design-skills` — https://github.com/elayadesign/ai-design-skills
