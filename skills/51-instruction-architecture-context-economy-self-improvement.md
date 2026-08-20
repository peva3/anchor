# Skill 51: Instruction Architecture — Context Economy & Self-Improvement

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 51. Instruction Architecture — Context Economy & Self-Improvement

The AGENTS.md file itself is a system. These patterns govern how instructions are loaded, maintained, and adapted — ensuring the instruction system stays lean and improving over time.

### 51.1 Trigger-Based Instruction Loading

Large AGENTS.md files must not flood every context window. Structure specialized knowledge so it only enters context when relevant.

```yaml
# sections/kubernetes.md
---
triggers:
  - kubernetes
  - k8s
  - helm
  - deployment
---
# Kubernetes Deployment Knowledge

When deploying to Kubernetes:
- Use the following resource patterns...
- Never hardcode container ports...
- Always include liveness and readiness probes...
```

**Rules:**
- **Core sections respond to all requests** (Section 1-2, 9, 15, 33, 36) — always loaded
- **Domain-specific sections load on trigger match** — keyword in user message activates them
- **Without a trigger list, the section is always loaded**
- **Trigger matching is case-insensitive, word-boundary-aware** — "kubernetes" matches "deploy to kubernetes" but not "kubernetes-health-check" (single word match)
- **Project-specific sections** (tech stack defaults, deployment patterns) belong in a project's own AGENTS.md, not the universal template — move them there

**Implementation approaches:**
| Approach | When | Trade-off |
|----------|------|-----------|
| **Frontmatter triggers** | Agent supports extensions/plugins | Requires agent support for trigger parsing |
| **Separate files** | Simple, works with any agent | AGENTS.md references them, human decides which to copy in |
| **Collapsible sections** | Markdown-native, always available | Still burns tokens scanning headers |

**The simplest approach (works everywhere):**
Keep the core AGENTS.md lean (≤ 500 lines). Move domain knowledge to `docs/AGENT_DOMAIN_*.md` files. The core file references them:

```markdown
## Domain-Specific Guidance

For specialized domains, consult the relevant guide:
- `docs/AGENT_DOMAIN_KUBERNETES.md` — When the task involves K8s, deployments, or containers
- `docs/AGENT_DOMAIN_ML.md` — When the task involves model training, inference, or data pipelines
- `docs/AGENT_DOMAIN_REALTIME.md` — When the task involves WebSockets, streaming, or pub/sub
```

### 51.2 Self-Maintaining Instructions — Meta-Learning

The AGENTS.md file must evolve. The agent should recognize when its instructions are insufficient and propose improvements.

**When the agent should suggest adding a rule:**
| Signal | Example | Rule to Add |
|--------|---------|-------------|
| **User had to intervene** | User corrected the approach after code was written | Document the correct approach as a required pattern |
| **Multiple back-and-forth rounds** | 3+ iterations to get a behavior right | Codify the final correct behavior as a convention |
| **Edge case discovered the hard way** | A bug caused by a pattern nobody documented | Add the edge case as a gotcha or anti-pattern |
| **Pattern required reading many files to understand** | Agent had to explore 5+ files to figure out architecture | Document the architecture in DEEPDIVE.md |
| **User explicitly said "always do X"** | "Always use `pathlib` not `os.path`" | Add to the Code Style section |

**What NOT to add:**
- Patterns the agent can figure out from reading 2-3 files (these are discoverable)
- Obvious conventions already in PEP 8 or standard style guides
- One-off decisions tied to a specific context that won't recur
- Tool version trivia ("use ruff 0.4.1") — pin in config files, not AGENTS.md

**The meta-instruction itself:**
```
If a user had to correct you, intervene, hand-hold, or repeat themselves
to get the right behavior, PROPOSE adding a rule to AGENTS.md that would
have prevented the issue. Do not wait for the user to ask. The proposal
should be:
  "I should add to AGENTS.md: [specific rule]. OK to add?"
```

**Why this matters:** AGENTS.md files go stale because no process updates them after edge cases are discovered. This pattern makes instruction maintenance a natural part of every interaction.

### 51.3 Context Budget Awareness

Every instruction loaded into context costs tokens. Large AGENTS.md files can consume significant portions of the context window before the task even begins.

**Rules for PROJECT-SPECIFIC AGENTS.md files:**
- **Total AGENTS.md ≤ 2,000 lines** — if longer, split into core + domain guides
- **Per-request instruction budget ≤ 5,000 tokens** — measure this, don't guess
- **Context headroom minimum: 70%** — at least 70% of context window must be available for the task itself
- **Periodic context snapshot** — if context exceeds 50%, summarize key decisions to external storage before continuing

**Exception — this template (standardized-markdown):**
This repository is a universal template library, not a project-specific instruction file. It intentionally exceeds these limits. Individual projects should copy only relevant sections and keep the adapted AGENTS.md within the size budget. The full template serves as a reference — project AGENTS.md files should be lean subsets.

**Size monitoring pattern:**
```bash
# Estimate token count of AGENTS.md (rough: 1 token ≈ 0.75 words)
python -c "
words = open('AGENTS.md').read().split()
print(f'~{int(len(words) / 0.75):,} tokens ({len(words):,} words)')
"
```

**When AGENTS.md is too long:**
1. Move domain-specific patterns to `docs/AGENT_DOMAIN_*.md` (trigger-loaded)
2. Remove redundant examples — one good example per pattern
3. Remove patterns covered by standard style guides (PEP 8, Google style)
4. Remove project-specific defaults and put them in the project's own AGENTS.md

### 51.4 Model Capability Awareness

Different models handle instructions differently. Structure AGENTS.md so it degrades gracefully when read by less capable models.

**Pattern: Tiered Detail Levels**

```markdown
<!-- TIER:ALL -->
This pattern applies to all models.

<!-- TIER:FULL -->
Additional nuance for models with ≥128K context.
Include verbose rationale and edge case discussion.

<!-- TIER:COMPACT -->
Condensed version for models with ≤8K context.
Focus on rules, omit rationale.
```

**What changes at each tier:**
| Aspect | FULL (≥128K) | STANDARD | COMPACT (≤8K) |
|--------|-------------|----------|---------------|
| **Rationale** | Include WHY for every rule | Include for non-obvious rules | Omit — rules only |
| **Examples** | Multiple per pattern | One canonical example | Code snippet only |
| **Edge cases** | Explicit discussion | Notable ones only | Omit — assume standard |
| **Cross-references** | Link between related sections | Key cross-refs | Omit |
| **Anti-patterns** | Multiple with explanation | One per anti-pattern | Short list, no explanation |

**For model families with known quirks:**
- **Claude models:** Can handle verbose, nuanced instruction. Prefer thoroughness.
- **GPT models:** Benefit from explicit output format schemas and structured constraints.
- **Gemini models:** Perform better with role-based framing and clear task boundaries.
- **Small/local models:** Strip everything non-essential. Commands, not prose.

**The fallback rule:** If unsure which model will read this, write for STANDARD. Provide a condensed appendix that summarizes the 20 most critical rules in bullet form for compact contexts.

### 51.5 Instruction Provenance — Where Did This Rule Come From

Every non-obvious rule should be traceable to its source. This prevents cargo-culting and enables future readers to decide if a rule still applies.

**Provenance annotation pattern:**
```markdown
- **No eval()/exec() on user input.** [Source: OWASP, Section 27.3]
- **800-line PR size limit.** [Source: Code review research, Section 33.1]
- **Structured tradeoff comments with named ceilings.** [Source: ponytail, Section 50.2]
```

**Rules for provenance:**
- **Cite the standard** (OWASP, SemVer, Google testing blog, PEP)
- **Link to source material** when available (arXiv paper, blog post, research article)
- **Include the date** when a rule was added (in Change Log)
- **Mark rules derived from project-specific experience** — these may not apply universally
- **Periodically audit** — if a rule's source has been superseded or disproven, update or remove it

---

