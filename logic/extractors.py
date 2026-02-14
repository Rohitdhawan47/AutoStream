import re

STOPWORDS = {
    "and", "or", "but", "so", "then",
    "want", "need", "looking", "pricing",
    "plan", "plans", "subscription", "about"
}

# ---------- NAME ----------

def extract_name(text: str):
    t = text.strip()

    # Full sentence patterns
    patterns = [
        r"(?:my name is|i am|i'm|this is)\s+([A-Za-z]+)(?:\s+([A-Za-z]+))?",
    ]

    for p in patterns:
        m = re.search(p, t, re.IGNORECASE)
        if m:
            return [m.group(1), m.group(2)] if m.group(2) else [m.group(1)]

    # Bare name fallback (single word, alphabetic, reasonable length)
    if re.fullmatch(r"[A-Za-z]{2,20}", t):
        return [t]

    return None

# ---------- EMAIL ----------
def is_email(text: str) -> str | None:
    match = re.search(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        text
    )
    return match.group(0) if match else None


# ---------- PLATFORM ----------
def extract_platform(text: str) -> str | None:
    t = text.lower()

    patterns = {
        "Youtube": r"\b(youtube|yt channel|yt)\b",
        "Instagram": r"\b(instagram|insta|reels?)\b",
        "Shorts": r"\b(youtube shorts|shorts)\b"
    }

    for platform, pattern in patterns.items():
        if re.search(pattern, t):
            return platform

    return None


# ---------- PLAN ----------
def extract_plan(text: str):
    t = text.lower()

    if "pro" in t:
        return "Pro"
    if "basic" in t or "free" in t:
        return "Basic"
    if "enterprise" in t or "business" in t or "team" in t:
        return "Enterprise"

    return None
