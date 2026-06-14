import logging
from enum import Enum
from typing import Callable

from agents.account_and_login import handle_account_and_login
from agents.common import get_history, get_query
from agents.general import handle_general
from agents.order_and_shipping import handle_order_and_shipping
from agents.product_info import handle_product_info
from agents.refunds_and_returns import handle_refunds_and_returns
from model import LLM
from state import GraphState


logger = logging.getLogger(__name__)


class SupportRoute(str, Enum):
    ACCOUNT = "account_and_login"
    GENERAL = "general"
    ORDER = "order_and_shipping"
    PRODUCT = "product_info"
    REFUNDS = "refunds_and_returns"


ROUTE_HANDLERS: dict[SupportRoute, Callable[[GraphState], str]] = {
    SupportRoute.ACCOUNT: handle_account_and_login,
    SupportRoute.GENERAL: handle_general,
    SupportRoute.ORDER: handle_order_and_shipping,
    SupportRoute.PRODUCT: handle_product_info,
    SupportRoute.REFUNDS: handle_refunds_and_returns,
}


ROUTE_KEYWORDS: dict[SupportRoute, tuple[str, ...]] = {
    SupportRoute.ACCOUNT: (
        "account",
        "login",
        "log in",
        "sign in",
        "sign up",
        "password",
        "profile",
    ),
    SupportRoute.ORDER: (
        "order",
        "shipping",
        "shipment",
        "track",
        "tracking",
        "delivery",
        "delivered",
    ),
    SupportRoute.PRODUCT: (
        "product",
        "price",
        "pricing",
        "availability",
        "available",
        "stock",
        "feature",
        "spec",
    ),
    SupportRoute.REFUNDS: (
        "refund",
        "return",
        "replacement",
        "exchange",
        "cancel",
        "cancellation",
    ),
}


def _build_routing_prompt(query: str, history: list[str]) -> str:
    """Build a prompt for the LLM to classify the query into a support route."""
    
    history_text = "\n".join(history[-6:]) if history else "No conversation history"
    
    return f"""You are a customer support router. Classify the following customer query into ONE of these categories:

CATEGORIES:
1. account_and_login - Account access, login issues, password reset, sign up, profile management
2. order_and_shipping - Orders, tracking, shipments, delivery status, order status
3. product_info - Product details, pricing, features, specifications, availability, stock
4. refunds_and_returns - Refunds, returns, exchanges, replacements, cancellations
5. general - Greetings, general questions, unclear requests, anything else

CONVERSATION HISTORY:
{history_text}

CUSTOMER QUERY: {query}

Respond with ONLY the category name (e.g., "account_and_login") and a brief reason on the next line. Do not include any other text."""


def route_query(state: GraphState) -> str:
    """Use the LLM to intelligently classify and route the query to the right agent."""
    
    query = get_query(state)
    history = get_history(state)
    
    if not query:
        logger.warning("Invalid or missing user query in graph state")
        return "general"
    
    prompt = _build_routing_prompt(query, history)
    
    try:
        # Invoke the LLM to classify the query
        response = LLM.invoke(prompt)
        response_text = response.content.strip().lower()
        
        # Extract the first line (the category name)
        category = response_text.split('\n')[0].strip()
        
        logger.debug(f"LLM routing response: {response_text}")
        
        # Map the response to a SupportRoute
        for route in SupportRoute:
            if route.value in category:
                logger.info(f"LLM routed query to: {route.value}")
                return route.value
        
        # Fallback to GENERAL if LLM response doesn't match any route
        logger.warning(f"LLM response '{category}' didn't match any route, defaulting to GENERAL")
        return SupportRoute.GENERAL.value
        
    except Exception as e:
        logger.error(f"LLM routing failed: {e}, falling back to GENERAL")
        return SupportRoute.GENERAL.value


def supervisor(state: GraphState) -> GraphState:
    """Supervisor node - routes query and updates history with response."""

    query = get_query(state)
    history = get_history(state)
    
    # Get the route from the router
    route = route_query(state)
    
    logger.info("LLM routed customer query to %s", route)
    
    # Get the appropriate handler and execute it
    handler = ROUTE_HANDLERS.get(SupportRoute(route), handle_general)
    response = handler(state)

    updated_history = [
        *history,
        f"USER: {query}",
        f"ASSISTANT: {response}",
    ]

    return {
        **state,
        "query": query,
        "response": response,
        "history": updated_history,
    }
