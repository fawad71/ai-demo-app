from langgraph.prebuilt.tool_executor import ToolExecutor

from graphs.react.react import agent, tools
from graphs.react.state import AgentState

def run_agent_reasoning_engine(state: AgentState):
    agent_outcome = agent.invoke(state)
    return {"agent_outcome": agent_outcome}

tool_executor = ToolExecutor(tools)

def execute_tool(state: AgentState):
    agent_action = state["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, output)]}