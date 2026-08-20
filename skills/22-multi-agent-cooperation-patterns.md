# Skill 22: Multi-Agent Cooperation Patterns

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 22. Multi-Agent Cooperation Patterns

Based on CAMEL (arXiv:2303.17760) and MetaGPT (arXiv:2308.00352).

### 22.1 Role Definition Template

Every multi-agent task requires explicit role definitions:

```yaml
role: Senior <Domain> Engineer
goal: <Specific outcome being sought>
backstory: |
  You are a seasoned engineer known for <expertise>.
  You approach problems by <methodology>.
constraints:
  - Do not <forbidden action>
  - Always <required action>
  - Stop when <termination condition>
```

### 22.2 Sequential Handoff Pattern (Assembly Line)

For workflows where agents pass work sequentially (MetaGPT-style):

```
Product Manager → Architect → Engineer → QA → Deploy
```

**Rules:**
1. Each agent has explicit input/output contracts
2. Verification gate at each handoff before proceeding
3. Document any deviations at handoff boundaries
4. Supervisor agent tracks overall progress

**Example:**
```
Agent 1 (PM): Defines requirements → outputs SPEC.md
Agent 2 (Architect): Reviews SPEC → outputs architecture.md
Agent 3 (Engineer): Implements → outputs code + tests
Agent 4 (QA): Verifies → outputs test report
```

### 22.3 Hierarchical Pattern

For supervisor/worker architectures:

```
Supervisor Agent
├── Worker 1 (specific subtask)
├── Worker 2 (specific subtask)
└── Worker 3 (specific subtask)
```

**Rules:**
1. Supervisor assigns clear sub-tasks with boundaries
2. Workers report results to supervisor
3. Supervisor aggregates and decides next steps
4. Timeout on workers — if exceeded, supervisor escalates

### 22.4 Collaborative Pattern

For peer-to-peer agent cooperation:

```
Agent A ←→ Shared Context ←→ Agent B
              ↓
          Critic Agent
```

**Rules:**
1. Agents share a common context (document, state, memory)
2. Critic agent reviews and provides feedback
3. Agents iterate based on critique
4. Termination when consensus reached or max iterations hit

### 22.5 Multi-Agent Termination Criteria

For all patterns, define:
- **Max iterations** — Stop after N cycles even if not complete
- **Consensus threshold** — When to stop (e.g., 2 of 3 agents agree)
- **Escalation path** — What to do when termination reached without success
- **Context snapshot** — Save state before termination for resume

---

