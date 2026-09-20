from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

tavily_client = TavilyClient()

import json


@tool
def search_tool(query: str) -> str:
    """
    Tool that searches over internet and returns the results.
    Args:
        query (str): The search query.
    Returns:
        str: The search results.
    """
    print(f"Searching for {query}")
    return tavily_client.search(query)


llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [search_tool]
agent = create_agent(model=llm, tools=tools)


def pretty_print(data):
    print(json.dumps(data, indent=2, default=str))


def main():
    print("Hello from agent-lab!")
    llm_input = {"messages": [HumanMessage(content="Search for the latest news on AI")]}
    result = agent.invoke(llm_input)
    pretty_print(result)


if __name__ == "__main__":
    main()
