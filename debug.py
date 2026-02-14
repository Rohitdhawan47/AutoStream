# Exists only for debugging remove comments in nodes to see the flow
def trace_node(state, name):
    state["trace"]= [*state.get("trace", []), str(name)]

def dump_messages(state):
    print("\n--- MESSAGE STATE ---")
    for i, msg in enumerate(state.get("messages", [])):
        role = msg.__class__.__name__
        content = getattr(msg, "content", str(msg))
        print(f"{i:02d} [{role}] {content}")
    print("--- END STATE ---\n")
