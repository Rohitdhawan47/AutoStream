from graph import build_graph
from session import SessionUser
from state import Agentstate
from langchain_core.messages import HumanMessage
from nodes.greeting import greetingnode
from debug import dump_messages

def main():
    session_user = SessionUser()

    state: Agentstate = {
        "messages": [],
        "trace": [],
        "session_user": session_user

    }

    print("AutoStream Assistant is running. Type 'exit' to quit.\n")
    state = greetingnode(state)
    print(f"Agent: {state['messages'][-1].content}\n")
    graph = build_graph(session_user)


    while True:
        user_input = input("User: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Session ended.")
            break
        state["trace"].clear()

        state["messages"].append(HumanMessage(content=user_input))

        state = graph.invoke(state)
        print("TRACE:", "->".join(state.get("trace", [])))

        last_message = state["messages"][-1]
        print(f"Agent: {last_message.content}\n")


if __name__ == "__main__":
    main()
