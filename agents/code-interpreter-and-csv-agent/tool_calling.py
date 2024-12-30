from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' times 'y'."""
    print(f"Multiplying {x} times {y}")
    return x * y


if __name__ == "__main__":
    print("Hello Tool Calling")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you're a helpful assistant"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    tools = [TavilySearchResults(), multiply]
    llm = ChatOpenAI(model="gpt-4o")

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    res = agent_executor.invoke(
        {
            "input": "what is 2 multiply by 10",
        }
    )

    print(res)
