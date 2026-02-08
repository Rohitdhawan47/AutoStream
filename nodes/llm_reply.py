from langchain_core.messages import AIMessage, SystemMessage
from state import Agentstate
from logic.lead_qualifier import mock_lead_capture
from debug import trace_node
from llm import llm
from knowledge_base.product import PRODUCT_SEED


def llm_reply_node(state: Agentstate) -> Agentstate:
    session_user = state["session_user"]
    trace_node(state, "llm_reply")

    # --------------------------------
    # 1️⃣ LEAD MODE — HARD PRIORITY
    # --------------------------------
    if session_user.mode == "lead":

        # ✅ Close deal ONCE
        if session_user.is_complete() and not session_user.lead_submitted:
            mock_lead_capture(
                name=f"{session_user.first_name or ''} {session_user.last_name or ''}".strip(),
                email=session_user.email,
                platform=session_user.platform,
                plan=session_user.plan
            )
            session_user.lead_submitted = True
            session_user.awaiting = None

            state["messages"].append(
                AIMessage(content="Thanks! Your details are saved. Our team will reach out shortly.")
            )
            return state

        # ✅ Ask in BUSINESS-OPTIMAL order (and DECLARE intent)
        if not session_user.email:
            session_user.awaiting = "email"
            question = "What’s the best email to send your AutoStream plan details to?"

        elif not session_user.platform:
            session_user.awaiting = "platform"
            question = "Which platform do you create content for? (YouTube, Instagram, or Shorts)"

        elif not session_user.plan:
            session_user.awaiting = "plan"
            question = "Which plan are you interested in? (Basic, Pro, or Enterprise)"

        elif not session_user.first_name:
            session_user.awaiting = "name"
            question = (
                "By the way, what should I call you?\n"
                "Please reply like: *My name is [First Name] [Last Name]*"
            )

        else:
            session_user.awaiting = None
            question = "Almost done — is there anything else you'd like to know?"

        state["messages"].append(AIMessage(content=question))
        return state

    # --------------------------------
    # 2️⃣ INFO MODE — PRODUCT ONLY
    # --------------------------------
    if session_user.mode == "info":
        session_user.awaiting = None

        system_message = SystemMessage(
            content=(
                "You are AutoStream's assistant.\n\n"
                f"{PRODUCT_SEED}\n\n"
                "Rules:\n"
                "- Answer ONLY using the product info above\n"
                "- Do NOT invent features, pricing, URLs, or policies\n"
                "- Keep answers under 2 sentences\n"
                "- If missing, say you don’t know\n"
            )
        )

        messages = [system_message] + state["messages"][-3:]
        response = llm.invoke(messages)

        if response.content.strip():
            state["messages"].append(AIMessage(content=response.content))

        return state

    # --------------------------------
    # 3️⃣ CHAT MODE — FREE LLM
    # --------------------------------
    session_user.awaiting = None

    system_message = SystemMessage(
        content=(
            "You are a friendly SaaS assistant for AutoStream.\n"
            "Keep responses short, helpful, and conversational.\n"
        )
    )

    messages = [system_message] + state["messages"][-5:]
    response = llm.invoke(messages)

    if response.content.strip():
        state["messages"].append(AIMessage(content=response.content))

    return state
