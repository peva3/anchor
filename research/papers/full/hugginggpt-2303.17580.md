# HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face

Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, Yueting Zhuang

## Abstract

Solving complicated AI tasks with different domains and modalities is a key step toward artificial general intelligence. While there are numerous AI models available for various domains and modalities, they cannot handle complicated AI tasks autonomously. Considering large language models (LLMs) have exhibited exceptional abilities in language understanding, generation, interaction, and reasoning, we advocate that LLMs could act as a controller to manage existing AI models to solve complicated AI tasks, with language serving as a generic interface to empower this.

## Architecture

HuggingGPT uses ChatGPT as a controller to:

1. **Task Planning**: When receiving a user request, conduct task planning
2. **Model Selection**: Select models according to their function descriptions available in Hugging Face
3. **Execution**: Execute each subtask with the selected AI model
4. **Summarization**: Summarize the response according to the execution results

## Key Features

- Leverages strong language capability of ChatGPT
- Utilizes abundant AI models in Hugging Face
- Tackles wide range of sophisticated AI tasks spanning different modalities and domains
- Achieves impressive results in language, vision, speech, and other challenging tasks

## Significance

HuggingGPT paves a new way towards the realization of artificial general intelligence by connecting LLMs with specialized models through a unified language interface.

---

arXiv: https://arxiv.org/abs/2303.17580
