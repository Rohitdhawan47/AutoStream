from langchain_core.messages import AIMessage
from state import AgentState
from debug import trace_node

def greetingnode(state: AgentState) -> AgentState:
    trace_node(state, "greeting")
    state["messages"].append(
        AIMessage(content="Hello! I'm AutoStream’s assistant. How can I help you today?")
    )
    return state
