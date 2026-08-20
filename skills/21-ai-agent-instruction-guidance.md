# Skill 21: AI Agent Instruction Guidance

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 21. AI Agent Instruction Guidance

> Based on research from AgentBench (arXiv:2308.03688) and CAMEL (arXiv:2303.17760) on what makes AI agents effective.
>
> **Provenance** (per [Section 51.5](skills/51-instruction-architecture-context-economy-self-improvement.md)):
> - **Sections 21.1, 24 (IF/IA/TLE/CLE failure modes)** — [AgentBench: A Benchmark for Evaluating LLMs as Agents](research/papers/full/agentbench-2308.03688.md) (arXiv:2308.03688, ICLR 2024)
> - **Sections 22, 21.2 (role assignment, multi-agent cooperation)** — [CAMEL: Communicative Agents for "Mind" Exploration of LLM Society](research/papers/full/camel-2303.17760.md) (arXiv:2303.17760, NeurIPS 2023)

### 21.1 Critical Findings

**Instruction following is the #1 differentiator** between successful and failing agents. Poor instruction following causes most agent failures, including:
- Invalid Format (IF) — Agent doesn't follow output format instructions
- Invalid Action (IA) — Format correct but action is invalid
- Task Limit Exceeded (TLE) — No solution after max rounds / repeated generations

### 21.2 Role Definition Pattern

Every task must include explicit role definitions:

```
Role: What the agent is expected to do
Goal: The specific outcome being sought
Backstory: Context that shapes how to approach the task
```

**Example:**
```yaml
role: Senior Data Researcher
goal: Uncover cutting-edge developments in {topic}
backstory: You're a seasoned researcher known for finding the most 
           relevant information and presenting it clearly.
```

### 21.3 Task Boundary Pattern

Define clear scope to prevent off-task behavior:

```
Description: What to do (specific, measurable)
Expected Output: Exact format of the deliverable
Tools: Available tools and how to use them
Constraints: What NOT to do
```

**Example:**
```yaml
description: >
  Conduct a thorough research about {topic}
  Make sure you find any interesting and relevant information
expected_output: >
  A list with 10 bullet points of the most relevant information
  Formatted as markdown without code blocks
constraints:
  - Do not invent information not in the source
  - Do not exceed 500 words total
```

### 21.4 Completion Criteria Pattern

Define when to stop and report results:

```
Completion Signal: What indicates the task is done
Output File: Where to write results (if applicable)
Success Criteria: How to verify the output is correct
```

**Example:**
```yaml
completion: >
  Task is complete when research findings are written to 
  report.md with all 10 bullet points filled in
output_file: report.md
success_criteria:
  - Exactly 10 bullet points
  - Each bullet < 50 words
  - No placeholder text "[TODO]"
```

### 21.5 Error Recovery Pattern

Include retry and validation mechanisms:

```
Validation: How to check if output is correct
Retry Strategy: What to do if validation fails
Fallback: What to do if retry also fails
```

**Example:**
```yaml
validation:
  - Check that output is not empty
  - Check that output is not gibberish or repeating
  - Check that output matches expected format
retry:
  max_attempts: 3
  delay_seconds: 2
fallback: >
  If all retries fail, report the specific error and 
  what was attempted before giving up
```

### 21.6 Explicit Action Schema Pattern

Define exact output formats to prevent format failures:

**Good:**
```yaml
output_format:
  type: structured
  schema:
    findings:
      type: array
      items:
        type: object
        properties:
          topic: string
          relevance: string
          source: string
        required: [topic, relevance]
  example: |
    findings:
      - topic: "AI Agents"
        relevance: "High"
        source: "arxiv.org"
```

**Bad:**
```yaml
# Vague instructions lead to format failures
output: "List your findings"
```

### 21.7 Multi-Agent Cooperation Pattern

When multiple agents work together:

```
Agent 1 (Task Specify): Proposes and breaks down tasks
Agent 2 (Task Execute): Performs the actual work
Critic Agent: Reviews and provides feedback
```

- Assign explicit roles to each agent
- Define interaction protocol (sequential, hierarchical, parallel)
- Include termination criteria for handoffs

---

