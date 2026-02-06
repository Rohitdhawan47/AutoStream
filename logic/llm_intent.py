# import json
# from langchain_core.messages import SystemMessage, HumanMessage
# from llm import llm

# ALLOWED_INTENTS = {"chat", "info", "pricing", "lead"}

# def classify_intent(text: str) -> str:
#     system = SystemMessage(content="""
# You are an intent classifier for a SaaS chatbot.

# Return STRICT JSON:
# {
#   "intent": "chat | info | pricing | lead"
#   "Confidence": 0.0-1.0
# }

# Definitions:
# - chat = greetings, small talk, identity
# - info = product understanding, features, what it does,what it is
# - pricing = cost, plans, subscriptions, upgrades
# - lead = buying intent, trial, signup, contact sales
# """)

#     response = llm.invoke([
#         system,
#         HumanMessage(content=text)
#     ])

#     try:
#         data = json.loads(response.content)
#     except Exception:
#         return {"intent": "chat", "confidence": 0.0}

#     intent = data.get("intent", "chat")
#     confidence = float(data.get("confidence", 0.0))

#     if intent not in ALLOWED_INTENTS:
#         return {"intent": "chat", "confidence": 0.0}

#     print("LLM INTENT:", intent, "CONF:", confidence)
#     return {
#         "intent": intent,
#         "confidence": confidence
#     }

import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import llm


def classify_intent(text: str) -> dict:
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
- wants_pricing = user is asking about price, plans, subscriptions, or cost

Rules:
- Do NOT detect buying or commitment
- Greetings, identity, or small talk = both false
- Output JSON ONLY, no text
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

    
