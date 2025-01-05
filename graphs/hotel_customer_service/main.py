"""Hotel Customer Service Chat Agent"""

from typing import cast
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from copilotkit.langchain import copilotkit_emit_message
from pydantic import BaseModel, Field
from graphs.hotel_customer_service.state import HotelCustomerServiceState

MENU = """
1. Classic Burger - $12.99
   Juicy beef patty with fresh vegetables
2. Caesar Salad - $8.99
   Fresh romaine lettuce with caesar dressing
3. Chocolate Cake - $6.99
   Rich chocolate cake with vanilla frosting
"""

class MenuAction(BaseModel):
    """Determine the menu-related action from user message"""
    action: str = Field(..., description="One of: show_menu, add_to_cart, show_cart")

async def process_message(state: HotelCustomerServiceState, config: RunnableConfig):
    """Process user messages."""
    last_message = cast(HumanMessage, state["messages"][-1])
    
    model = ChatOpenAI(model="gpt-4", temperature=0).bind_tools([MenuAction])
    response = await model.ainvoke([
        SystemMessage(content="You are a hotel service chatbot. Determine if the user wants to: show_menu, add_to_cart, or show_cart"),
        last_message
    ], config)

    tool_calls = cast(AIMessage, response).tool_calls
    if not tool_calls:
        await copilotkit_emit_message(config, "I can show you our menu or help with your order. Try saying 'show menu'.")
        return state

    action = tool_calls[0]["args"]["action"]

    if action == "show_menu":
        await copilotkit_emit_message(config, f"Here's our menu:{MENU}")
    elif action == "add_to_cart":
        await copilotkit_emit_message(config, "I've noted down your order. What else would you like?")
    elif action == "show_cart":
        await copilotkit_emit_message(config, "Your cart contains your selected items. Would you like to see the menu again?")

    return state

# Create and compile the workflow
workflow = StateGraph(HotelCustomerServiceState)
workflow.add_node("process", process_message)
workflow.set_entry_point("process")
workflow.add_edge("process", END)
graph = workflow.compile()

graph.get_graph().draw_mermaid_png(output_file_path="graphs/hotel_customer_service/hotel_customer_service_graph.png")