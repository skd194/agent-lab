"""A ReAct-style search agent that answers queries using Tavily web search.

This is the project's *original* Tavily/LangChain agent (§8). It is preserved
here rather than recreated. The only structural change from the standalone
script is that the agent is now built lazily via :func:`build_search_agent`
instead of at import time, so the module can be imported safely in demo mode
or environments without API keys. Running the module directly still behaves
exactly as before.
"""

import json

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

load_dotenv()


class Source(BaseModel):
    """Schema for a source used by the agent"""

    url: str = Field(..., description="The URL of the source")


class AgentResponse(BaseModel):
    """Schema for the agent's response"""

    answer: str = Field(
        ..., description="The answer provided by the agent to the query"
    )
    sources: list[Source] = Field(
        description="List of sources used by the agent to generate the answer",
        default_factory=list,
    )


def build_search_agent(model: str = "gpt-4o", temperature: float = 0.0):
    """Build the Tavily-backed ReAct agent.

    Constructed lazily so importing this module never requires API keys.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    tools = [TavilySearch()]
    return create_agent(model=llm, tools=tools, response_format=AgentResponse)


def build_raw_tavily_tool(**kwargs) -> TavilySearch:
    """Return a bare TavilySearch tool for raw, structured result retrieval."""
    return TavilySearch(**kwargs)


def pretty_print(data):
    """Print data as nicely indented JSON."""
    print(json.dumps(data, indent=2, default=str))


def main():
    """Run the agent against a sample query and print the response."""
    print("Hello from agent-lab!")
    agent = build_search_agent()
    llm_input = {"messages": [HumanMessage(content="Search for the latest news on AI")]}
    result = agent.invoke(llm_input)
    pretty_print(result)


if __name__ == "__main__":
    main()
