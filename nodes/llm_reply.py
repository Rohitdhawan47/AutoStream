from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from knowledge_base.product import PRODUCT_SEED
from rag.retriever import retrieve_context
from logic.lead_qualifier import mock_lead_capture
from logic.rules import wants_to_buy, contains_question
from debug import trace_node
from llm import llm


def llm_reply_node(state, vector_store):
# For Debugging
    trace_node(state, "llm_reply")
#     print(
#     "[LLM_REPLY] sees slot_filled_this_turn =",
#     state.get("slot_filled_this_turn")
# )


    session_user = state["session_user"]
    last = state["messages"][-1]

    if not isinstance(last, HumanMessage):
        print("[LLM_REPLY] Last message is not HumanMessage → returning state")
        return state

    text = last.content.strip()
    
    # For Debugging
    # print("\n[LLM_REPLY] ================= TURN START =================")
    # print("[INPUT TEXT]:", text)
    # print("[SESSION BEFORE]:", session_user.to_dict())

    # --------------------------------------------------
    # 1️⃣ Detect explicit buy signal (STRICT)
    # --------------------------------------------------
    if wants_to_buy(text):
        session_user.wants_to_buy = True
        print("[BUY SIGNAL] Explicit buy detected → wants_to_buy = True")

    slot_filled = state.get("slot_filled_this_turn", False)
    asked_question = (
    contains_question(text)
    or (
        not slot_filled
        and (session_user.wants_info or session_user.wants_pricing)
    )
)

    print("[FLAGS] slot_filled:", slot_filled,
          "| asked_question:", asked_question,
          "| wants_info:", session_user.wants_info,
          "| wants_pricing:", session_user.wants_pricing,
          "| wants_to_buy:", session_user.wants_to_buy)

    # --------------------------------------------------
    # 2️⃣ HARD CLOSE (ONLY when valid)
    # --------------------------------------------------
    if session_user.wants_to_buy and session_user.is_complete():
        # print("[HARD CLOSE] Conditions met")

        if not session_user.lead_submitted:
            # print("[LEAD CAPTURE] Submitting lead")
            mock_lead_capture(
                name=f"{session_user.first_name or ''} {session_user.last_name or ''}".strip(),
                email=session_user.email,
                platform=session_user.platform,
                plan=session_user.plan
            )
            session_user.lead_submitted = True

        return _say(
            state,
            "You're all set! I've sent your details to our team — they'll reach out shortly,\n " 
            "Type exit if you want to end the conversation. "
        )

    if session_user.lead_submitted:
        # print("[LEAD COMPLETE] Already submitted → stopping")
        return state

    # --------------------------------------------------
    # 3️⃣ SLOT-ONLY TURN (NO QUESTION)
    # --------------------------------------------------
    follow_up = _next_missing_slot(session_user)
    # print("[NEXT SLOT]:", follow_up)

    if slot_filled and not asked_question:
        # print("[SLOT ONLY TURN] No question asked")

        if follow_up:
            # print("[ASK NEXT SLOT]")
            return _say(state, follow_up)

        if session_user.is_complete() and not session_user.wants_to_buy:
            # print("[ALL SLOTS DONE] Showing soft CTA")
            return _say(
                state,
                "If you'd like to move forward, just say:\n"
                "*I'll go with the Pro plan* (or Basic / Enterprise)."
            )

        # print("[NO RESPONSE NEEDED] Ending turn")
        return state

    # --------------------------------------------------
    # 4️⃣ QUESTION ANSWERING (ONLY IF QUESTION EXISTS)
    # --------------------------------------------------
    if not asked_question:
        # print("[NO QUESTION] Nothing to answer → returning state")
        return state

    # print("[QUESTION DETECTED] Answering question")
    answer = ""

    if session_user.wants_pricing:
        # print("[ANSWER MODE] Pricing")

        context = retrieve_context(vector_store, text)
        # print("[RAG CONTEXT FOUND]:", bool(context.strip()))

        if context.strip():
            system = SystemMessage(
                content=(
                    "You are AutoStream's assistant.\n"
                    "Answer ONLY from the context below.\n"
                    "1-2 sentences max.\n\n"
                    f"Context:\n{context}"
                )
            )
            answer = llm.invoke(
                [system, HumanMessage(content=text)]
            ).content.strip()
        else:
            answer = "We offer Basic, Pro, and Enterprise plans."

    elif session_user.wants_info:
        # print("[ANSWER MODE] Info")

        system = SystemMessage(
            content=(
                "You are AutoStream's assistant.\n"
                f"{PRODUCT_SEED}\n\n"
                "- Answer in 1-2 sentences\n"
                "- Do NOT invent features or pricing\n"
            )
        )
        answer = llm.invoke(
            [system, HumanMessage(content=text)]
        ).content.strip()

    else:
        # print("[ANSWER MODE] Chat")
        answer = llm.invoke(state["messages"]).content.strip()

    # Append follow-up slot question if any
    if follow_up:
        answer = f"{answer}\n\n{follow_up}"

    # print("[FINAL ANSWER]:", answer)
    # print("[SESSION AFTER]:", session_user.to_dict())
    # print("[LLM_REPLY] ================= TURN END =================\n")

    return _say(state, answer)


# ---------------- HELPERS ---------------- #

def _next_missing_slot(session_user):
    if not session_user.platform:
        session_user.awaiting_slot = "platform"
        return "Which platform do you mainly create for? (YouTube, Instagram, or Shorts)"
    if not session_user.plan:
        session_user.awaiting_slot = "plan"
        return "Which plan are you considering? (Basic, Pro, or Enterprise)"
    if not session_user.email:
        session_user.awaiting_slot = "email"
        return "What's the best email to send your AutoStream plan details to?"
    if not session_user.first_name:
        session_user.awaiting_slot = "name"
        return (
            "By the way, what should I call you?\n"
            "👉 Type: *my name is First Last* (or *N/A* for last name)"
        )

    session_user.awaiting_slot = None
    return None


def _say(state, text):
    if text and text.strip():
        state["messages"].append(AIMessage(content=text))
    return state

