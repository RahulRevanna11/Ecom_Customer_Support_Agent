from langgraph.graph import END, StateGraph

from agents.supervisor import route_query
from agents.account_and_login import handle_account_and_login
from agents.order_and_shipping import handle_order_and_shipping
from agents.product_info import handle_product_info
from agents.refunds_and_returns import handle_refunds_and_returns
from agents.general import handle_general
from state import GraphState


def router_node(state: GraphState) -> GraphState:
    """Route the query to the appropriate agent using LLM classification and store route in state."""
    route = route_query(state)
    return {**state, "route": route}


def account_node(state: GraphState) -> GraphState:
    """Account and login support node."""
    response = handle_account_and_login(state)
    return {**state, "response": response}


def order_node(state: GraphState) -> GraphState:
    """Order and shipping support node."""
    response = handle_order_and_shipping(state)
    return {**state, "response": response}


def product_node(state: GraphState) -> GraphState:
    """Product info support node."""
    response = handle_product_info(state)
    return {**state, "response": response}


def refunds_node(state: GraphState) -> GraphState:
    """Refunds and returns support node."""
    response = handle_refunds_and_returns(state)
    return {**state, "response": response}


def general_node(state: GraphState) -> GraphState:
    """General support node."""
    response = handle_general(state)
    return {**state, "response": response}


def conditional_router(state: GraphState) -> str:
    """Read the route from state and return the node name."""
    route = state.get("route", "general")
    
    route_mapping = {
        "account_and_login": "account_and_login",
        "order_and_shipping": "order_and_shipping",
        "product_info": "product_info",
        "refunds_and_returns": "refunds_and_returns",
        "general": "general",
    }
    
    return route_mapping.get(route, "general")


def build_workflow():
    """Build and compile the customer support workflow with LangGraph routing."""

    graph = StateGraph(GraphState)
    
    # Add all agent nodes
    graph.add_node("account_and_login", account_node)
    graph.add_node("order_and_shipping", order_node)
    graph.add_node("product_info", product_node)
    graph.add_node("refunds_and_returns", refunds_node)
    graph.add_node("general", general_node)
    
    # Set entry point
    graph.set_entry_point("router")
    
    # Add conditional routing node
    graph.add_node("router", router_node)
    
    # Add conditional edges from router to each agent
    graph.add_conditional_edges(
        "router",
        conditional_router,
        {
            "account_and_login": "account_and_login",
            "order_and_shipping": "order_and_shipping",
            "product_info": "product_info",
            "refunds_and_returns": "refunds_and_returns",
            "general": "general",
        }
    )
    
    # All agent nodes connect to END
    graph.add_edge("account_and_login", END)
    graph.add_edge("order_and_shipping", END)
    graph.add_edge("product_info", END)
    graph.add_edge("refunds_and_returns", END)
    graph.add_edge("general", END)
    
    return graph.compile()


app = build_workflow()
