# final.py
from state import GraphState

def final_node(state: GraphState) -> GraphState:
    state["history"].append(f"FINAL: {state['response']}")
    return state
