from agents.common import get_history
from state import GraphState


def human_node(state: GraphState) -> GraphState:
    """Optional terminal node for collecting another user message."""

    response = state.get("response", "")
    print(f"\nAI: {response}")

    human_input = input("USER: ").strip()
    history = [
        *get_history(state),
        f"ASSISTANT: {response}",
        f"USER: {human_input}",
    ]

    return {
        **state,
        "query": human_input,
        "history": history,
    }
