import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import llm

ALLOWED_INTENTS = {"chat", "info", "pricing", "lead"}

def classify_intent(text: str) -> str:
    system = SystemMessage(content="""
You are an intent classifier for a SaaS chatbot.

Return STRICT JSON:
{
  "intent": "chat | info | pricing | lead"
  "Confidence": 0.0-1.0
}

Definitions:
- chat = greetings, small talk, identity
- info = product understanding, features, what it does,what it is
- pricing = cost, plans, subscriptions, upgrades
- lead = buying intent, trial, signup, contact sales
""")

    response = llm.invoke([
        system,
        HumanMessage(content=text)
    ])

    try:
        data = json.loads(response.content)
    except Exception:
        return {"intent": "chat", "confidence": 0.0}

    intent = data.get("intent", "chat")
    confidence = float(data.get("confidence", 0.0))

    if intent not in ALLOWED_INTENTS:
        return {"intent": "chat", "confidence": 0.0}

    print("LLM INTENT:", intent, "CONF:", confidence)
    return {
        "intent": intent,
        "confidence": confidence
    }

