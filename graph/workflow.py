from agents.account_and_login import account_and_login_node
from agents.category import categorize_node
from agents.order_and_shipping import order_and_shipping_node
from state import GraphState

from langgraph.graph import StateGraph, END
from utils.router_node import router_node


# Create the graph
graph = StateGraph(GraphState)

# Add nodes
graph.add_node("category", categorize_node)
graph.add_node("router", router_node)
graph.add_node("account_and_login", account_and_login_node)
graph.add_node("order_and_shipping", order_and_shipping_node)

# Add edges
# graph.add_edge("category", "router")

graph.add_conditional_edges(
    "category",
    router_node,
    {
        "account_and_login": "account_and_login",
        "order_and_shipping": "order_and_shipping",
        # "billing": "billing",
        # "general": "general",
    },
)

graph.add_edge("account_and_login", END)
graph.add_edge("order_and_shipping", END)

# Set entry point
graph.set_entry_point("category")

# Compile graph
app = graph.compile()
