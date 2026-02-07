from state import GraphState

def human_node(state: GraphState) -> GraphState:
    # Show assistant message
    print(f"\nAI: {state['response']}")

    # ⌨️ Read from terminal
    human_input = input("USER: ")

    # Update state
    state["history"].append(f"AI: {state['response']}")
    state["history"].append(f"USER: {human_input}")
    state["query"] = human_input
    state["next"] = "supervisor"

    return state
