from langchain_core.messages import AIMessage
from state import Agentstate
from debug import trace_node

def greetingnode(state: Agentstate) -> Agentstate:
    trace_node(state, "greeting")
    state["messages"].append(
        AIMessage(content="Hello! I'm AutoStream’s assistant. How can I help you today?")
    )
    return state
