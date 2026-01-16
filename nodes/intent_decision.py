from state import Agentstate
from debug import trace_node
def intent_decision_node(state: Agentstate) -> Agentstate:
    trace_node(state, "intent_decision")
    return state
