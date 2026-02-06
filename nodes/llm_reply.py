# from langchain_core.messages import AIMessage, SystemMessage
# from state import Agentstate
# from logic.lead_qualifier import mock_lead_capture
# from debug import trace_node
# from llm import llm
# from knowledge_base.product import PRODUCT_SEED


# def llm_reply_node(state: Agentstate) -> Agentstate:
#     session_user = state["session_user"]
#     trace_node(state, "llm_reply")


#     # 1️⃣ Lead COMPLETE → Capture once and confirm
#     if (
#         session_user.mode == "lead"
#         and session_user.is_complete()
#         and not session_user.lead_submitted
#     ):
#         mock_lead_capture(
#             name=f"{session_user.first_name} {session_user.last_name or ''}".strip(),
#             email=session_user.email,
#             platform=session_user.platform,
#             plan=session_user.plan
#         )
#         session_user.lead_submitted = True

#         state["messages"].append(
#             AIMessage(content="Thanks! Your details are saved. Our team will reach out shortly.")
#         )
#         return state

#     # 2️⃣ Lead INCOMPLETE → Ask for missing fields
#     context = None

#     if session_user.mode == "lead":
#         if not session_user.email:
#             context = (
#                 f"The user's name is {session_user.first_name or 'there'}.\n"
#                 "Ask them for their email."
#             )
#         elif not session_user.platform:
#             context = (
#                 "The user's email is already collected.\n"
#                 "Ask which platform they create content for "
#                 "(YouTube, Instagram, or Shorts)."
#             )
#         elif not session_user.plan:
#             context = (
#                 "Ask which plan they are interested in "
#                 "(Basic, Pro, or Enterprise)."
#             )

#     # 3️⃣ INFO MODE → Product seed grounded answer
#     if session_user.mode == "info":
#         system_message = SystemMessage(
#             content=(
#                 "You are AutoStream's assistant.\n"
#                 f"{PRODUCT_SEED}\n\n"
#                 "- Answer only from the product information above.\n"
#                 "- Do NOT invent features, pricing, or policies.\n"
#                 "- Keep the answer under 2 sentences.\n"
#             )
#         )

#         messages = [system_message] + state["messages"][-3:]
#         response = llm.invoke(messages)

#         if response.content.strip():
#             state["messages"].append(AIMessage(content=response.content))
#         return state

#     # 4️⃣ CHAT MODE OR NO CONTEXT → Normal LLM reply
#     if not context:
#         response = llm.invoke(state["messages"])
#         if response.content.strip():
#             state["messages"].append(AIMessage(content=response.content))
#         return state

#     # 5️⃣ Lead question via controlled system prompt
#     system_message = SystemMessage(
#         content=(
#             "You are AutoStream's assistant.\n"
#             f"{PRODUCT_SEED}\n\n"
#             "- Ask only ONE question.\n"
#             "- Do NOT invent features, pricing, URLs, or policies.\n"
#             "- Keep the response under 1 sentence.\n\n"
#             f"{context}"
#         )
#     )

#     messages = [system_message] + state["messages"][-3:]
#     response = llm.invoke(messages)

#     if response.content.strip():
#         state["messages"].append(AIMessage(content=response.content))
#     return state
# from langchain_core.messages import AIMessage, SystemMessage
# from state import AgentState
# from logic.lead_qualifier import mock_lead_capture
# from debug import trace_node
# from llm import llm
# from knowledge_base.product import PRODUCT_SEED


# def llm_reply_node(state: AgentState) -> AgentState:
#     session_user = state["session_user"]
#     trace_node(state, "llm_reply")
#     print("LLM MODE CHECK:", session_user.mode)
#     # -------------------------------
#     # 1️⃣ LEAD MODE (HARD PRIORITY)
#     # -------------------------------
#     if session_user.mode == "lead":
#         # Lead COMPLETE → Capture once
#         if session_user.is_complete() and not session_user.lead_submitted:
#             mock_lead_capture(
#                 name=f"{session_user.first_name} {session_user.last_name or ''}".strip(),
#                 email=session_user.email,
#                 platform=session_user.platform,
#                 plan=session_user.plan
#             )
#             session_user.lead_submitted = True

#             state["messages"].append(
#                 AIMessage(content="Thanks! Your details are saved. Our team will reach out shortly.")
#             )
#             return state

#     # Ask in BUSINESS-OPTIMAL ORDER
#         if not session_user.email:
#             question = "What’s the best email to send your AutoStream plan details to?"
#         elif not session_user.platform:
#             question = "Which platform do you create content for? (YouTube, Instagram, or Shorts)"
#         elif not session_user.plan:
#             question = "Which plan are you interested in? (Basic, Pro, or Enterprise)"
#         elif not session_user.first_name:
#             question = "By the way, what should I call you?"
#         else:
#             question = "Almost done — is there anything else you'd like to know?"

#         state["messages"].append(AIMessage(content=question))
#         return state

#     # -------------------------------
#     # 2️⃣ INFO MODE (PRODUCT ONLY)
#     # -------------------------------
#     if session_user.mode == "info":
#         system_message = SystemMessage(
#             content=(
#                 "You are AutoStream's assistant.\n\n"
#                 f"{PRODUCT_SEED}\n\n"
#                 "Rules:\n"
#                 "- Answer ONLY using the product info above\n"
#                 "- Do NOT invent features, pricing, URLs, or policies\n"
#                 "- Keep answers under 2 sentences\n"
#                 "- If the answer is missing, say you don’t know\n"
#             )
#         )

#         messages = [system_message] + state["messages"][-3:]
#         response = llm.invoke(messages)

#         if response.content.strip():
#             state["messages"].append(AIMessage(content=response.content))

#         return state

#     # -------------------------------
#     # 3️⃣ CHAT MODE (FREE LLM)
#     # -------------------------------
#     system_message = SystemMessage(
#         content=(
#             f"You are a friendly SaaS assistant for AutoStream which is {PRODUCT_SEED}\n"
            
#             "Keep responses short, helpful, and conversational.\n"
#         )
#     )

#     messages = [system_message] + state["messages"][-5:]
#     response = llm.invoke(messages)

#     if response.content.strip():
#         state["messages"].append(AIMessage(content=response.content))

#     return state

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from knowledge_base.product import PRODUCT_SEED
from rag.retriever import retrieve_context
from logic.lead_qualifier import mock_lead_capture
from logic.rules import wants_to_buy
from debug import trace_node
from llm import llm


def llm_reply_node(state):
    trace_node(state, "llm_reply")

    session_user = state["session_user"]
    last = state["messages"][-1]

    if not isinstance(last, HumanMessage):
        return state

    text = last.content.strip()

    # -------------------------------
    # 1️⃣ Detect explicit buy signal
    # -------------------------------
    if wants_to_buy(text):
        session_user.wants_to_buy = True

    # -------------------------------
    # 2️⃣ Answer user question
    # -------------------------------
    wants_info = state.get("wants_info", False)
    wants_pricing = state.get("wants_pricing", False)

    if wants_pricing:
        context = retrieve_context(state["vector_store"], text)

        if context.strip():
            system = SystemMessage(
                content=(
                    "You are AutoStream's assistant.\n"
                    "Answer ONLY from the context below.\n"
                    "1-2 sentences max.\n\n"
                    f"Context:\n{context}"
                )
            )
            answer = llm.invoke([system, HumanMessage(content=text)]).content.strip()
        else:
            answer = "We offer Basic, Pro, and Enterprise plans."

    elif wants_info:
        system = SystemMessage(
            content=(
                "You are AutoStream's assistant.\n"
                f"{PRODUCT_SEED}\n\n"
                "- Answer in 1-2 sentences\n"
                "- Do NOT invent features or pricing\n"
            )
        )
        answer = llm.invoke([system, HumanMessage(content=text)]).content.strip()

    else:
        answer = llm.invoke(state["messages"]).content.strip()

    # -------------------------------
    # 3️⃣ ONE aggressive follow-up
    # -------------------------------
    follow_up = None

    if not session_user.first_name:
        follow_up = "By the way, what should I call you?"
    elif not session_user.platform:
        follow_up = "Which platform do you mainly create for? (YouTube, Instagram, or Shorts)"
    elif not session_user.plan:
        follow_up = "Which plan are you considering? (Basic, Pro, or Enterprise)"
    elif not session_user.email:
        follow_up = "What's the best email to send your AutoStream plan details to?"

    # -------------------------------
    # 4️⃣ Close deal ONLY if allowed
    # -------------------------------
    if session_user.wants_to_buy and session_user.is_complete():
        if not session_user.lead_submitted:
            mock_lead_capture(
                name=f"{session_user.first_name} {session_user.last_name or ''}".strip(),
                email=session_user.email,
                platform=session_user.platform,
                plan=session_user.plan
            )
            session_user.lead_submitted = True

        answer = "You're all set! I've sent your details to our team — they'll reach out shortly."
        return _say(state, answer)

    # Append follow-up if any
    if follow_up:
        answer = f"{answer}\n\n{follow_up}"

    return _say(state, answer)


def _say(state, text):
    state["messages"].append(AIMessage(content=text))
    return state
