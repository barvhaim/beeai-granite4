# BeeAI Granite 4

An interactive AI agent powered by IBM Granite 4 micro model and the BeeAI Framework.

## Overview

This project implements a ReAct (Reasoning and Acting) agent that can interact with users through a console interface and use tools to answer questions and perform tasks.

## Features

- **Interactive Chat**: Console-based chat interface with colored output
- **Tool Integration**: Weather information via OpenMeteo
- **Event Streaming**: Real-time visibility into agent reasoning process
- **Memory Management**: Token-based memory for conversation context
- **Error Handling**: Robust retry mechanisms and error reporting

## Prerequisites

- Python >=3.11.13
- [uv](https://github.com/astral-sh/uv) package manager
- [Ollama](https://ollama.ai/) with Granite 4 micro model

### Install Ollama and Granite 4

```bash
# Install Ollama (if not already installed)
# Visit https://ollama.ai/ for installation instructions

# Pull the Granite 4 micro model
ollama pull granite4:micro
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/barvhaim/beeai-granite4.git
cd beeai-granite4
```

2. Install dependencies using uv:
```bash
uv sync
```

3. (Optional) Create a `.env` file for environment variables:
```bash
CODE_INTERPRETER_URL=http://localhost:8000  # If using code interpreter
```

## Usage

Start the interactive agent:

```bash
python agent.py
```

Once started:
- Type your questions or requests at the prompt
- Type 'q' to quit
- The agent will use available tools to answer your questions

Example interaction:
```
User : What's the weather like in San Francisco?
Agent >: [Agent processes using OpenMeteoTool]
Agent >: The current weather in San Francisco is...
```

## Development

### Code Formatting
```bash
black .
```

### Linting
```bash
pylint agent.py helpers/
```

### Adding Dependencies
```bash
uv add <package-name>
```

## Project Structure

```
beeai-granite4/
agent.py          # Main agent implementation
helpers/
__init__.py
io.py         # Console reader utilities
pyproject.toml    # Project configuration
README.md
```

## Configuration

The agent is configured with:
- **Max retries per step**: 3
- **Total max retries**: 10
- **Max iterations**: 20
- **Temperature**: 0 (deterministic responses)

## License

See LICENSE file for details.
