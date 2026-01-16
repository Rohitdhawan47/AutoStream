from state import Agentstate
from langchain_core.messages import HumanMessage
from debug import trace_node

def user_input_node(state: Agentstate)-> Agentstate:
    trace_node(state, "user_input")
    user_message = input("User: ")
    state["messages"].append(HumanMessage(content = user_message))
    return state