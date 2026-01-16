from langgraph.graph import StateGraph, END
from state import Agentstate
from langchain_core.messages import HumanMessage
from nodes.greeting import greetingnode
from nodes.user_input import user_input_node
from nodes.llm_reply import llm_reply_node
from nodes.rule_processor import rule_processor_node
from logic.intent_detector import intent_decider
from logic.rules import is_product_question
from rag.vector_store import build_vector_store
from nodes.rag_reply import rag_reply_node
from nodes.intent_decision import intent_decision_node
def build_graph(session_user):

    def rag_router(state):
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                user_text = msg.content
                break
        else:
            return "normal"

        route = "rag" if is_product_question(user_text) else "normal"
        print("RAG ROUTER →", route)
        return route

    
    vector_store = build_vector_store()
    graph = StateGraph(Agentstate)
    
    graph.add_node("greeting", greetingnode)
    graph.add_node("user_input", user_input_node)
    graph.add_node(
        "llm_reply",
        lambda state: llm_reply_node(state, session_user)
    )
    graph.add_node("intent_decision", intent_decision_node)
    graph.add_node(
        "rule_processor",
        lambda state: rule_processor_node(state, session_user)
    )
    graph.add_node("rag_reply",
                   lambda state: rag_reply_node(state, vector_store))
    

    graph.set_entry_point("user_input")
    graph.add_edge("greeting", "user_input")
    graph.add_edge("user_input", "rule_processor")
    graph.add_edge("rule_processor", "intent_decision")
    graph.add_conditional_edges(
        "intent_decision",
        lambda state: intent_decider(state, session_user),
        {
            "lead":"llm_reply",
            "normal":"llm_reply"
        })
    graph.add_conditional_edges("llm_reply",
                                rag_router,
                                {
                                    "rag": "rag_reply",
                                    "normal": END
                                })
    graph.add_edge("rag_reply", END)


    return graph.compile()

