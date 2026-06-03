# AI Agents for Beginners - AGENTS.md

## Project Overview

This repository contains "AI Agents for Beginners" - a comprehensive educational course teaching everything needed to build AI Agents.

## Key Technologies

- Python 3.12+
- Jupyter Notebooks for interactive learning
- AI Frameworks: Microsoft Agent Framework (MAF)
- Azure AI Services: Microsoft Foundry, Azure AI Foundry Agent Service V2

## Architecture

- Lesson-based structure (00-15+ directories)
- Each lesson contains: README documentation, code samples (Jupyter notebooks), and images
- Multi-language support via automated translation system
- One Python notebook per lesson using Microsoft Agent Framework

## Setup Commands

### Prerequisites
- Python 3.12 or higher
- Azure subscription (for Azure AI Foundry)
- Azure CLI installed and authenticated (`az login`)

### Initial Setup

1. Clone or fork the repository
2. Create and activate Python virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables from `.env.example`

### Required Environment Variables

For **Azure AI Foundry** (Required):
- `AZURE_AI_PROJECT_ENDPOINT` - Azure AI Foundry project endpoint
- `AZURE_AI_MODEL_DEPLOYMENT_NAME` - Model deployment name (e.g., gpt-4o)

For **Azure AI Search** (Lesson 05 - RAG):
- `AZURE_SEARCH_SERVICE_ENDPOINT` - Azure AI Search endpoint
- `AZURE_SEARCH_API_KEY` - Azure AI Search API key

## Development Workflow

### Running Jupyter Notebooks

Each lesson contains multiple Jupyter notebooks for different frameworks:

1. Start Jupyter: `jupyter notebook`
2. Navigate to a lesson directory (e.g., `01-intro-to-ai-agents/code_samples/`)
3. Open and run notebooks:
   - `*-python-agent-framework.ipynb` - Using Microsoft Agent Framework (Python)
   - `*-dotnet-agent-framework.ipynb` - Using Microsoft Agent Framework (.NET)

## Code Style

- Python 3.12+
- Standard Python PEP 8 conventions
- Clear markdown cells in notebooks
- Imports grouped by standard library, third-party, local

## Build and Deployment

This is an educational repository - no deployment process. Users:
1. Fork or clone the repository
2. Run notebooks locally or in GitHub Codespaces
3. Learn by modifying and experimenting with examples

## Pull Request Guidelines

- Test affected notebooks completely
- Update README.md if adding new concepts
- Avoid committing `.env` files
- Don't commit `venv/` or `__pycache__/` directories

## Learning Path

1. **00-course-setup** - Start here for environment setup
2. **01-intro-to-ai-agents** - Understand AI agent fundamentals
3. **02-explore-agentic-frameworks** - Learn about different frameworks
4. **03-agentic-design-patterns** - Core design patterns
5. Continue through numbered lessons sequentially

---

Source: https://github.com/microsoft/ai-agents-for-beginners
