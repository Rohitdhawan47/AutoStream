from logic.rules import detect_intent
from logic.llm_intent import classify_intent

def decide_intent(text, session_user):
    # HARD LOCK: Stay in lead mode until complete
    if session_user.mode == "lead" and not session_user.is_complete():
        return "lead"

    # Try rules first
    rule_label, rule_conf = detect_intent(text)

    if rule_conf >= 0.6:
        return rule_label
    # print(f"the rules passed this {rule_label, rule_conf}") for debug

    # LLM fallback
    llm_result = classify_intent(text)

    if llm_result["confidence"] >= 0.6:
        # print(f"LLM ANswer: {llm_result}") for debug
        return llm_result["intent"]

    return "chat"





