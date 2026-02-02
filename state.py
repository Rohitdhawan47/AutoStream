from typing import TypedDict, List, Optional
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langgraph.channels import LastValue
from langchain_core.messages import BaseMessage
from session import SessionUser

class User(TypedDict):
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]

class Agentstate(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]
    trace: Annotated[List[str], LastValue]
    session_user: SessionUser
