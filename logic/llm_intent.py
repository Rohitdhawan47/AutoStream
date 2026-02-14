import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import llm
from logic.rules import contains_user_identity, contains_question

def classify_intent(text: str) -> dict:
    # 1️⃣ HARD GUARD — user identity is NOT product intent
    if contains_user_identity(text) and not contains_question(text):
        return {
            "wants_info": False,
            "wants_pricing": False,
            "confidence": 1.0
        }
    
    """
    Detects informational signals only.
    DOES NOT detect buying intent.
    """

    system = SystemMessage(
        content="""
You are a signal classifier for a SaaS chatbot.

Return STRICT JSON ONLY:
{
  "wants_info": true | false,
  "wants_pricing": true | false,
  "confidence": 0.0 to 1.0
}

Definitions:
- wants_info = user is trying to understand what the product is or does
- wants_pricing = user is asking about price of the plans, subscriptions, or cost, plan structure

Rules:
- Do NOT detect buying or commitment
- Output JSON ONLY, no text
- Consider personal information as false
"""
    )

    response = llm.invoke([
        system,
        HumanMessage(content=text)
    ])

    # -------- SAFE PARSE --------
    try:
        data = json.loads(response.content)
    except Exception:
        return _empty()

    # -------- NORMALIZATION --------
    wants_info = bool(data.get("wants_info", False))
    wants_pricing = bool(data.get("wants_pricing", False))

    try:
        confidence = float(data.get("confidence", 0.0))
    except Exception:
        confidence = 0.0

    # Clamp confidence
    if confidence < 0.0:
        confidence = 0.0
    elif confidence > 1.0:
        confidence = 1.0

    return {
        "wants_info": wants_info,
        "wants_pricing": wants_pricing,
        "confidence": confidence
    }


def _empty():
    return {
        "wants_info": False,
        "wants_pricing": False,
        "confidence": 0.0
    }

    
