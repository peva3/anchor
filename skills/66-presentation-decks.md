# Skill 66: Presentation Decks

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 66. Presentation Decks

Decks are a deliverable like any other: they get tested (does it render, does it project, does the audience read it) and they get the honesty rules. A deck is not a place where unverified numbers become facts because the font is large.

### 66.1 Content Discipline

One idea per slide. If a slide needs a second idea, it needs a second slide.

| Constraint | Rule |
|------------|------|
| **Ideas per slide** | Exactly one claim, decision, or question |
| **Body type size** | Large enough to read at the back of the room — if you have to say "you probably can't see this," the slide is wrong |
| **Words per slide** | A headline plus a few supporting lines. Paragraphs belong in the speaker notes, not on the slide |
| **Speaker notes** | Every slide has notes — what you will say, in the order you will say it |
| **Bullet depth** | One level. Nested bullets are an outline leaking onto a slide |
| **Title** | States the point, not the topic ("Latency dropped 40%" not "Performance") |

### 66.2 Accessibility

Slides are read on projectors, phones, and by people with low vision or color blindness.

- **Contrast** — meet WCAG AA (4.5:1 for normal text, 3:1 for large text). Dark text on light or light on dark; never mid-gray on mid-gray
- **Never color-only** — a red/green status must also carry text or an icon
- **Alt text** on every image, chart, and diagram
- **Reduced motion** — if the deck animates, respect `prefers-reduced-motion` in an HTML deck; avoid motion that carries meaning
- **Fonts** — use one or two; if the deck must render identically on an unknown machine, embed or use a web-safe stack

### 66.3 Honest Numbers

The same honesty boundaries as [Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md) 50.6 apply, and decks are where they get broken most often:

- Every number is either measured (with a source and a date) or explicitly labeled **illustrative**
- No invented benchmarks, user counts, growth curves, or "industry average" figures
- Labeled illustrative data still looks illustrative — say it on the slide, not just in the notes
- If asked "where does that come from?" during the talk, the answer must exist
- Name the model or tool that produced any AI-generated result you present

### 66.4 Optional: Decks as Code

When a deck will be re-rendered repeatedly (a recurring talk, a template for the team), build it as code rather than by hand-editing a binary file.

**Structure:**

- **Design tokens** — colors, spacing, type scale in one theme file you can swap
- **Grid** — a consistent layout grid; every slide places content on it
- **Type scale** — a small set of sizes (title, subtitle, body, caption); no ad-hoc sizes
- **One accent color** — used only for the call to action or the single thing you want remembered
- **Layout primitives** — a handful of slide types (title, statement, comparison, chart, quote) reused everywhere

**Render-and-inspect loop:**

1. Render to PDF or PNG
2. Inspect each slide as an image — not as source
3. Fix overflow, cramped spacing, and unreadable type
4. Repeat until no slide needs a second look

Never eyeball the source and call it done; text that fits in the editor routinely overflows in the export.

### 66.5 Delivery Check

- [ ] Every slide carries one idea, with speaker notes
- [ ] Body type is readable from the back of the room
- [ ] Contrast meets AA; no meaning is carried by color alone
- [ ] Every number is measured-with-source or labeled illustrative
- [ ] The deck opens and renders on the machine you will present from
- [ ] Exported file is committed/archived, not just the source

---

## References

- WCAG contrast (minimum): https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- Marp (Markdown decks as code): https://marp.app/
- Reveal.js: https://revealjs.com/
