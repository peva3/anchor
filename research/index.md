# AI Agent Prompt Guidance Research - Complete Index

This folder contains comprehensive research on best practices for AI agent prompt guidance, including whitepapers and GitHub projects with excellent AGENTS.md files.

## Research Gathered

### Whitepapers (in `/research/whitepapers/`)
| File | Description |
|------|-------------|
| `agentic_ai_best_practices.md` | Comprehensive best practices guide (8.1KB) |

### Papers (in `/research/papers/full/`)
| File | arXiv ID | Key Finding |
|------|----------|-------------|
| `agentbench.md` | 2308.03688 | Instruction following is the main differentiator between LLM agents |
| `agentbench-2308.03688.md` | 2308.03688 | Full AgentBench paper summary |
| `camel.md` | 2303.17760 | Inception prompting enables autonomous multi-agent cooperation |
| `camel-2303.17760.md` | 2303.17760 | Full CAMEL paper summary |
| `chatdev-2307.07924.md` | 2307.07924 | Multi-agent software development (ACL 2024) |
| `hugginggpt-2303.17580.md` | 2303.17580 | LLM as controller paper |
| `metagpt-2308.00352.md` | 2308.00352 | Meta-programming framework with SOPs |
| `tool-learning-2304.08354.md` | 2304.08354 | Comprehensive tool learning framework |
| `voyager-2305.16291.md` | 2305.16291 | Minecraft embodied agent paper |

### GitHub Projects (in `/research/github/`)
| File | Stars | Key Insight |
|------|-------|-------------|
| `autogpt_agents_md.md` | 185k | AutoGPT's AGENTS.md - agent contribution guidelines |
| `autogpt-agents.md` | 185k | AutoGPT agent patterns |
| `autogpt-readme.md` | 185k | AutoGPT README content |
| `langchain.md` | 138k | Comprehensive development guidelines, type hints mandatory |
| `langchain-agents.md` | 138k | LangChain agent patterns |
| `microsoft-ai-agents-for-beginners.md` | 66k | Educational course structure, clear progression |
| `microsoft-ai-agents-beginners-agents.md` | 66k | Microsoft AI Agents course AGENTS.md |
| `microsoft-autogen-agents.md` | - | Microsoft AutoGen patterns |

## Key Insights for AGENTS.md Design

### From AgentBench (arXiv:2308.03688)
1. **Clear, precise instructions** - Ambiguity leads to format failures
2. **Explicit action schemas** - Define exact output formats
3. **Single-turn focus where possible** - Reduce multi-round complexity
4. **Error recovery patterns** - Include retry/validation mechanisms
5. **Code-style examples** - Show exact expected outputs

### From CAMEL (arXiv:2303.17760)
1. **Role definitions** - What the agent is expected to do
2. **Task boundaries** - Clear scope and limitations
3. **Cooperation protocols** - How to interact with other agents/tools
4. **Safety constraints** - What the agent should and shouldn't do
5. **Completion criteria** - When to stop and report results

### From LangChain AGENTS.md
1. **Explicit tool requirements** - Specify make, uv, ruff, mypy
2. **Command examples** - Actual commands to run
3. **PR title format** - Clear conventions with examples
4. **Breaking change warnings** - Critical for API stability
5. **Type hints mandatory** - Enforced standard
6. **Test coverage requirement** - Every feature needs tests

### From Microsoft AI Agents for Beginners
1. **Lesson-based structure** - Clear progression path
2. **Setup verification steps** - Ensure environment correctness
3. **Common pitfalls documented** - Help users avoid issues
4. **Multiple framework examples** - Flexibility in implementation

## Original Sources

- AgentBench: https://arxiv.org/abs/2308.03688
- CAMEL: https://arxiv.org/abs/2303.17760
- LangChain: https://github.com/langchain-ai/langchain
- Microsoft AI Agents for Beginners: https://github.com/microsoft/ai-agents-for-beginners
- CAMEL-AI Framework: https://www.camel-ai.org
- AutoGPT: https://github.com/autogpt-agent/autogpt
- MetaGPT: https://github.com/FoundationAgents/MetaGPT
- CrewAI: https://github.com/crewAIInc/crewAI
- AgentOps: https://github.com/AgentOps-AI/agentops

## Key Findings Summary

### Critical for Agent Instruction Quality:
1. **Instruction Following** - The #1 differentiator between successful and failing agents
2. **Clear Role Definitions** - Agents need explicit role descriptions
3. **Task Boundaries** - Clear scope and limitations prevent off-task behavior
4. **Completion Criteria** - When to stop and report results
5. **Error Recovery** - Retry and validation mechanisms

### AGENTS.md Best Practices Observed:
1. Include explicit tool requirements (make, uv, ruff, mypy, pytest)
2. Provide command examples - actual commands to run
3. Document common pitfalls and how to avoid them
4. Include setup verification steps
5. Use code-style examples showing exact expected outputs
6. Define clear PR/commit conventions
7. Specify test coverage requirements

## Directory Structure

```
standardized-markdown/
├── research/
│   ├── index.md (this file)
│   ├── ai_agent_prompt_research_summary.md
│   ├── papers/
│   │   └── full/
│   │       ├── agentbench.md
│   │       ├── agentbench-2308.03688.md
│   │       ├── camel.md
│   │       ├── camel-2303.17760.md
│   │       ├── chatdev-2307.07924.md
│   │       ├── hugginggpt-2303.17580.md
│   │       ├── metagpt-2308.00352.md
│   │       ├── tool-learning-2304.08354.md
│   │       └── voyager-2305.16291.md
│   ├── github/
│   │   ├── autogpt_agents_md.md
│   │   ├── autogpt-agents.md
│   │   ├── autogpt-readme.md
│   │   ├── langchain.md
│   │   ├── langchain-agents.md
│   │   ├── microsoft-ai-agents-for-beginners.md
│   │   ├── microsoft-ai-agents-beginners-agents.md
│   │   └── microsoft-autogen-agents.md
│   └── whitepapers/
│       └── agentic_ai_best_practices.md
└── AGENTS.md (standardized template)
```

## Collection Stats

- **7 full papers** retrieved and summarized
- **9 GitHub projects** analyzed for AGENTS.md patterns
- **1 comprehensive whitepaper** on agentic AI best practices
- **5+ key whitepaper sources** identified (AgentBench, CAMEL, etc.)

Total research content: ~40KB across all files