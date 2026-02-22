from langchain_core.messages import HumanMessage
from logic.llm_intent import classify_intent
from debug import trace_node

def intent_node(state):
    trace_node(state, "intent_decision")

    last = state["messages"][-1]
    if not isinstance(last, HumanMessage):
        return state

    signals = classify_intent(last.content)
    session_user = state["session_user"]
    # print(f"this was passed from llm_intent: {signals}")

    # ✅ Persist signals where the system actually reads them
    session_user.wants_info = signals["wants_info"]
    session_user.wants_pricing = signals["wants_pricing"]

    return state




