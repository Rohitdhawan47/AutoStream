from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from state import Agentstate
from llm import llm
from rag.retriever import retrieve_context
from debug import trace_node

RAG_CACHE = {}

def rag_reply_node(state: Agentstate, vector_store) -> Agentstate:
    trace_node(state, "rag_reply")

    last_message = state["messages"][-1]
    question = last_message.content.lower()

    # Cache hit
    if question in RAG_CACHE:
        state["messages"].append(
            AIMessage(content=RAG_CACHE[question])
        )
        return state

    # Retrieve from vector DB
    context = retrieve_context(vector_store, question)

    # Hard stop only if NOTHING was retrieved
    if not context.strip():
        answer = (
            "I don't have that information yet. "
            "I can help with AutoStream's pricing, plans, or features."
        )
        RAG_CACHE[question] = answer
        state["messages"].append(AIMessage(content=answer))
        return state

    system_message = SystemMessage(
        content=(
            "You are AutoStream's assistant.\n"
            "Answer the user's QUESTION using ONLY the context below.\n\n"
            "Rules:\n"
            "- Answer in 1–2 sentences\n"
            "- Do NOT list features or plans unless asked\n"
            "- Do NOT invent information\n"
            "- If the answer is not in the context, say: "
            "'I don't have that information yet.'\n\n"
            f"Context:\n{context}"
        )
    )

    response = llm.invoke([
        system_message,
        HumanMessage(content=question)
    ])

    answer = response.content.strip()
    RAG_CACHE[question] = answer

    state["messages"].append(AIMessage(content=answer))
    return state
