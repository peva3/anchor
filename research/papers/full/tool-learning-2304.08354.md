# Tool Learning with Foundation Models

Yujia Qin, Shengding Hu, Yankai Lin, Weize Chen, Ning Ding, Ganqu Cui, Zheni Zeng, Yufei Huang, Chaojun Xiao, Chi Han, Yi Ren Fung, Yusheng Su, Huadong Wang, Cheng Qian, Runchu Tian, Kunlun Zhu, Shihao Liang, Xingyu Shen, Bokai Xu, Zhen Zhang, Yining Ye, Bowen Li, Ziwei Tang, Jing Yi, Yuzhang Zhu, Zhenning Dai, Lan Yan, Xin Cong, Yaxi Lu, Weilin Zhao, Yuxiang Huang, Junxi Yan, Xu Han, Xian Sun, Dahai Li, Jason Phang, Cheng Yang, Tongshuang Wu, Heng Ji, Zhiyuan Liu, Maosong Sun

Tsinghua University and others

## Abstract

Humans possess an extraordinary ability to create and utilize tools, allowing them to overcome physical limitations and explore new frontiers. With the advent of foundation models, AI systems have the potential to be equally adept in tool use as humans. This paradigm, i.e., tool learning with foundation models, combines the strengths of specialized tools and foundation models to achieve enhanced accuracy, efficiency, and automation in problem-solving.

## Framework

The tool learning framework comprises:

### Components
1. **Tool Set**: Specialized tools for specific tasks
2. **Environment**: Context where tools are deployed
3. **Controller**: Typically a foundation model that orchestrates tool usage
4. **Perceiver**: Mechanism to interpret feedback
5. **Human**: End user or overseer

### General Procedure
1. Understanding user instruction (intent understanding)
2. Decomposing complex tasks into subtasks
3. Dynamically adjusting plans through reasoning
4. Selecting appropriate tools for each sub-task
5. Executing and verifying results

## Key Topics Covered

### Training Models for Tool Learning
- Learning from demonstrations (supervised, semi-supervised, self-supervised)
- Learning from feedback (reinforcement learning, environment feedback, human feedback)
- Generalizable tool learning

### Applications
The paper experiments with 18 representative tools showing the potential of current foundation models in skillfully utilizing tools.

### Discussion Topics
- Safe and trustworthy tool learning
- Tool learning for large complex systems
- From tool user to tool maker: AI's evolutionary role
- From general intelligence to personalized intelligence
- Tool learning and embodied learning
- Knowledge conflicts in tool augmentation

---

arXiv: https://arxiv.org/abs/2304.08354
GitHub: https://github.com/OpenBMB/BMTools
