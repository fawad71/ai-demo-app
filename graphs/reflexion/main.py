from typing import List

from chains import first_responder, revisor
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph
from tool_executor import tool_node

MAX_ITERATIONS = 2

builder = MessageGraph()
builder.add_node("draft", first_responder)
builder.add_node("execute_tools", tool_node)
builder.add_node("revise", revisor)

builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")


def event_loop(state: List[BaseMessage]) -> str:
    num_iterations = sum(isinstance(item, ToolMessage) for item in state)
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"


builder.add_conditional_edges("revise", event_loop)
builder.set_entry_point("draft")
graph = builder.compile()

# graph.get_graph().draw_mermaid_png(
#     output_file_path="graphs/reflexion/reflexion_graph.png"
# )

res = graph.invoke(
    "what are the benefits of drinking water?"
)

print(res[-1].tool_calls[0]["args"]["answer"])
print(res)
