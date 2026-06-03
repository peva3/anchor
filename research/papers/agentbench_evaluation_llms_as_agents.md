# AgentBench: Evaluating LLMs as Agents

## Paper Information
- **arXiv ID**: 2308.03688
- **Authors**: Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, Jie Tang
- **Institution**: Tsinghua University, The Ohio State University, UC Berkeley
- **Published**: ICLR 2024
- **URL**: https://arxiv.org/abs/2308.03688

## Abstract
The potential of Large Language Model (LLM) as agents has been widely acknowledged. This paper presents AgentBench, a multi-dimensional benchmark consisting of 8 distinct environments to assess LLM-as-Agent's reasoning and decision-making abilities. Evaluation of 29 API-based and open-sourced LLMs shows that top commercial LLMs present strong agent abilities, but there's significant disparity between them and many OSS competitors no larger than 70B.

## Key Findings

### Main Results
1. **Top models like GPT-4 excel** on 6 out of 8 datasets
2. **Significant performance gap** between commercial APIs and OSS models
3. **Poor long-term reasoning, decision-making, and instruction following** are main obstacles

### Key Insights
- Improving instruction following improves agent performance
- High-quality multi-round alignment data helps
- Code training has mixed impacts (improves some tasks, harms others)
- OSS models under 70B lag considerably behind top commercial models

## AgentBench Environments

### Code-grounded (3 environments)
1. **Operating System (OS)** - Ubuntu Docker interaction via terminal
2. **Database (DB)** - SQL interfaces, authentic database operations
3. **Knowledge Graph (KG)** - Freebase interaction, decision-making with incomplete info

### Game-grounded (3 environments)
1. **Digital Card Game (DCG)** - Strategic decision-making (Aquawar)
2. **Lateral Thinking Puzzles (LTP)** - "Yes/No/Irrelevant" question games
3. **House Holding (HH)** - ALFWorld commonsense grounding

### Web-grounded (2 environments)
1. **Web Shopping (WS)** - WebShop simulated e-commerce
2. **Web Browsing (WB)** - Mind2Web general web interaction

## Failure Modes Identified

1. **Context Limit Exceeded (CLE)** - Interaction history exceeds max context length
2. **Invalid Format (IF)** - Agent doesn't follow format instruction
3. **Invalid Action (IA)** - Format correct but action invalid
4. **Task Limit Exceeded (TLE)** - No solution after max rounds / repeated generations

## Evaluation Methodology

### Chain-of-Thought (CoT) Prompting
- Used as basic reasoning strategy
- No multiple trials, repeated generations, or complicated strategies
- Simplest, cheapest, most common deployment approach

### Metrics
- Success Rate (SR) for OS, DB, HH, DCG
- Answer F1 for KG
- Game Progress / Win Rate for LTP, WS
- Step SR for WB

## Key Recommendations

1. **Instruction Following** - Critical for agent performance
2. **Multi-round Alignment Data** - High-quality data improves performance
3. **Code Training** - Double-edged sword; benefits vary by task
4. **Long-term Reasoning** - Needs significant improvement

## GitHub Resource
- Evaluation toolkit: https://github.com/THUDM/AgentBench

## Relevance to AI Agent Prompt Guidance

This benchmark provides essential insights for designing AI agent prompts:
- Highlights importance of clear instruction following
- Shows need for structured output formats
- Demonstrates value of multi-turn conversation capabilities
- Identifies key failure modes to address in prompt design

---
*Extracted from arXiv:2308.03688 - AgentBench: Evaluating LLMs as Agents*
