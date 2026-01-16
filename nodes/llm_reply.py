from state import Agentstate
from llm import llm
from langchain_core.messages import AIMessage, SystemMessage
from session import SessionUser
from logic.lead_qualifier import mock_lead_capture
from debug import trace_node



def llm_reply_node(state: Agentstate, session_user: SessionUser)-> Agentstate:
    trace_node(state, "llm_reply")

    if state.get("replied", False):
        return state
    
    if (
        session_user.mode == "lead"
        and session_user.is_complete()
        and not session_user.lead_submitted
    ):
        mock_lead_capture(
            name=f"{session_user.first_name} {session_user.last_name or ''}".strip(),
            email=session_user.email,
            platform=session_user.platform,
            plan=session_user.plan
        )
        session_user.lead_submitted = True
    context = ""
    if session_user.mode == "chat":
        response = llm.invoke(state["messages"])
        if response.content.strip():
            state["messages"].append(AIMessage(content=response.content))
            state["replied"] = True 
        return state
    
    if session_user.first_name and not session_user.email:
        context = (
            f"The user's name is {session_user.first_name}."
            "Ask them for their email."
        )
    
    elif session_user.email and not session_user.platform:
        context = ("""
                   The user's email is already collected.
                   Ask which platform they create content for
                   (Youtube, Instagram, or Shorts).


""")
    
    elif session_user.mode == "lead" and session_user.is_complete():
        context = (
            "Thank the user and confirm that thier details are captured"
            "for trying AutoStream."
        )

    system_message = SystemMessage(
        content=(
            "You are AutoStream's assistant."
            "Respond Clearly and briefly.\n"
            f"{context}"
        )
    )

    messages = [system_message] + state["messages"]
    response = llm.invoke(messages)

    if response.content.strip():
        state["messages"].append(AIMessage(content=response.content))
        state["replied"] = True 

    return state    
