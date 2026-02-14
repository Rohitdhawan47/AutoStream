import regex as re
BUY_PATTERN = re.compile(
    r"\b(i\s*(will|want|choose)?\s*(go\s*)?with\s*(the\s*)?(basic|pro|enterprise)\s*plan)\b",
    re.IGNORECASE
)

def wants_to_buy(text: str) -> bool:
    return bool(BUY_PATTERN.search(text))

QUESTION_START = (
    "what", "why", "how", "when", "where",
    "which", "can you", "could", "do", "does",
    "is", "are", "should", "would"
)

def contains_question(text: str) -> bool:
    t = text.strip().lower()

    if "?" in t:
        return True

    return any(t.startswith(q + " ") for q in QUESTION_START)

def contains_user_identity(text: str) -> bool:
    t = text.lower()
    return any([
        "my name is" in t,
        "i am " in t,
        "email is" in t,
        "@" in t,
        "you can call me" in t
    ])
