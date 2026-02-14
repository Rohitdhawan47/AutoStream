# # from langgraph.graph import StateGraph, END
# # from state import Agentstate
# # from nodes.llm_reply import llm_reply_node
# # from nodes.rule_processor import rule_processor_node
# # from nodes.rag_reply import rag_reply_node
# # from nodes.info_router import info_router_node
# # from logic.intent_detector import intent_decider
# # from nodes.intent_decision import intent_decision_node
# # from rag.vector_store import build_vector_store

# # def build_graph(session_user):
# #     vector_store = build_vector_store()
# #     graph = StateGraph(Agentstate)

# #     # Nodes
# #     graph.add_node(
# #         "rule_processor",
# #         lambda state: rule_processor_node(state, session_user)
# #     )
# #     graph.add_node("intent_decision", intent_decision_node)
    
# #     graph.add_node("info_router", info_router_node)

# #     graph.add_node(
# #         "llm_reply",
# #         lambda state: llm_reply_node(state, session_user)
# #     )
# #     graph.add_node(
# #         "rag_reply",
# #         lambda state: rag_reply_node(state, vector_store)
# #     )

# #     # Entry
# #     graph.set_entry_point("rule_processor")

# #     # Flow
# #     graph.add_edge("rule_processor", "intent_decision")


# #     # Intent decides path
# #     graph.add_conditional_edges(
# #         "intent_decision",
# #         lambda state: intent_decider(state, session_user),
# #         {
# #             "chat": "llm_reply",
# #             "lead": "llm_reply",
# #             "info": "info_router"
# #         }
# #     )

# #     # Info router decides knowledge source
# #     graph.add_conditional_edges(
# #         "info_router",
# #         lambda state: state["route"],
# #         {
# #             "rag": "rag_reply",
# #             "llm": "llm_reply"
# #         }
# #     )

# #     # All replies END
# #     graph.add_edge("llm_reply", END)
# #     graph.add_edge("rag_reply", END)

# #     return graph.compile()

# from langgraph.graph import StateGraph, END
# from state import AgentState
# from nodes.rule_processor import rule_processor_node
# from nodes.intent_decision import intent_node
# from nodes.llm_reply import llm_reply_node
# from nodes.rag_reply import rag_reply_node
# from rag.vector_store import build_vector_store

# def build_graph(session_user):
#     vector_store = build_vector_store()
#     graph = StateGraph(AgentState)

#     graph.add_node(
#         "rule_processor", rule_processor_node)
#     graph.add_node(
#         "intent",intent_node)
#     graph.add_node(
#         "llm_reply",llm_reply_node)
#     graph.add_node(
#         "rag_reply",
#         lambda s: rag_reply_node(s, vector_store)
#     )

#     graph.set_entry_point("rule_processor")

#     graph.add_edge("rule_processor", "intent")

#     graph.add_conditional_edges(
#         "intent",
#         lambda s: s["route"],
#         {
#             "chat": "llm_reply",
#             "info": "llm_reply",
#             "lead": "llm_reply",
#             "pricing": "rag_reply"
#         }
#     )

#     graph.add_edge("llm_reply", END)
#     graph.add_edge("rag_reply", END)

#     return graph.compile()
# from langgraph.graph import StateGraph, END
# from state import AgentState
# from logic.lead_controller import lead_controller

# def build_graph():
#     graph = StateGraph(AgentState)

#     graph.add_node("brain", lead_controller)

#     graph.set_entry_point("brain")
#     graph.add_edge("brain", END)

#     return graph.compile()
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.rule_processor import rule_processor_node
from nodes.intent_decision import intent_node
from nodes.llm_reply import llm_reply_node
from rag.vector_store import build_vector_store

def build_graph():
    graph = StateGraph(AgentState)
    vector_store = build_vector_store()
    # --------------------
    # Nodes
    # --------------------
    graph.add_node("rule_processor", rule_processor_node)
    graph.add_node("intent", intent_node)
    graph.add_node(
    "llm_reply",
    lambda s: llm_reply_node(s, vector_store)
)


    # --------------------
    # Entry point
    # --------------------
    graph.set_entry_point("rule_processor")

    # --------------------
    # Flow
    # --------------------
    graph.add_edge("rule_processor", "intent")
    graph.add_edge("intent", "llm_reply")
    graph.add_edge("llm_reply", END)

    return graph.compile()
