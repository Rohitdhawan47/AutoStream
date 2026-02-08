def detect_intent(text: str):
    text = text.lower()

    pricing = [
        "price", "pricing", "plans", "subscription", "cost", "upgrade",
        "subscribe",
        "cost",
        "features"
    ]

    lead = [
        "buy", "trial", "sign up", "signup", "contact sales", "purchase", "interested", "go with"
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