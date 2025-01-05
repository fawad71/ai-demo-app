"""
This is the state definition for the AI.
It defines the state of the agent and the state of the conversation.
"""

from typing import List, Dict, Optional
from langgraph.graph import MessagesState
from pydantic import BaseModel

class CartItem(BaseModel):
    """Cart item model"""
    item_id: int
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    """Order model"""
    order_id: str
    items: List[CartItem]
    total: float
    status: str  # pending, confirmed, cancelled
    user_name: str

class HotelCustomerServiceState(MessagesState):
    """Hotel Customer Service State"""
    name: Optional[str] = None
    cart: List[CartItem] = []
    current_order: Optional[Order] = None
    last_shown_menu: bool = False
    awaiting_human_approval: bool = False
    human_response: Optional[str] = None