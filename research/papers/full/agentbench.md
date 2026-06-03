# AgentBench: Evaluating LLMs as Agents

**arXiv:** https://arxiv.org/abs/2308.03688
**Published:** ICLR 2024
**Authors:** Xiao Liu, Hao Yu, Hanchen Zhang, et al. (23 authors from Tsinghua, Ohio State, UC Berkeley)

## Abstract

AgentBench is a multi-dimensional benchmark for evaluating LLMs as agents on challenging tasks in interactive environments. It consists of 8 distinct environments (Operating System, Database, Knowledge Graph, Digital Card Game, Lateral Thinking Puzzles, House Holding, Web Shopping, Web Browsing) to assess reasoning and decision-making abilities.

Key finding: **Poor instruction following is a main obstacle for developing usable LLM agents.** Top commercial LLMs (GPT-4) show strong agent abilities, but there's a significant performance gap between them and open-source models.

## Key Findings

1. **Instruction Following is Critical** - Main differentiator between models. Poor instruction following causes most agent failures.

2. **Long-term Reasoning & Decision-Making** - Models struggle with multi-round interactions and sustained reasoning.

3. **Code Training Impact** - Training on code has **ambivalent impacts**: improves some agent tasks but harms others.

4. **High-quality Alignment Data** - Training on GPT-4-quality multi-round alignment data improves agent performance.

5. **Context Limit Issues** - Models tend to repeat previous content when approaching context limits.

## Evaluation Results

- **29 LLMs tested** (API-based and open-source)
- **GPT-4 achieved best performance** on 6/8 environments (78% on House Holding)
- **Significant gap** between top commercial LLMs and OSS models ≤70B parameters
- **All OSS models scored below 1.0** on AgentBench overall score vs GPT-4's 4.01

## The 8 Environments

### Code-grounded
1. **Operating System** - Ubuntu Docker terminal interaction
2. **Database** - SQL interface operation
3. **Knowledge Graph** - Freebase-style graph queries

### Game-grounded
4. **Digital Card Game** (Aquawar) - Strategic card game
5. **Lateral Thinking Puzzles** - Yes/No puzzle solving
6. **House Holding** (ALFWorld) - Commonsense household tasks

### Web-grounded
7. **Web Shopping** (WebShop) - E-commerce interaction
8. **Web Browsing** (Mind2Web) - General web navigation

## Failure Modes Identified

1. **Context Limit Exceeded (CLE)** - Interaction history exceeds max context
2. **Invalid Format (IF)** - Agent doesn't follow output format instructions
3. **Invalid Action (IA)** - Format correct but action is invalid
4. **Task Limit Exceeded (TLE)** - No solution after max rounds / repeated generations

## Implications for AGENTS.md Design

1. **Clear, precise instructions** - Ambiguity leads to format failures
2. **Explicit action schemas** - Define exact output formats
3. **Single-turn focus where possible** - Reduce multi-round complexity
4. **Error recovery patterns** - Include retry/validation mechanisms
5. **Code-style examples** - Show exact expected outputs

## Repository

https://github.com/THUDM/AgentBench