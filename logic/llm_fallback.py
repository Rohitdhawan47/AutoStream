from langchain_core.messages import SystemMessage, HumanMessage
from llm import llm
import json

def llm_extract_fields(text:str)-> dict:
    """
    Uses LLM to extract structured fields.
    returns a dict with possible keys:
    first_name, last_name, email, platform
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
        return json.loads(response.content)
    except Exception:
        return {}