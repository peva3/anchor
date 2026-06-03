# AutoGen - Multi-Agent AI Applications Framework

## Overview

AutoGen is a framework for creating multi-agent AI applications that can act autonomously or work alongside humans.

> **Note**: AutoGen is now in maintenance mode. For new projects, consider [Microsoft Agent Framework](https://github.com/microsoft/agent-framework).

## Architecture

The autogen framework uses a layered and extensible design:

### Core API (`autogen-core`)
Implements message passing, event-driven agents, and local and distributed runtime for flexibility and power. Also supports cross-language support for .NET and Python.

### AgentChat API (`autogen-agentchat`)
Implements a simpler but opinionated API for rapid prototyping. Built on top of the Core API and supports common multi-agent patterns.

### Extensions API (`autogen-ext`)
Enables first- and third-party extensions expanding framework capabilities. Supports specific LLM clients (OpenAI, AzureOpenAI) and capabilities like code execution.

## Installation

```bash
# Install AgentChat and OpenAI client
pip install -U "autogen-agentchat" "autogen-ext[openai]"

# Install AutoGen Studio for no-code GUI
pip install -U "autogenstudio"
```

## Quickstart

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4.1")
    agent = AssistantAgent("assistant", model_client=model_client)
    print(await agent.run(task="Say 'Hello World!'"))
    await model_client.close()

asyncio.run(main())
```

## Multi-Agent Example

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool

# Create expert agents
math_agent = AssistantAgent("math_expert", system_message="You are a math expert.")
chemistry_agent = AssistantAgent("chemistry_expert", system_message="You are a chemistry expert.")

# Create tools from agents
math_agent_tool = AgentTool(math_agent, return_value_as_last_message=True)
chemistry_agent_tool = AgentTool(chemistry_agent, return_value_as_last_message=True)

# Create main agent with access to expert tools
agent = AssistantAgent(
    "assistant",
    system_message="You are a general assistant. Use expert tools when needed.",
    tools=[math_agent_tool, chemistry_agent_tool],
    max_tool_iterations=10,
)
```

## Developer Tools

- **AutoGen Studio**: No-code GUI for building multi-agent applications
- **AutoGen Bench**: Benchmarking suite for evaluating agent performance

## Resources

- Documentation: https://microsoft.github.io/autogen/
- Discord: https://aka.ms/autogen-discord
- GitHub Discussions: https://github.com/microsoft/autogen/discussions

---

Source: https://github.com/microsoft/autogen
