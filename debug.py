def trace_node(state, name):
    state["trace"].append(name)
    return state