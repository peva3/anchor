# ChatDev: Communicative Agents for Software Development

Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, Maosong Sun

Tsinghua University

## Abstract

Software development is a complex task that necessitates cooperation among multiple members with diverse skills. Numerous studies used deep learning to improve specific phases in a waterfall model, such as design, coding, and testing. However, the deep learning model in each phase requires unique designs, leading to technical inconsistencies across various phases, which results in a fragmented and ineffective development process. In this paper, we introduce ChatDev, a chat-powered software development framework in which specialized agents driven by large language models (LLMs) are guided in what to communicate (via chat chain) and how to communicate (via communicative dehallucination). These agents actively contribute to the design, coding, and testing phases through unified language-based communication, with solutions derived from their multi-turn dialogues.

## Key Features

### Chat Chain
ChatDev segments the software development process into three sequential phases: design, coding, and testing. Each phase is further broken down into smaller subtasks with multi-turn communications between different roles.

### Communicative Dehallucination
To minimize coding hallucinations, ChatDev includes a mechanism where agents request more specific details before giving direct responses, enabling precise information exchange for effective solution optimization.

## Architecture

The framework integrates multiple "software agents" with various social roles:
- Requirements analysts
- Professional programmers
- Test engineers

Each subtask involves two agents: an instructor (ℐ) who initiates instructions and an assistant (𝒜) who responds with appropriate solutions.

## Evaluation Results

ChatDev outperforms baseline methods across all metrics:
- Completeness: 0.5600
- Executability: 0.8800
- Consistency: 0.8021
- Quality: 0.3953

Compared to GPT-Engineer and MetaGPT, ChatDev shows significant improvements in software development tasks.

---

arXiv: https://arxiv.org/abs/2307.07924
GitHub: https://github.com/OpenBMB/ChatDev
Accepted at ACL 2024
