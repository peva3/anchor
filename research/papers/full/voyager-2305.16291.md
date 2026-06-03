# Voyager: An Open-Ended Embodied Agent with Large Language Models

Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar

## Abstract

We introduce Voyager, the first LLM-powered embodied lifelong learning agent in Minecraft that continuously explores the world, acquires diverse skills, and makes novel discoveries without human intervention. Voyager consists of three key components:

1. **Automatic Curriculum**: Maximizes exploration
2. **Ever-Growing Skill Library**: Stores and retrieves executable code for complex behaviors
3. **Iterative Prompting Mechanism**: Incorporates environment feedback, execution errors, and self-verification for program improvement

Voyager interacts with GPT-4 via blackbox queries, which bypasses the need for model parameter fine-tuning.

## Key Innovations

### Automatic Curriculum
Automatically generates increasingly challenging tasks to maximize exploration and learning.

### Skill Library
Executable code library that:
- Stores complex behaviors
- Enables retrieval for future tasks
- Compounds agent abilities rapidly
- Alleviates catastrophic forgetting

### Iterative Prompting
Incorporates:
- Environment feedback
- Execution errors
- Self-verification

## Results

Voyager shows strong in-context lifelong learning capability:
- 3.3x more unique items collected
- 2.3x longer distances traveled
- 15.3x faster key tech tree milestone unlocking

Compared to prior SOTA methods, Voyager demonstrates superior generalization to new Minecraft worlds.

---

arXiv: https://arxiv.org/abs/2305.16291
Website: https://voyager.minedojo.org/
GitHub: Open-source codebase available
