import re
def extract_name(text:str):
    text = text.lower()

    if "my name is" in text:
        return text.split("my name is")[-1].strip().split()[0]
    
    if text.startswith("i am"):
        return text.split("i am")[-1].strip().split()[0]
    
    return None

def detect_intent(text:str):
    text = text.lower()

    high_intent_keywords = [
        "i want to try",
        "sign me up",
        "get started",
        "subscribe",
        "pro plan",
        "buy",
        "trial"
    ]

    for keyword in high_intent_keywords:
        if keyword in text:
            return "high_intent"
        
    return "info"
def is_product_question(text: str) -> bool:
    text = text.lower()

    keywords = [
        "pricing",
        "price",
        "plans",
        "subscription",
        "subscribe"
        "pro plan",
        "cost",
        "features"
    ]

    return any(k in text for k in keywords)
