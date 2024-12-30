from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from langchain import hub


class AgentManager:
    def __init__(self):
        self.llm4o = ChatOpenAI(temperature=0, model="gpt-4o")
        self.llm4oMini = ChatOpenAI(temperature=0, model="gpt-4o-mini")
        self.python_agent = self._setup_python_agent()
        self.csv_agent = self._setup_csv_agent()
        self.router_agent = self._setup_router_agent()

    def _setup_python_agent(self):
        python_tools = [PythonREPLTool()]

        REPLPrompt = hub.pull("code-interpreter-and-csv-agent-repl")

        agent = create_tool_calling_agent(
            llm=self.llm4oMini, tools=python_tools, prompt=REPLPrompt
        )
        return AgentExecutor(agent=agent, tools=python_tools, verbose=True)

    def _setup_csv_agent(self):
        return create_csv_agent(
            llm=self.llm4oMini,
            path="agents/code-interpreter-and-csv-agent/episode_info.csv",
            verbose=True,
            allow_dangerous_code=True,
        )

    def _setup_router_agent(self):
        router_tools = [
            Tool(
                name="Python_Agent",
                func=lambda x: self.python_agent.invoke({"input": x}),
                description="Useful when you need to transform natural language to python and execute the python code, returning the results of the code execution. DOES NOT ACCEPT CODE AS INPUT",
            ),
            Tool(
                name="CSV_Agent",
                func=self.csv_agent.invoke,
                description="Useful when you need to answer question over episode_info.csv file, takes an input the entire question and returns the answer after running pandas calculations",
            ),
        ]

        RouterPrompt = hub.pull("code-interpreter-and-csv-agent-router")

        agent = create_tool_calling_agent(
            llm=self.llm4oMini, tools=router_tools, prompt=RouterPrompt
        )
        return AgentExecutor(agent=agent, tools=router_tools, verbose=True)


def main():
    print("Start...")
    agent_manager = AgentManager()

    # agent_manager.router_agent.invoke({"input": "in episode_info.csv file which season has the most episodes?"})
    agent_manager.router_agent.invoke({"input": "Generate and save in current working directory 15 qrcodes that point to `https://github.com/fawad71/ai-demo-app`"})


if __name__ == "__main__":
    main()
