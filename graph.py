from langgraph.graph import StateGraph, END
from state import Agentstate
from nodes.rule_processor import rule_processor_node
from nodes.intent_decision import intent_node
from nodes.llm_reply import llm_reply_node
from nodes.rag_reply import rag_reply_node
from rag.vector_store import build_vector_store

def build_graph(session_user):
    vector_store = build_vector_store()
    graph = StateGraph(Agentstate)

    graph.add_node(
        "rule_processor", rule_processor_node)
    graph.add_node(
        "intent",intent_node)
    graph.add_node(
        "llm_reply",llm_reply_node)
    graph.add_node(
        "rag_reply",
        lambda s: rag_reply_node(s, vector_store)
    )

    graph.set_entry_point("rule_processor")

    graph.add_edge("rule_processor", "intent")

    graph.add_conditional_edges(
        "intent",
        lambda s: s["route"],
        {
            "chat": "llm_reply",
            "info": "llm_reply",
            "lead": "llm_reply",
            "pricing": "rag_reply"
        }
    )

    graph.add_edge("llm_reply", END)
    graph.add_edge("rag_reply", END)

    return graph.compile()
