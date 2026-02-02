from langchain_core.messages import HumanMessage
from logic.rules import is_pricing_question
from debug import trace_node

# def info_router_node(state):
#     trace_node(state, "info_router")

#     # Default route
#     state["route"] = "llm"

#     # Find last human message
#     for msg in reversed(state["messages"]):
#         if isinstance(msg, HumanMessage):
#             text = msg.content.lower()
#             break
#     else:
#         return state

#     if is_pricing_question(text):
#         print("KNOWLEDGE → pricing (RAG)")
#         state["route"] = "rag"
#     else:
#         print("KNOWLEDGE → product (SEED)")
#         state["route"] = "llm"

#     return state


def info_router_node(state):
    # Find last human message
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            text = msg.content.lower()
            break
    else:
        return "llm"

    # Pricing / plans / subscription → RAG
    if is_pricing_question(text):
        print("KNOWLEDGE → pricing (RAG)")
        return "rag"

    print("KNOWLEDGE → product (SEED)")
    return "llm"
