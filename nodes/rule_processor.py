from langchain_core.messages import HumanMessage
from logic.extractors import extract_name, is_email, extract_platform, extract_plan
from state import AgentState
from logic.llm_fallback import llm_extract_fields
from debug import trace_node

MIN_LLM_FALLBACK_CHARS = 20


def rule_processor_node(state: AgentState) -> AgentState:
    session_user = state["session_user"]
    trace_node(state, "rule_processor")
    # print("[RULE_PROCESSOR] slot flag BEFORE:", state.get("slot_filled_this_turn"))


    last_message = state["messages"][-1]
    if not isinstance(last_message, HumanMessage):
        return state

    text = last_message.content.strip()

    # --------------------------------------------------
    # 1️⃣ STRICT extraction when awaiting a slot
    # --------------------------------------------------
    awaiting = getattr(session_user, "awaiting_slot", None)

    if awaiting == "name":
        name_parts = extract_name(text)
        if name_parts:
            print("[RULE_PROCESSOR] extracted platform:", name_parts)
            session_user.first_name = name_parts[0].capitalize()
            session_user.last_name = (
                name_parts[1].capitalize() if len(name_parts) > 1 else None
            )
            state["slot_filled_this_turn"] = True
            print("[RULE_PROCESSOR] slot flag SET TO TRUE")
            session_user.awaiting_slot = None
            return state

    if awaiting == "email":
        email = is_email(text)
        if email:
            print("[RULE_PROCESSOR] extracted platform:", email)
            session_user.email = email
            state["slot_filled_this_turn"] = True
            print("[RULE_PROCESSOR] slot flag SET TO TRUE")
            session_user.awaiting_slot = None
            return state

    if awaiting == "platform":
        platform = extract_platform(text)
        if platform:
            print("[RULE_PROCESSOR] extracted platform:", platform)
            session_user.platform = platform
            state["slot_filled_this_turn"] = True
            print("[RULE_PROCESSOR] slot flag SET TO TRUE")
            session_user.awaiting_slot = None
            return state

    if awaiting == "plan":
        plan = extract_plan(text)
        if plan:
            print("[RULE_PROCESSOR] extracted platform:", plan)
            session_user.plan = plan
            state["slot_filled_this_turn"] = True
            print("[RULE_PROCESSOR] slot flag SET TO TRUE")
            session_user.awaiting_slot = None
            return state

    # --------------------------------------------------
    # 2️⃣ SAFE background extraction (only non-ambiguous)
    # --------------------------------------------------
    if session_user.email is None:
        email = is_email(text)
        if email:
            session_user.email = email
            state["slot_filled_this_turn"] = True
            return state

    # --------------------------------------------------
    # 3️⃣ LLM fallback (only when NOT answering a question)
    # --------------------------------------------------
    missing_fields = [
        session_user.first_name is None,
        session_user.email is None,
        session_user.platform is None,
        session_user.plan is None,
    ]

    if (
        session_user.awaiting_slot is None
        and len(text) >= MIN_LLM_FALLBACK_CHARS
        and sum(missing_fields) >= 2
    ):
        llm_data = llm_extract_fields(text)

        if session_user.first_name is None and llm_data.get("first_name"):
            session_user.first_name = llm_data["first_name"]
            state["slot_filled_this_turn"] = True
            print("extracted first name using llm fallback")

        if session_user.last_name is None and llm_data.get("last_name"):
            session_user.last_name = llm_data["last_name"]
            state["slot_filled_this_turn"] = True
            print("extracted last name using llm fallback")

        if session_user.email is None and llm_data.get("email"):
            session_user.email = llm_data["email"]
            state["slot_filled_this_turn"] = True
            print("extracted email using llm fallback")

        if session_user.platform is None and llm_data.get("platform"):
            session_user.platform = llm_data["platform"]
            state["slot_filled_this_turn"] = True
            print("extracted platform using llm fallback")

        if session_user.plan is None and llm_data.get("plan"):
            session_user.plan = llm_data["plan"]
            state["slot_filled_this_turn"] = True
            print("extracted plan using llm fallback")

    #     if llm_data:
    #         print("LLM FALLBACK USED:", llm_data)
    # print("[RULE_PROCESSOR] slot flag AFTER:", state.get("slot_filled_this_turn"))


    return state
