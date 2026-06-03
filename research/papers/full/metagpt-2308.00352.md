# MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework

Sirui Hong, Mingchen Zhuge, Jiaqi Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber

DeepWisdom, King Abdullah University of Science and Technology, Xiamen University, The Chinese University of Hong Kong, Shenzhen, Nanjing University, University of Pennsylvania, UC Berkeley,IDSIA/USI/SUPSI

## Abstract

Remarkable progress has been made on automated problem solving through societies of agents based on large language models (LLMs). Existing LLM-based multi-agent systems can already solve simple dialogue tasks. Solutions to more complex tasks, however, are complicated through logic inconsistencies due to cascading hallucinations caused by naively chaining LLMs. Here we introduce MetaGPT, an innovative meta-programming framework incorporating efficient human workflows into LLM-based multi-agent collaborations. MetaGPT encodes Standardized Operating Procedures (SOPs) into prompt sequences for more streamlined workflows, thus allowing agents with human-like domain expertise to verify intermediate results and reduce errors. MetaGPT utilizes an assembly line paradigm to assign diverse roles to various agents, efficiently breaking down complex tasks into subtasks involving many agents working together.

## Key Innovations

### Standardized Operating Procedures (SOPs)
MetaGPT encodes SOPs into prompt sequences, allowing agents with human-like domain expertise to verify intermediate results and reduce errors.

### Assembly Line Paradigm
MetaGPT assigns diverse roles to various agents, efficiently breaking down complex tasks into subtasks involving many agents working together.

### Structured Communication
Unlike unconstrained natural language communication, MetaGPT uses structured communication interfaces with role-specific outputs.

### Executable Feedback Mechanism
After generating initial code, the Engineer agent runs and checks for errors. If errors occur, the agent checks past messages and debugs the code iteratively.

## Roles in MetaGPT

1. **Product Manager**: Conducts business-oriented analysis and creates Product Requirements Documents (PRDs)
2. **Architect**: Translates requirements into system design components
3. **Project Manager**: Handles task distribution
4. **Engineer**: Executes designated classes and functions
5. **QA Engineer**: Formulates test cases for code quality

## Performance

On HumanEval, MetaGPT achieves 85.9% Pass@1
On MBPP, MetaGPT achieves 87.7% Pass@1

Compared to ChatDev, MetaGPT shows improvements in executability (3.75 vs 2.25) and overall code quality.

---

arXiv: https://arxiv.org/abs/2308.00352
GitHub: https://github.com/geekan/MetaGPT
