from langchain_core.messages import HumanMessage
from logic.extractors import extract_name, is_email, extract_platform, extract_plan
from state import Agentstate
from logic.llm_fallback import llm_extract_fields
from debug import trace_node

MIN_LLM_FALLBACK_CHARS = 25  # guard against hallucination

def rule_processor_node(state: Agentstate) -> Agentstate:
    session_user = state["session_user"]
    trace_node(state, "rule_processor")

    last_message = state["messages"][-1]
    if not isinstance(last_message, HumanMessage):
        return state

    text = last_message.content.strip()
    extracted_something = False

    awaiting = getattr(session_user, "awaiting", None)

    # --------------------------------------------------
    # NAME — ONLY when explicitly asked
    # Expected format: "my name is Rohit Dhawan"
    # --------------------------------------------------
    if (
        session_user.first_name is None
        and awaiting == "name"
    ):
        name_parts = extract_name(text)
        if name_parts:
            session_user.first_name = name_parts[0].capitalize()
            if len(name_parts) > 1:
                session_user.last_name = name_parts[1].capitalize()
            extracted_something = True
            session_user.awaiting = None
            print("SESSION USER UPDATED:", session_user.to_dict())
    

    # --------------------------------------------------
    # EMAIL — safe to extract anytime
    # --------------------------------------------------
    if session_user.email is None:
        email = is_email(text)
        if email:
            session_user.email = email
            extracted_something = True
            session_user.awaiting = None
            print("SESSION USER UPDATED:", session_user.to_dict())

    # --------------------------------------------------
    # PLATFORM — ONLY when asked
    # --------------------------------------------------
    if (
        session_user.platform is None
        and awaiting == "platform"
    ):
        platform = extract_platform(text)
        if platform:
            session_user.platform = platform
            extracted_something = True
            session_user.awaiting = None
            print("SESSION USER UPDATED:", session_user.to_dict())

    # --------------------------------------------------
    # PLAN — ONLY when asked
    # --------------------------------------------------
    if (
        session_user.plan is None
        and awaiting == "plan"
    ):
        plan = extract_plan(text)
        if plan:
            session_user.plan = plan
            extracted_something = True
            session_user.awaiting = None
            print("SESSION USER UPDATED:", session_user.to_dict())

    # --------------------------------------------------
    # LLM FALLBACK — VERY RESTRICTED
    # Only during lead mode AND after a question was asked
    # --------------------------------------------------
    should_fallback = (
        session_user.mode == "lead"
        and not extracted_something
        and awaiting is not None
        and not session_user.is_complete()
        and len(text) >= MIN_LLM_FALLBACK_CHARS
    )

    if should_fallback:
        llm_data = llm_extract_fields(text)

        if awaiting == "name" and session_user.first_name is None:
            if llm_data.get("first_name"):
                session_user.first_name = llm_data["first_name"]
                session_user.last_name = llm_data.get("last_name")
                extracted_something = True

        elif awaiting == "email" and session_user.email is None:
            if llm_data.get("email"):
                session_user.email = llm_data["email"]
                extracted_something = True

        elif awaiting == "platform" and session_user.platform is None:
            if llm_data.get("platform"):
                session_user.platform = llm_data["platform"]
                extracted_something = True

        elif awaiting == "plan" and session_user.plan is None:
            if llm_data.get("plan"):
                session_user.plan = llm_data["plan"]
                extracted_something = True

        if extracted_something:
            session_user.awaiting = None
            print("LLM FALLBACK USED:", llm_data)
            print("SESSION USER UPDATED:", session_user.to_dict())

    return state
