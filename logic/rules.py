def detect_intent(text: str):
    text = text.lower()

    pricing = [
        "price", "pricing", "plans", "subscription", "cost", "upgrade"
    ]

    lead = [
        "buy", "trial", "sign up", "signup", "contact sales", "purchase", "interested"
    ]

    info = [
        "what is", "what does", "features", "explain", "tell me about"
    ]

    if any(k in text for k in pricing):
        return ("pricing", 0.95)

    if any(k in text for k in lead):
        return ("lead", 0.95)

    if any(k in text for k in info):
        return ("info", 0.80)

    return ("chat", 0.0)


def is_pricing_question(text: str) -> bool:
    text = text.lower()

    keywords = [
        "pricing",
        "price",
        "plans",
        "subscription",
        "subscribe",
        "pro plan",
        "cost",
        "features"
    ]

    return any(k in text for k in keywords)

import re

BUY_PATTERN = re.compile(
    r"\b(i\s*(will|want|choose|go)\s*with\s*(basic|pro|enterprise)\s*plan)\b",
    re.IGNORECASE
)

def wants_to_buy(text: str) -> bool:
    return bool(BUY_PATTERN.search(text))

