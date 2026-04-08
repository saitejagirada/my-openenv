from pydantic import BaseModel, ConfigDict, Field
from typing import List, Literal, Optional
import openenv.core.env_server.types as openenv_types

class Observation(openenv_types.Observation):
    ticket_id: str = Field(default="", description="Unique ID of the ticket")
    customer_message: str = Field(default="", description="The current message from the customer")
    history: List[str] = Field(default_factory=list, description="Conversation history")
    missing_info: List[str] = Field(default_factory=list, description="Fields required before routing")
    status: str = Field(default="OPEN", description="Ticket status")
    refund_processed: bool = Field(default=False, description="True if a refund was already executed")

class Action(openenv_types.Action):
    action_type: Literal["ROUTE", "ASK_INFO", "REFUND", "CLOSE"] = Field(..., description="Type of action to take")
    argument: str = Field(..., description="The category to route to, the question to ask, or the order ID to refund")

class State(openenv_types.State):
    ticket_id: str = Field(default="", description="Unique ID of the ticket")
    customer_message: str = Field(default="", description="The current message from the customer")
    history: List[str] = Field(default_factory=list, description="Conversation history")
    missing_info: List[str] = Field(default_factory=list, description="Fields required before routing")
    status: str = Field(default="OPEN", description="Ticket status")
    refund_processed: bool = Field(default=False, description="True if a refund was already executed")

class Reward(BaseModel):
    value: float = Field(..., description="Numerical reward between -1.0 and 1.0")
    feedback: str = Field(..., description="Incremental feedback for the agent")