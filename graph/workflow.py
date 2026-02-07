
from langgraph.graph import StateGraph
from state import GraphState
from agents.supervisor import supervisor 
from agents.human import human_node
from agents.final import final_node

graph = StateGraph(GraphState)



graph.add_node("supervisor", supervisor)
graph.add_node("human", human_node)
# graph.add_node("final", final_node)

# graph.add_conditional_edges(
#     "supervisor",
#     lambda s: s["next"],
#     {
#         "human": "human",
#         "final": "final",
#     }
# )

graph.add_edge("supervisor", "human")
graph.add_edge("human", "supervisor")


graph.set_entry_point("supervisor")

app = graph.compile()
