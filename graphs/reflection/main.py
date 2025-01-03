from typing import List, Sequence

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from graphs.reflection.chains import generation_chain, reflection_chain

REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: Sequence[BaseMessage]):
    return generation_chain.invoke({"messages": state})


def reflection_node(messages: Sequence[BaseMessage]):
    res = reflection_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]


# Create graph without nodes first, then add them
builder = MessageGraph()
builder.add_node(REFLECT, reflection_node)
builder.add_node(GENERATE, generation_node)

builder.set_entry_point(GENERATE)


def should_continue(state: List[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT


builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()

graph.get_graph().draw_mermaid_png(
    output_file_path="graphs/reflection/reflection_graph.png"
)


if __name__ == "__main__":
    user_input = input("Enter your tweet: ")
    input = HumanMessage(
        content=user_input
    )

    res = graph.invoke([input])
    print(res)
