"""A ReAct-style search agent that answers queries using Tavily web search."""

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


llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def pretty_print(data):
    """Print data as nicely indented JSON."""
    print(json.dumps(data, indent=2, default=str))


def main():
    """Run the agent against a sample query and print the response."""
    print("Hello from agent-lab!")
    llm_input = {"messages": [HumanMessage(content="Search for the latest news on AI")]}
    result = agent.invoke(llm_input)
    pretty_print(result)


if __name__ == "__main__":
    main()
