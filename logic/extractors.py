import re
def extract_name(text: str):
    text = text.strip()

    if "my name is" in text.lower():
        name_part = text.lower().split("my name is")[-1].strip()
        parts = name_part.split()
        return parts
    
    parts = text.split()
    if len(parts) == 2:
        return parts
    
    return None

def is_email(text: str) -> str | None:
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    if match:
        return match.group(0)
    return None

def extract_platform(text: str)-> str | None:
    t = text.lower()
    
    if "youtube" in t or "yt" in t:
        return "Youtube"
    
    if "instagram" in t or "insta" in t or "reel" in t:
        return "Instagram"
    
    if "short" in t:
        return "Shorts"
    
    return None
def extract_plan(text: str):
    text = text.lower()

    plan_keywords = {
        "pro": ["pro plan", "professional", "pro"],
        "basic": ["basic plan", "starter", "free"],
        "enterprise": ["enterprise", "business", "team"]
    }

    for plan, keywords in plan_keywords.items():
        for k in keywords:
            if k in text:
                return plan.capitalize()

    return None