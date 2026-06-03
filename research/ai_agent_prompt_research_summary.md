# AI Agent Prompt Guidance & Instructions - Research Summary

## Overview
This document summarizes research gathered on best practices for AI agent prompt guidance, system prompts, instruction-following, and agentic AI systems.

---

## 1. ARXIV RESEARCH PAPERS

### 1.1 AgentBench: Evaluating LLMs as Agents (arXiv:2308.03688)
- **Authors**: Xiao Liu et al. (22 authors)
- **Published**: ICLR 2024
- **Key Finding**: Top commercial LLMs show strong agent abilities, but significant disparity exists between them and open-source models (70B or smaller)
- **Key Issues Identified**: 
  - Poor long-term reasoning
  - Decision-making failures
  - Instruction following issues
- **Recommendations**: 
  - Improving instruction following improves agent performance
  - High-quality multi-round alignment data helps
  - Training on code shows mixed results
- **URL**: https://arxiv.org/abs/2308.03688

### 1.2 CAMEL: Communicative Agents for "Mind" Exploration (arXiv:2303.17760)
- **Authors**: Guohao Li et al.
- **Published**: NeurIPS 2023
- **Key Contribution**: Novel role-playing framework for autonomous cooperation among communicative agents
- **Method**: Uses "inception prompting" to guide chat agents toward task completion
- **URL**: https://arxiv.org/abs/2303.17760

### 1.3 Meta-Agent: From Task Descriptions to Verified Multi-Agent Systems (arXiv:2605.25233)
- **Authors**: Andy Xu, Yu-Wing Tai
- **Key Contribution**: Two-phase framework that automatically constructs specialized multi-agent systems from natural-language task descriptions
- **Features**:
  - Construction phase: task planner decomposes problems into DAG of agent specifications
  - Execution phase: coordinator dispatches subtasks with verification
  - Three-level error attribution mechanism
- **URL**: https://arxiv.org/abs/2605.25233

### 1.4 PRISM: Prompt Reliability via Iterative Simulation and Monitoring (arXiv:2605.15665)
- **Authors**: Keshava Chaitanya, Jahnavi Gundakaram
- **Key Contribution**: Closed-loop framework treating prompt engineering as continuous reliability engineering
- **Results**: 
  - Reduces median prompt authoring from 2 days to <30 minutes
  - 99% production reliability across 35 enterprise agents
  - Detects and repairs regressions within 24 hours
- **URL**: https://arxiv.org/abs/2605.15665

### 1.5 OpenJarvis: Personal AI, On Personal Devices (arXiv:2605.17172)
- **Authors**: Jon Saad-Falcon et al.
- **Key Contribution**: Decomposed personal AI stack with 5 primitives: Intelligence, Engine, Agents, Tools & Memory, and Learning
- **Innovation**: LLM-guided spec search for local-cloud collaboration
- **Results**: On-device specs match/exceed cloud accuracy on 4/8 benchmarks
- **URL**: https://arxiv.org/abs/2605.17172

### 1.6 GraphFlow: Architecture for Verifiable Visual Workflows (arXiv:2605.14968)
- **Authors**: Drewry H. Morris V et al.
- **Key Contribution**: Visual workflow system for reliable agentic AI automation
- **Results**: 97.08% completion rate across 8,728 workflow runs
- **URL**: https://arxiv.org/abs/2605.14968

### 1.7 Agentic Agile-V: From Vibe Coding to Verified Engineering (arXiv:2605.20456)
- **Authors**: Christopher Koch
- **Key Contribution**: SCOPE-V loop (Specify, Constrain, Orchestrate, Prove, Evolve, Verify) for agentic software engineering
- **Key Insight**: Agentic AI doesn't eliminate engineering discipline; it increases value of requirements, constraints, traceability
- **URL**: https://arxiv.org/abs/2605.20456

### 1.8 Eywa: Provenance-Grounded Long-Term Memory for AI Agents (arXiv:2605.30771)
- **Authors**: Resham Joshi
- **Key Contribution**: Memory architecture built around "evidence before belief"
- **Results**: 90.19% judge accuracy on LoCoMo C1-C4 split
- **URL**: https://arxiv.org/abs/2605.30771

### 1.9 Meta-Engineering Harnesses for AI-Native Software Production (arXiv:2605.25665)
- **Authors**: Satadru Sengupta et al.
- **Key Contribution**: Contract-driven adversarial verification architecture
- **Features**: Two-pass contract compilation, persistent markdown memory, four-way failure arbiter
- **URL**: https://arxiv.org/abs/2605.25665

### 1.10 Context-Augmented Code Generation (arXiv:2605.08112)
- **Authors**: Drew Dillon, Kasyup Varanasi
- **Key Finding**: Product context retrieval improves AI coding agent decision compliance by 49% (46% to 95%)
- **URL**: https://arxiv.org/abs/2605.08112

---

## 2. GITHUB REPOSITORIES WITH EXCELLENT AGENT GUIDANCE

### 2.1 AutoGPT (Significant-Gravitas/AutoGPT) - 185k stars
- **AGENTS.md**: https://github.com/Significant-Gravitas/AutoGPT/blob/master/AGENTS.md
- **Content**: Platform contribution guide with directory overview, code style, frontend guidelines, testing strategy
- **Key Patterns**:
  - Component structure: ComponentName/ComponentName.tsx + useComponentName.ts + helpers.ts
  - Design system usage from src/components/
  - Testing: Vitest + RTL + MSW for integration, Playwright for E2E
  - Function declarations (not arrow functions) for components/handlers

### 2.2 Dify (langgenius/dify) - 144k stars
- **Focus**: Production-ready platform for agentic workflow development
- **Tags**: python, agent, workflow, automation, ai, mcp, orchestration

### 2.3 Microsoft AI Agents for Beginners (microsoft/ai-agents-for-beginners) - 66.4k stars
- **Content**: 12 Lessons to get started building AI agents
- **Topics**: autogen, semantic-kernel, ai-agents-framework

### 2.4 Hugging Face Agents Course (huggingface/agents-course) - 29.1k stars
- **Content**: Comprehensive agents course with tutorials

### 2.5 ruflo (ruvnet/ruflo) - 57.7k stars
- **Focus**: Agent meta-harness for Claude with multi-agent swarms
- **Features**: Adaptive memory, self-learning swarm intelligence, RAG integration

### 2.6 claude-code-best-practice (shanraisshan/claude-code-best-practice) - 56.2k stars
- **Content**: From vibe coding to agentic engineering best practices

### 2.7 Composio (ComposioHQ/composio) - 28.6k stars
- **Focus**: Toolkits, tool search, context management, authentication for AI agents

### 2.8 Google ADK Python (google/adk-python) - 20k stars
- **Focus**: Code-first Python toolkit for building AI agents

### 2.9 agents-towards-production (NirDiamant/agents-towards-production) - 20.6k stars
- **Focus**: End-to-end tutorials for production-grade GenAI agents

---

## 3. PROMPT ENGINEERING RESOURCES

### 3.1 Prompt Engineering Institute (promptengineering.org)
- **ACE Framework**: Split work into Aim, Coordinate, Execute
- **Key Articles**:
  - "Agents At Work: The 2026 Playbook for Building Reliable Agentic Workflows"
  - "From hype to revenue: 7 non-negotiables for a production-grade agentic workflow"
- **URL**: https://promptengineering.org/

### 3.2 Anthropic Claude Cookbooks
- **Path**: https://github.com/anthropics/claude-cookbooks/tree/main/tool_use
- **Content**: Tool use patterns, context engineering, memory demos

### 3.3 Ollama Framework
- **URL**: https://github.com/ollama/ollama - 173k stars
- **Supports**: Local LLM deployment with agent integrations

---

## 4. KEY THEMES & BEST PRACTICES

### 4.1 System Prompt Structure
- Clear role definition
- Explicit capability boundaries
- Structured output requirements (JSON schemas)
- Error handling and fallback instructions

### 4.2 Agent Architecture Patterns
- **Multi-Agent Coordination**: Role-playing frameworks (CAMEL)
- **Verification**: Multi-stage verification gates (Meta-Agent, GraphFlow)
- **Memory**: Provenance-grounded approaches (Eywa)
- **Harnesses**: Coding harnesses with tools, memory, planning

### 4.3 Instruction Following Best Practices
- High-quality multi-round alignment data
- Continuous prompt monitoring (PRISM approach)
- Product context augmentation (49% improvement per study)

### 4.4 Reliability Engineering
- Contract-driven verification
- Failure classification and recovery
- Test-time compute vs. training-time investment

### 4.5 Production Considerations
- Deterministic outputs with schemas
- Guardrails and acceptance criteria
- Observability and monitoring
- Staged deployment with rollback

---

## 5. NOTABLE arXiv PAPERS FOR PROMPT/AGENT RESEARCH

| Paper | Subject | Key Focus |
|-------|---------|-----------|
| 2308.03688 | AgentBench | LLM evaluation as agents |
| 2303.17760 | CAMEL | Multi-agent cooperation |
| 2605.25233 | Meta-Agent | Multi-agent construction |
| 2605.15665 | PRISM | Prompt reliability |
| 2605.14968 | GraphFlow | Visual workflow verification |
| 2605.20456 | Agentic Agile-V | Software engineering process |
| 2605.30771 | Eywa | Long-term memory |
| 2605.25665 | Meta-Engineering | AI-native production |
| 2605.08112 | Context-Augmented | Code generation context |

---

## 6. REPOSITORIES BY CATEGORY

### Agent Frameworks
- AutoGPT (185k stars)
- Dify (144k stars)
- Flowise (53k stars)
- Google ADK (20k stars)

### Agent Skills/Marketplaces
- Composio (28.6k stars)
- ruflo (57.7k stars)
- agents marketplace (36k stars)

### Tutorials/Education
- Microsoft AI Agents for Beginners (66k stars)
- Hugging Face Agents Course (29k stars)
- agents-towards-production (20k stars)

### Code Agents
- claude-code-best-practice (56k stars)

---

## 7. LINKS SUMMARY

### Papers (PDF available)
- AgentBench: https://arxiv.org/pdf/2308.03688
- CAMEL: https://arxiv.org/pdf/2303.17760
- Meta-Agent: https://arxiv.org/pdf/2605.25233
- PRISM: https://arxiv.org/pdf/2605.15665

### GitHub
- AutoGPT: https://github.com/Significant-Gravitas/AutoGPT
- AutoGPT AGENTS.md: https://raw.githubusercontent.com/Significant-Gravitas/AutoGPT/master/AGENTS.md
- Dify: https://github.com/langgenius/dify
- Ollama: https://github.com/ollama/ollama

### Resources
- Prompt Engineering Institute: https://promptengineering.org/
- Claude Cookbooks: https://github.com/anthropics/claude-cookbooks
- Agentic AI Topic: https://github.com/topics/agentic-ai

---

*Generated: June 2026*
*Research collected for AI agent prompt guidance documentation*
