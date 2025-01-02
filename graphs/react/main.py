from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph

from graphs.react.nodes import run_agent_reasoning_engine, execute_tool
from graphs.react.state import AgentState

AGENT_REASON = "agent_reason"
ACT = "act"

def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT
    
flow = StateGraph(AgentState)

flow.add_node(AGENT_REASON, run_agent_reasoning_engine)
flow.add_node(ACT, execute_tool)

flow.add_conditional_edges(AGENT_REASON, should_continue)

flow.add_edge(ACT, AGENT_REASON)

flow.set_entry_point(AGENT_REASON)

graph = flow.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graphs/react/react_graph.png")

res = graph.invoke(
    input={
        "input": "what is the weather in SF? write it and then Triple it."
    }
)

print(
    res["agent_outcome"].return_values["output"]
)