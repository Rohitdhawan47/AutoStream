from langchain_core.messages import HumanMessage
from logic.extractors import extract_name, is_email, extract_platform, extract_plan
from session import SessionUser
from state import Agentstate
from logic.llm_fallback import llm_extract_fields
from debug import trace_node

def rule_processor_node(state: Agentstate, session_user: SessionUser) -> Agentstate:
    trace_node(state, "rule_processor")
    last_message = state["messages"][-1]

    if not isinstance(last_message, HumanMessage):
        return state
    
    text = last_message.content
    # extracted_something = False
    
    # NAME EXTRACTION
    if session_user.first_name is None:
        name_parts = extract_name(text)
        if name_parts:
            session_user.first_name = name_parts[0].capitalize()
            if len(name_parts) > 1:
                session_user.last_name = name_parts[1].capitalize()

            print("SESSION USER UPDATED:", session_user.to_dict())

    #EMAIL EXTRACTION
    if session_user.email is None:
        email = is_email(text)
        if email:
            session_user.email = email
            print("SESSION USER UPDATED:", session_user.to_dict( ))
    
    #PLATFORM EXTRACTION
    if session_user.platform is None:
        platform = extract_platform(text)
        if platform:
            session_user.platform = platform
            print("Session user updated:", session_user.to_dict())
    
    # PLAN EXTRACTION
    if session_user.plan is None:
        plan = extract_plan(text)
        if plan:
            session_user.plan = plan
            print("SESSION USER UPDATED:", session_user.to_dict())
    
    # ---------- LLM FALLBACK (DISABLED FOR FREE TIER) ----------
    
    # # LLM FALLBACK EXTRACTION (only if something is missing)
    # if session_user.mode == "lead" and not extracted_something:
        
    #     llm_data = llm_extract_fields(text)

    #     if session_user.first_name is None and llm_data.get("first_name"):
    #         session_user.first_name = llm_data["first_name"]

    #     if session_user.last_name is None and llm_data.get("last_name"):
    #         session_user.last_name = llm_data["last_name"]

    #     if session_user.email is None and llm_data.get("email"):
    #         session_user.email = llm_data["email"]

    #     if session_user.platform is None and llm_data.get("platform"):
    #         session_user.platform = llm_data["platform"]
    
    #     if session_user.plan is None and llm_data.get("plan"):
    #          session_user.plan  = llm_data["plan"]

    #     if llm_data:
    #         print("LLM FALLBACK USED:", llm_data)
    #         print("SESSION USER UPDATED:", session_user.to_dict())

    return state
   