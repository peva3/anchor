# CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society

**arXiv:** https://arxiv.org/abs/2303.17760
**Published:** NeurIPS 2023
**Authors:** Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, Bernard Ghanem

## Abstract

CAMEL introduces a novel **role-playing** framework for autonomous cooperation among communicative agents. The key innovation is **inception prompting** - guiding chat agents toward task completion while maintaining consistency with human intentions.

## Core Concept: Inception Prompting

Instead of relying on human guidance at every step, CAMEL uses an AI assistant to instruct another AI assistant. This creates a self-reinforcing loop where:
1. One agent proposes tasks
2. Another agent executes them
3. The conversation guides itself without human intervention

## Role-Playing Framework

Agents are assigned specific roles (e.g., "Python programmer", "Linux terminal") with:
- Defined **role description**
- Clear **task specification**
- **Termination criteria**

The AI assistant role-play initiates cooperation, with the first agent guiding the process.

## Key Design Principles

1. **Scalability** - Generate unlimited conversation data for studying agent behaviors
2. **Consistency** - Prevent role flipping through careful prompt engineering
3. **Safety** - Prohibit harmful or false information through inception prompts
4. **Cooperation** - Encourage consistent conversation flow

## CAMEL Architecture

```
Agent 1 (Task Specify) → Agent 2 (Task Execute) → Critique Agent → Iterative Refinement
```

### Agent Types
- **Task Specify Agent** - Proposes and breaks down tasks
- **Task Execute Agent** - Performs the actual work
- **Critic Agent** - Reviews and provides feedback

## Multi-Agent Cooperation Patterns

1. **Role Assignment** - Explicit role definitions in prompts
2. **Task Decomposition** - Breaking complex tasks into subtasks
3. **Feedback Loops** - Critic agents provide revision guidance
4. **Termination Detection** - Criteria for recognizing task completion

## Impact on Agent Guidance Design

CAMEL's approach suggests AGENTS.md should include:
- **Role definitions** - What the agent is expected to do
- **Task boundaries** - Clear scope and limitations
- **Cooperation protocols** - How to interact with other agents/tools
- **Safety constraints** - What the agent should and shouldn't do
- **Completion criteria** - When to stop and report results

## Key Insight: "Essence lies in prompt engineering"

From Sophia Yang (Head of Developer Relations at Mistral AI):
> "The essence of Camel lies in its prompt engineering, i.e., inception prompting. The prompts are actually carefully defined to assign roles, prevent flipping roles, prohibit harm and false information, and encourage consistent conversation."

## Repository

https://github.com/camel-ai/camel
https://www.camel-ai.org