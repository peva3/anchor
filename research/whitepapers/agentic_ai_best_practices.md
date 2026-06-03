# Agentic AI Best Practices - Comprehensive Guide

## Overview
This document compiles best practices for AI agent system prompts, instruction-following, and prompt engineering for agents based on research and industry resources.

---

## 1. SYSTEM PROMPT STRUCTURE

### Core Components
Every agent system prompt should include:

1. **Role Definition**
   - Clear identification of agent's purpose
   - Specific domain expertise
   - Boundaries and limitations

2. **Capability Boundaries**
   - What the agent can and cannot do
   - Available tools and functions
   - Output format constraints

3. **Output Specifications**
   - Structured output requirements (JSON schemas)
   - Response formatting rules
   - Error handling protocols

4. **Behavior Guardrails**
   - Ethical guidelines
   - Safety constraints
   - Fallback instructions

### Example Structure
```
# Role: [Agent Name]
You are a [domain] assistant that [primary function].

## Capabilities
- [List of abilities]
- [Tools available]

## Output Format
Always respond with valid JSON:
{
  "action": "string",
  "parameters": {},
  "reasoning": "string"
}

## Constraints
- Never [forbidden actions]
- Always [required behaviors]
```

---

## 2. INSTRUCTION FOLLOWING BEST PRACTICES

### From AgentBench Research (arXiv:2308.03688)
- **Instruction following is critical** - main obstacle for LLM agents
- High-quality multi-round alignment data improves performance
- Code training has mixed effects (improves some tasks, harms others)
- Poor long-term reasoning is a key failure mode

### Key Strategies
1. **Clear, Explicit Instructions**
   - Break down complex tasks
   - Use step-by-step guidance
   - Provide examples

2. **Format Enforcement**
   - Use structured prompts
   - Include output templates
   - Validate responses

3. **Feedback Loops**
   - Include self-correction mechanisms
   - Allow iterative refinement
   - Monitor instruction compliance

---

## 3. MULTI-AGENT COORDINATION

### From CAMEL Research (arXiv:2303.17760)
- Role-playing frameworks improve agent cooperation
- Inception prompting guides agents toward goals
- Task decomposition through roles enables complex problem-solving

### Patterns
1. **Role Assignment**
   - Define clear roles for each agent
   - Specify interaction protocols
   - Establish decision-making authority

2. **Hierarchical Coordination**
   - Supervisor agent orchestrates worker agents
   - Clear input/output contracts
   - Verification gates at each stage

3. **Collaborative Problem-Solving**
   - Multiple agents contribute expertise
   - Structured debate/discussion protocols
   - Consensus building mechanisms

---

## 4. MEMORY AND CONTEXT MANAGEMENT

### From Eywa Research (arXiv:2605.30771)
- Provenance-grounded memory architecture improves reliability
- Evidence before belief principle
- Zero LLM calls inside retrieval for deterministic results

### Best Practices
1. **Separation of Concerns**
   - Store evidence separately from derived facts
   - Keep retrieved context distinct from answer instructions
   - Enable audit trails for decisions

2. **Context Management**
   - Bounded memory context windows
   - Deterministic retrieval paths
   - Source verification

---

## 5. PRODUCTION DEPLOYMENT CONSIDERATIONS

### From PRISM Research (arXiv:2605.15665)
- Continuous prompt monitoring is essential
- Simulation-driven optimization catches regressions
- 99% production reliability achievable

### Key Requirements
1. **Deterministic Outputs**
   - JSON Schema enforcement
   - Explicit acceptance criteria
   - Validation at boundaries

2. **Observability**
   - Track prompt performance over time
   - Monitor behavioral drift
   - Implement alerting for failures

3. **Guardrails**
   - Input validation
   - Output filtering
   - Rollback mechanisms

---

## 6. VERIFICATION AND ERROR HANDLING

### From Meta-Agent Research (arXiv:2605.25233)
- Construction-time verification validates generated artifacts
- Execution-time verification gates intermediate outputs
- Three-level error attribution (local, upstream, structural)

### Strategies
1. **Multi-Stage Verification**
   - Validate each step before proceeding
   - Catch errors early
   - Enable targeted recovery

2. **Error Classification**
   - Distinguish failure types
   - Apply appropriate recovery strategies
   - Learn from failures

---

## 7. CODE GENERATION AGENTS

### From Context-Augmented Code Generation (arXiv:2605.08112)
- Product context retrieval improves decision compliance by **49%**
- Baseline achieves 100% on decisions visible in codebase
- Falls to 0-33% on decisions requiring product context

### Implications
- Provide relevant context in prompts
- Include team-specific conventions
- Reference existing patterns

---

## 8. AGENT HARNESS FRAMEWORKS

### Essential Components
1. **Tools** - Function calling capabilities
2. **Memory** - Persistent state management
3. **Planning** - Goal decomposition and tracking
4. **Verification** - Output validation

### Example Frameworks
- AutoGPT: 185k stars, extensive agent capabilities
- Dify: Production workflow development platform
- Ollama: Local LLM deployment with agent integrations

---

## 9. EVALUATION METRICS

### Agent Performance Dimensions
1. **Task Success Rate** - Completion of objectives
2. **Instruction Compliance** - Following given instructions
3. **Reasoning Quality** - Logical chain-of-thought
4. **Error Recovery** - Self-correction ability
5. **Contextual Awareness** - Appropriate use of provided context

### Benchmark Resources
- AgentBench (arXiv:2308.03688): 8 environments, 29 LLMs
- LoCoMo: Long-term memory evaluation
- LongMemEval-S: Technical memory stress test
- BEAM: 700-question benchmark

---

## 10. KEY TENSIONS AND TRADEOFFS

### Flexibility vs. Robustness
- More flexible prompts allow diverse responses
- More constrained prompts improve reliability
- Trade-off depends on use case criticality

### Test-Time vs. Training-Time Investment
- Prompt optimization (test-time) vs. fine-tuning (training-time)
- PRISM approach: simulation-driven continuous optimization
- Cost-benefit analysis required

### Local vs. Cloud Models
- OpenJarvis findings: local models can match cloud on 4/8 benchmarks
- ~800x cost reduction possible with local deployment
- 4x latency improvement

---

## 11. ANTHROPIC CLAUDE COOKBOOK PATTERNS

### Tool Use Patterns
- Context engineering for tool selection
- Memory integration patterns
- Parallel tool execution

### Key Resources
- https://github.com/anthropics/claude-cookbooks/tree/main/tool_use
- Contains: customer_service_agent.ipynb, memory_cookbook.ipynb, etc.

---

## 12. AUTOGPT AGENTS.MD BEST PRACTICES

### Code Organization
- Component structure: ComponentName/ComponentName.tsx + useComponentName.ts + helpers.ts
- Function declarations (not arrow functions) for components/handlers
- Colocate state, avoid large components

### Testing Strategy
- Integration tests (Vitest + RTL + MSW) ~90% - DEFAULT
- Playwright for E2E critical flows
- Storybook for design system components

### Data Fetching
- Generated API hooks from `@/app/api/__generated__/endpoints/`
- Pattern: `use{Method}{Version}{OperationName}`

---

## 13. PROMPT ENGINEERING INSTITUTE FRAMEWORKS

### ACE Framework
- **Aim**: Define business intent in plain language
- **Coordinate**: Decide who/what runs next
- **Execute**: Perform work via deterministic scripts

### Production Requirements
1. Deterministic outputs with schemas
2. Guardrails and explicit acceptance criteria
3. Observability and monitoring
4. Staged deployment with rollback

---

## 14. SUMMARY OF KEY PRINCIPLES

| Principle | Source | Impact |
|-----------|--------|--------|
| Clear role definition | CAMEL | Enables cooperation |
| Instruction following | AgentBench | Critical for success |
| Context augmentation | Context-Augmented | +49% compliance |
| Provenance memory | Eywa | 90%+ accuracy |
| Continuous monitoring | PRISM | 99% reliability |
| Multi-stage verification | Meta-Agent | Catches failures early |

---

*Compiled from research papers and industry resources*
*June 2026*
