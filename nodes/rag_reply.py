from langchain_core.messages import SystemMessage, AIMessage
from state import Agentstate
from llm import llm
from rag.retriever import retrieve_context
from debug import trace_node

RAG_CACHE = {}

def rag_reply_node(state: Agentstate, vector_store) -> Agentstate:
    trace_node(state, "rag_reply")


    if state.get("replied", False):
        return state

    last_message = state["messages"][-1]
    question = last_message.content.lower()


    if question in RAG_CACHE:
        answer = RAG_CACHE[question]
    else:

        context = retrieve_context(vector_store, question)


        system_message = SystemMessage(
            content=(
                "You are AutoStream's assistant.\n"
                "Answer ONLY using the context below.\n"
                "If the answer is not in the context, say you don't know.\n\n"
                f"Context:\n{context}"
            )
        )


        response = llm.invoke([system_message])

        answer = response.content
        RAG_CACHE[question] = answer  # cache it


    state["messages"].append(AIMessage(content=answer))
    return state
