from langchain_core.messages import HumanMessage
from logic.intent_engine import decide_intent
from debug import trace_node

def intent_decider(state, session_user) -> str:
    trace_node(state, "intent_decider")

    last = state["messages"][-1]

    # Never re-run intent on AI messages
    if not isinstance(last, HumanMessage):
        return session_user.mode or "chat"

    # 🔒 LOCK MODE IF ALREADY IN LEAD
    if session_user.mode == "lead":
        # print("INTENT → locked (lead)")
        return "lead"

    # Otherwise, decide normally
    intent = decide_intent(last.content, session_user)
    session_user.mode = intent

    print("INTENT →", intent)
    return intent
