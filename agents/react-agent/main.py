from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, tool
from langchain_openai import ChatOpenAI


@tool
def get_text_length(text: str) -> int:
    """Returns the length of the text by character count"""
    return len(text)


@tool
def calculate_math(expression: str) -> float:
    """Evaluates a mathematical expression. Example: '5 + 5 * 2'"""
    try:
        # Using eval() safely with only mathematical expressions
        return eval(expression, {"__builtins__": {}})
    except:
        return "Invalid mathematical expression"


@tool
def capitalize_text(text: str) -> str:
    """Capitalizes the first letter of each word in the text"""
    return text.title()


@tool
def celsius_to_fahrenheit(celsius: float) -> float:
    """Converts temperature from Celsius to Fahrenheit"""
    return (float(celsius) * 9 / 5) + 32


if __name__ == "__main__":
    print("Start...")

    llm = ChatOpenAI(model="gpt-4o-mini")

    tools = [get_text_length, calculate_math, capitalize_text, celsius_to_fahrenheit]

    react_prompt = hub.pull("common-react_agent")

    agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Get input from user
    user_input = input("Ask Me: ")

    result = agent_executor.invoke(input={"input": user_input})

    print(f"Result: {result['output']}")
