from langchain import hub
from langchain.agents import create_react_agent, tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

react_prompt: PromptTemplate = hub.pull("common-react_agent")

@tool
def triple(num: float) -> float:
    """Triple the number"""
    return float(num) * 3

tools = [TavilySearchResults(max_results=1), triple]

llm=ChatOpenAI(model="gpt-4o-mini")

agent = create_react_agent(llm, tools, react_prompt)

