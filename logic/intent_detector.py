# from langchain_core.messages import HumanMessage
# from logic.rules import detect_intent
# from logic.llm_intent import llm_classify_intent
# from logic.intent_engine import decide_intent
# from debug import trace_node

# def intent_decider(state, session_user) -> str:
#     trace_node(state, "intent_decider")

#     last_message = state["messages"][-1]

#     if not isinstance(last_message, HumanMessage):
#         return "chat"

#     text = last_message.content.lower()
    

#     # Step 1 — Try rules first
#     intent = detect_intent(text)
#     print("INTENT (rules) →", intent)

#     # Step 2 — LLM fallback ONLY for chat/unknown
#     llm_intent = llm_classify_intent(text)
#     print("INTENT (llm) →", llm_intent)

#     if llm_intent in ["lead", "info"]:
#         session_user.mode = llm_intent
#         return llm_intent

#     session_user.mode = "chat"
#     return "chat"

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
        print("INTENT → locked (lead)")
        return "lead"

    # Otherwise, decide normally
    intent = decide_intent(last.content, session_user)
    session_user.mode = intent

    print("INTENT →", intent)
    return intent
