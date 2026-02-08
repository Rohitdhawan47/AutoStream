import re

STOPWORDS = {
    "and", "or", "but", "so", "then",
    "want", "need", "looking", "pricing",
    "plan", "plans", "subscription", "about"
}

# ---------- NAME ----------


from typing import Optional, Tuple

def extract_name(text: str) -> Optional[Tuple[str, str]]:
    """
    Extracts FIRST and LAST name ONLY when user explicitly says:
    - my name is FIRST LAST
    - i am FIRST LAST
    - i'm FIRST LAST
    - this is FIRST LAST
    """

    t = text.strip()

    pattern = r"""
        \b(?:my\s+name\s+is|i\s+am|i'm|this\s+is)\b
        \s+
        ([A-Za-z]{2,20})
        \s+
        ([A-Za-z]{2,20})
        \b
    """

    match = re.search(pattern, t, re.IGNORECASE | re.VERBOSE)
    if not match:
        return None

    first_name = match.group(1).capitalize()
    last_name = match.group(2).capitalize()

    return first_name, last_name



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
