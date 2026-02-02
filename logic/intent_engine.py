from logic.rules import detect_intent
from logic.llm_intent import classify_intent

# def decide_intent(text, session_user):
#     # HARD LOCK: Stay in lead mode until complete
#     if session_user.mode == "lead" and not session_user.is_complete():
#         return "lead"

#     # Try rules first
#     rule_label, rule_conf = detect_intent(text)

#     if rule_conf >= 0.9:
#         return rule_label

#     # LLM fallback
#     llm_result = classify_intent(text)

#     if llm_result["confidence"] >= 0.6:
#         return llm_result["intent"]

#     return "chat"


from logic.rules import detect_intent
from logic.llm_intent import classify_intent

def decide_intent(text, session_user):

    # # Try rules
    # rule_intent, rule_conf = detect_intent(text)
    # if rule_conf >= 0.9:
    #     print("RULE INTENT:", rule_intent)
    #     return rule_intent 

    # Ask LLM
    result = classify_intent(text)
        # SAFETY: extract string only
    print(f"i passed this{result}")
    if isinstance(result, dict):
        return result.get("intent", "chat")

    # If someone changes classify_intent later
    if isinstance(result, str):
        return result

    return "chat"




