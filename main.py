# from graph import build_graph
# from session import SessionUser
# from state import AgentState
# from langchain_core.messages import HumanMessage
# from nodes.greeting import greetingnode
# from rag.vector_store import build_vector_store

# def main():
#     session_user = SessionUser()

#     state: AgentState = {
#         "messages": [],
#         "vector_store": build_vector_store(),
#         "session_user": session_user

#     }

#     print("AutoStream Assistant is running. Type 'exit' to quit.\n")
#     state = greetingnode(state)
#     print(f"Agent: {state['messages'][-1].content}\n")
#     graph = build_graph(session_user)


#     while True:
#         user_input = input("User: ").strip()

#         if user_input.lower() in ["exit", "quit"]:
#             print("Session ended.")
#             break
#         state["trace"].clear()

#         state["messages"].append(HumanMessage(content=user_input))

#         state = graph.invoke(state)
#         print("TRACE:", "->".join(state.get("trace", [])))

#         last_message = state["messages"][-1]
#         print(f"Agent: {last_message.content}\n")


# if __name__ == "__main__":
#     main()
# from graph import build_graph
# from session import SessionUser
# from state import AgentState
# from langchain_core.messages import HumanMessage
# from nodes.greeting import greetingnode
# from rag.vector_store import build_vector_store

# def main():
#     state: AgentState = {
#         "messages": [],
#         "session_user": SessionUser(),
#         "vector_store": build_vector_store()
#     }

#     print("AutoStream Assistant is running. Type 'exit' to quit.\n")

#     # Greeting
#     state = greetingnode(state)
#     print(f"Agent: {state['messages'][-1].content}\n")

#     graph = build_graph()

#     while True:
#         user_input = input("User: ").strip()

#         if user_input.lower() in ["exit", "quit"]:
#             print("Session ended.")
#             break

#         state["messages"].append(HumanMessage(content=user_input))

#         state = graph.invoke(state)

#         last_message = state["messages"][-1]
#         print(f"Agent: {last_message.content}\n")

# if __name__ == "__main__":
#     main()

from graph import build_graph
from session import SessionUser
from state import AgentState
from langchain_core.messages import HumanMessage
from nodes.greeting import greetingnode

def main():
    # Persistent user memory (ONE per session)
    session_user = SessionUser()

    # Initial graph state
    state: AgentState = {
        "messages": [],
        "trace": [],
        "session_user": session_user
    }

    print("AutoStream Assistant is running. Type 'exit' to quit.\n")

    # Initial greeting (no graph run)
    state = greetingnode(state)
    print(f"Agent: {state['messages'][-1].content}\n")

    # Build graph ONCE
    graph = build_graph()

    while True:
        user_input = input("User: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Session ended.")
            break

        # Reset per-turn debug trace
        state["trace"].clear()

        # Append user message
        state["messages"].append(HumanMessage(content=user_input))

        # Run graph
        state = graph.invoke(state)

        # Debug path
        print("TRACE:", " -> ".join(state["trace"]))

        # Last assistant reply
        last_message = state["messages"][-1]
        print(f"Agent: {last_message.content}\n")

if __name__ == "__main__":
    main()
