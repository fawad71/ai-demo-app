from typing import List, Sequence, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Import all available graphs
from graphs.async_graph.main import graph as async_graph
from graphs.conditional_async.main import graph as conditional_async_graph
from graphs.email_agent.main import graph as email_agent_graph
from graphs.HITL_memory.main import graph as human_memory_graph
from graphs.rag.graph.graph import app as rag_graph
from graphs.react.main import graph as react_graph
from graphs.reflection.main import graph as reflection_graph
from graphs.reflexion.main import graph as reflexion_graph

# Define available routes
ROUTES = {
    "async": async_graph,
    "conditional_async": conditional_async_graph,
    "email_agent": email_agent_graph,
    "human_memory": human_memory_graph,
    "rag": rag_graph,
    "react": react_graph,
    "reflection": reflection_graph,
    "reflexion": reflexion_graph
}

# Define the prompt template
router_template = ChatPromptTemplate.from_messages([
    ("system", """You are a routing assistant that analyzes prompts and determines the most appropriate implementation to use.
    
Available implementations:
1. async - for asynchronous operations
2. conditional_async - for conditional async flows
3. email_agent - for email related tasks
4. human_memory - for tasks requiring human interaction and memory
5. rag - for retrieval augmented generation

Output only one of: async, conditional_async, email_agent, human_memory, rag, react, reflection, reflexion"""),
    ("user", "{prompt}")
])

# Create the chain lazily
def get_router_chain():
    return router_template | ChatOpenAI(model="gpt-4o-mini", temperature=0)

def router_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Routes to appropriate implementation based on prompt analysis"""
    initial_prompt = state["messages"][0].content
    router_chain = get_router_chain()
    route = router_chain.invoke({"prompt": initial_prompt}).content.strip().lower()
    return {"route": route}

def process_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Processes the request using the selected implementation"""
    route = state["route"]
    
    if route not in ROUTES:
        return AIMessage(content=f"Error: Invalid route '{route}'")
    
    # Process through selected graph
    graph = ROUTES[route]
    return graph.invoke(state["messages"])

# Build the router graph with custom state
builder = StateGraph(Dict[str, Any])

# Add nodes
builder.add_node("router", router_node)
builder.add_node("process", process_node)

# Set entry point directly to router
builder.set_entry_point("router")

# Add edges
builder.add_edge("router", "process")
builder.add_edge("process", END)

# Compile the graph
graph = builder.compile()

# Uncomment to generate visualization
graph.get_graph().draw_mermaid_png(
    output_file_path="graphs/router/router_graph.png"
)