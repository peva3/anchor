# AgentBench: Evaluating LLMs as Agents

Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, Jie Tang

Tsinghua University, The Ohio State University, UC Berkeley

## Abstract

The potential of Large Language Model (LLM) as agents has been widely acknowledged recently. Thus, there is an urgent need to quantitatively evaluate LLMs as agents on challenging tasks in interactive environments. We present AgentBench, a multi-dimensional benchmark that consists of 8 distinct environments to assess LLM-as-Agent's reasoning and decision-making abilities. Our extensive test over 29 API-based and open-sourced (OSS) LLMs shows that, while top commercial LLMs present a strong ability of acting as agents in complex environments, there is a significant disparity in performance between them and many OSS competitors that are no larger than 70B. We identify the typical reasons of failures in environments and LLMs, showing that poor long-term reasoning, decision-making, and instruction following abilities are the main obstacles for developing usable LLM agents. Improving instruction following and training on high quality multi-round alignment data could improve agent performance. And different from existing assumptions, training on code present ambivalent impacts on different agent tasks.

## 1 Introduction

Intelligent agents and autonomous entities that are capable of decision-making and action execution in particular environments have been key concepts of artificial intelligence (AI) historically. Notwithstanding substantial advancements in deep learning algorithms applied in both computer vision and natural language processing (NLP), their potential for developing efficient and practically usable assisting agents remains largely unexplored.

The advent of Large Language Models (LLMs) such as GPT-4, has brought plenty of new opportunities to this realm. Through extensive alignment training, LLMs have not only mastered traditional NLP tasks but also showcased an impressive ability to comprehend human intent and execute instructions. This has spurred the development of various LLM-based applications for autonomous goal completion (like AutoGPT, BabyAGI, AgentGPT) as well as LLM agents situated in social and game contexts.

Despite these advancements, the lack of a systematic and standard benchmark to evaluate LLM-as-Agent presents a critical challenge. To address these challenges, we introduce AgentBench, a multi-dimensional benchmark designed to evaluate LLM-as-Agent across a spectrum of different environments.

## 2 LLM-as-Agent: Definition and Preliminary

The interactive evaluation of LLM-as-Agent could be regarded as a Partially Observable Markov Decision Process (𝒮,𝒜,𝒯,ℛ,𝒰,𝒪), which comprises state space 𝒮, action space 𝒜, transition function 𝒯:𝒮×𝒜→𝒮, reward assigning function ℛ, task instruction space 𝒰, and observation space 𝒪.

Chain-of-Thought (CoT) and Other Reasoning Strategies: Since LLM-as-Agent requires LLMs' strong reasoning ability, CoT, which has been considered a de facto strategy in related evaluation together with actions, is also adopted in AgentBench.

## 3 Composition of AgentBench

AgentBench encompasses eight distinct environments, which could be categorized into three types of groundings:

### Code-grounded Environments
- Operating System (OS): Evaluate LLMs in genuine interactive bash environments
- Database (DB): Examine LLMs' abilities to operate on real databases via SQL
- Knowledge Graph (KG): Assess decision-making abilities of AI agents in partially observable KG environments

### Game-grounded Environments
- Digital Card Game (DCG): Test models' understanding of game rules, operating logic, and strategic decisions
- Lateral Thinking Puzzles (LTP): Assess lateral reasoning abilities through strategic questioning
- House Holding (HH, ALFWorld): Accomplish tasks in physical house-holding environments

### Web-grounded Environments
- Web Shopping (WebShop): Evaluate language agents on online shopping tasks
- Web Browsing (Mind2Web): General benchmark for web agents capable of executing intricate tasks

## 4 Evaluation

We extensively evaluate 29 LLMs, including API-based commercial models and open-sourced LLMs. Our results reveal that top-tier models like GPT-4 are capable of handling a wide array of real-world tasks. However, we also note a significant performance gap between these top-tier models and their OSS competitors.

Key findings:
- GPT-4 achieves best performance on 6 out of 8 datasets
- Claude-2 and Claude follow GPT-4 but quite outperform GPT-3.5-turbo
- All API-based LLMs have an AgentBench overall score above 1.00
- OSS LLMs lag considerably despite recent success on several benchmarks

## 5 Related Work

Related work includes text-based game environments for language agent evaluation, embodied agents with multi-modal simulators, and various approaches to LLM-based autonomous agents.

## 6 Conclusion

We introduce AgentBench, the first systematic benchmark to evaluate LLM-as-Agent on a wide array of real-world challenges and 8 distinct environments. We perform a thorough evaluation of 29 different LLMs, uncovering a significant performance gap between leading API-based commercial LLMs and many OSS models. We also quantitatively analyze the reasons for failures in existing LLM agents and highlight directions for improvement.

---

arXiv: https://arxiv.org/abs/2308.03688
GitHub: https://github.com/THUDM/AgentBench
