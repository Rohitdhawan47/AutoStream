from state import Agentstate
from logic.rules import detect_intent
from langchain_core.messages import HumanMessage

def intent_decider(state: Agentstate, session_user) -> str:
    last_message = state["messages"][-1]

    

    if isinstance(last_message, HumanMessage):
        intent = detect_intent(last_message.content)
        print("INTENT ROUTER →", intent)

        if intent == "high_intent":
            session_user.mode = "lead"
            return "lead"

    return "normal"
