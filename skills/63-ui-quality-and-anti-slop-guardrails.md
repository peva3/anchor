# Skill 63: UI Quality & Anti-Slop Guardrails

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 63. UI Quality & Anti-Slop Guardrails

Frontend work has its own failure modes distinct from backend code. "Slop" is the pattern of shipping interfaces that look finished but contain fabricated content, dead controls, or broken states. These guardrails mirror [Section 34](skills/34-ai-code-quality-anti-pattern-detection.md) but for the visual layer. They are engineering requirements, not aesthetic opinions. (Adapted from the anti-slop rule library: https://github.com/miqdadbadjuber/anti-slop.)

### 63.1 No Fabricated Content

Every visible asset must be real or explicitly labeled as a placeholder. Agents commonly invent the following to make a UI look complete:

| Fabrication | Looks Like | Must Be |
|-------------|-----------|---------|
| **Testimonials** | "Loved by 10,000+ teams" with fake quotes | Real quotes with real attribution, or removed |
| **Stats/metrics** | "99.9% uptime", "2M users" without a data source | Real numbers pulled from a real source, or removed |
| **Compliance claims** | "SOC 2", "GDPR", "HIPAA compliant" badges | Only shown when the project actually holds the certification |
| **Logos/avatars** | Brand logos, customer logos, team photos | Real assets with rights, or a labeled placeholder (`[LOGO]`, `[PHOTO]`) |
| **Team/personas** | Fictional team members, fake bylines | Real people, or omitted |
| **Success/failure messages** | "Payment sent!" on a mock flow | Only when the underlying action actually ran |

**Rule:** if a claim or asset cannot be sourced to reality, do not fabricate it to improve the demo. Label placeholders honestly (e.g. "Sample data shown — connect a real source").

### 63.2 Functional Completeness — No Dead Controls

A visible interactive element with no working behavior is a defect, not a placeholder:

- **Every button, link, nav item, form field, and toggle MUST have real behavior** — or be removed from the UI for the current milestone
- If an action is intentionally deferred, it must be visibly disabled or labeled ("Coming soon") — never silently a dead end
- **Every nav destination must exist** — no menu items pointing at empty/404 pages
- Forms must actually submit, validate, and handle the response; modals must open AND close; carousels must navigate
- Run a manual click-through of every interactive element before calling UI work complete (ties to [Section 35](skills/35-pr-description-format-template.md) testing checklist)

### 63.3 Required UI States

Any UI that displays data MUST handle all three states, not just the happy path:

| State | Requirement |
|-------|-------------|
| **Empty** | A clear empty state explaining there is no data yet and (where relevant) how to add it — never a blank box |
| **Loading** | A visible loading indicator while fetching — never a flash of "empty" before data arrives |
| **Error** | A readable error state with what went wrong and a retry path — never a silent freeze or white screen |

**Rule:** an agent must implement and verify empty/loading/error states for every data-driven view, not assume data will always be present.

### 63.4 Accessibility Minimums (WCAG AA)

Accessibility is functional engineering, not polish:

- **Color contrast** ≥ 4.5:1 for normal text, ≥ 3:1 for large text (WCAG AA)
- **Keyboard operable** — every interactive element reachable and usable via Tab/Enter/Space; no mouse-only interactions
- **Visible focus indicators** — never remove outlines with `outline: none` without a replacement focus style
- **Semantic HTML / roles** — use real buttons/links/landmarks rather than divs with handlers where possible
- **Form labels** — every field has an associated label; errors are programmatically associated with their field
- Do not rely on color alone to convey state (e.g. also show an icon or text for success/error)

### 63.5 The "Dials" Mechanism — Enforceable Liveliness

Subjective taste is hard for an agent to self-judge. Replace continuous judgment with a **3-level dial** that is binary-checkable at each level. Set each dial explicitly and check the level's requirements before shipping:

| Dial | Level 1 (minimal) | Level 2 (moderate) | Level 3 (high) |
|------|-------------------|--------------------|-----------------|
| **ENERGY** | Static layout, default system styling | A clear visual hierarchy + one deliberate accent | Distinct personality: custom palette, type scale, motion |
| **RHYTHM** | Default spacing | Consistent spacing scale + alignment grid | Deliberate pacing of density/whitespace for scanability |
| **MOTION** | No animation | Purposeful transitions (hover/state changes only) | Motion used to guide attention; respects `prefers-reduced-motion` |

**Rule:** for any UI deliverable, state the intended level of each dial up front, then verify the output actually meets that level's bar. If a design decision cannot be justified at the chosen dial level, simplify or raise the level deliberately — do not ship a gray area.

### 63.6 Delivery Self-Check

Before a UI change is marked complete, run this checklist (mirrors [Section 34.8](skills/34-ai-code-quality-anti-pattern-detection.md) for the visual layer):

- [ ] No fabricated content, stats, personas, or compliance claims
- [ ] No dead controls — every interactive element clicked through and works
- [ ] Empty / loading / error states present on all data-driven views
- [ ] WCAG AA contrast + keyboard navigation + visible focus verified
- [ ] ENERGY / RHYTHM / MOTION dials set deliberately and met
- [ ] Renders correctly at the project's supported viewport sizes

---

## References

- Anti Slop — Rules for AI Coding Agents: https://github.com/miqdadbadjuber/anti-slop
- WCAG 2 contrast (minimum): https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
