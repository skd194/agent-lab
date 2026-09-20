from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
import json



llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [TavilySearch()]
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
