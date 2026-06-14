from agents.common import get_history
from state import GraphState


def final_node(state: GraphState) -> GraphState:
    """Append the final response to history when used in a larger graph."""

    response = state.get("response", "")
    return {
        **state,
        "history": [*get_history(state), f"FINAL: {response}"],
    }
