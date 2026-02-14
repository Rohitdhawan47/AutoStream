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
        "session_user": session_user,
        "slot_filled_this_turn": False
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
        state["slot_filled_this_turn"] = False

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
