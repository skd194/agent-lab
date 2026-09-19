# agent-lab

A lab environment for experimenting with LLM agents using [LangChain](https://python.langchain.com/), managed with [uv](https://docs.astral.sh/uv/).

> This project uses the **OpenAI** integration as an example. LangChain is provider-agnostic — you can swap in any supported provider, or run a local model with [Ollama](https://python.langchain.com/docs/integrations/chat/ollama/). Just install the matching integration instead of `langchain-openai`.

## Requirements

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) package manager

## Setting Up a New Project from Scratch

### 1. Install uv

```bash
pip3 install uv
```

### 2. Initialize a Python project

```bash
uv init
```

### 3. Add LangChain

```bash
uv add langchain
```

### 4. Add your LLM provider integration

Install the integration for the provider you want to use. This project uses OpenAI:

```bash
uv add langchain-openai
```

> Using a different provider? Check the [LangChain provider docs](https://python.langchain.com/docs/integrations/providers/) and install the matching package instead — for example `langchain-ollama` to run a local model.

### 5. Load environment variables with python-dotenv

```bash
uv add python-dotenv
```

Then create a `.env` file in the project root for your credentials:

```env
OPENAI_API_KEY=your-api-key-here
```

> **Note:** `.env` is git-ignored — never commit your API keys. (Local models via Ollama typically need no API key.)

### 6. Add formatting tools

```bash
uv add black isort
```

These keep the code consistently styled so you never format by hand or debate style:

- **`black`** — an opinionated code formatter. It rewrites your files to one consistent style (line length, spacing, quotes, wrapping), so all code looks the same and diffs stay clean.
- **`isort`** — sorts and groups your imports (standard library → third-party → local), which `black` intentionally leaves untouched.

They cover separate concerns and complement each other. Add the following to `pyproject.toml` so the two tools agree and produce no warnings:

```toml
[tool.black]
target-version = ["py311"]

[tool.isort]
profile = "black"
```

> `target-version` pins Black to your Python version, and `profile = "black"` makes isort format imports in a way Black accepts, so they don't undo each other.

### 7. Run the project

```bash
uv run main.py
```

## Working with an Existing Project

If you are cloning this project (or any uv project) that already has its dependencies defined in `pyproject.toml`, you don't need to add packages one by one. Just sync:

```bash
git clone <repository-url>
cd agent-lab
uv sync
```

`uv sync` installs everything from `pyproject.toml` / `uv.lock` into the virtual environment. Then create your `.env` file (step 5 above) and run:

```bash
uv run main.py
```

## Dependencies

| Package            | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| `langchain`        | Core framework for building LLM applications     |
| `langchain-openai` | OpenAI provider integration (swap per provider)  |
| `python-dotenv`    | Loads environment variables from the `.env` file |
| `black`            | Code formatter                                   |
| `isort`            | Import sorter                                     |

## Code Formatting

Format code and sort imports before committing:

```bash
uv run black .
uv run isort .
```
