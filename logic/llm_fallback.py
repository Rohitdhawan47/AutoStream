from langchain_core.messages import SystemMessage, HumanMessage
from llm import llm
import json

def llm_extract_fields(text:str)-> dict:
    """
    Uses LLM to extract structured fields.
    returns a dict with possible keys:
    first_name, last_name, email, platform, plan
    """

    system = SystemMessage(
        content=(
        
            "You are an information extraction assistant.\n"
            "Extract ONLY the following fields if explicitly present:\n"
            "- first_name\n"
            "- last_name\n"
            "- email\n"
            "- platform (YouTube, Instagram, Shorts)\n"
            "- plan (Basic, Pro, Enterprise)\n\n"
            "Return STRICT JSON only.\n"
            "If a field is not present, use null.\n\n"
            "Example:\n"
            "{\n"
            '  "first_name": "Rohit",\n'
            '  "last_name": null,\n'
            '  "email": null,\n'
            '  "platform": "YouTube,"\n'
            '  "plan": "pro"'
            "}"


        )
    )

    human = HumanMessage(content=text)

    response = llm.invoke([system, human])

    try:
        raw = json.loads(response.content)

        return {
            "first_name": clean_field(raw.get("first_name")),
            "last_name": clean_field(raw.get("last_name")),
            "email": clean_field(raw.get("email")),
            "platform": clean_field(raw.get("platform"), VALID_PLATFORMS),
            "plan": clean_field(raw.get("plan"), VALID_PLANS),
        }
    except Exception:
        return {}

    
VALID_PLANS = {"basic", "pro", "enterprise"}
VALID_PLATFORMS = {"youtube", "instagram", "shorts"}

def clean_field(value, valid_set=None):
    if not value:
        return None

    v = str(value).strip().lower()

    # Reject vague or hallucinated phrases
    if any(bad in v for bad in ["not provided", "unknown", "n/a", "none", "null", "pricing"]):
        return None

    if valid_set and v not in valid_set:
        return None

    return v.capitalize() if not valid_set else v.capitalize()