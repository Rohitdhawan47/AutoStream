from typing import TypedDict, List
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langgraph.channels import LastValue
from langchain_core.messages import BaseMessage
from session import SessionUser

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    trace: Annotated[List[str], LastValue]
    session_user: SessionUser
    slot_filled_this_turn : bool
