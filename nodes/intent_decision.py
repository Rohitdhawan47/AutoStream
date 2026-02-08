from langchain_core.messages import HumanMessage
from logic.intent_engine import decide_intent
from debug import trace_node
def intent_node(state):
    trace_node(state, "intent_node")

    session_user = state["session_user"]
    last = state["messages"][-1]

    if not isinstance(last, HumanMessage):
        return state

    intent = decide_intent(last.content, session_user)
    print(f"type: {type(intent)}")

    print("INTENT →", intent)
    print("MODE BEFORE:", session_user.mode)

    # Lead mode persists, but intent still routes
    if session_user.mode == "lead":
        if intent in ["pricing", "info"]:
            state["route"] = intent
            return state

        # Stay in lead flow
        state["route"] = "lead"
        return state

    # Normal mode switching
    session_user.mode = intent
    state["route"] = intent

    print("MODE AFTER:", session_user.mode)
    return state


