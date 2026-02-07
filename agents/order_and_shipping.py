from typing import Dict, Any
import logging

from langchain.agents import create_agent
from langchain.tools import tool

from tools.order_and_shipping_tool import order_and_shipping_tool
from state import GraphState
from model import LLM

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ORDER_SHIPPING_SYSTEM_PROMPT = (
    "You are an Order & Shipping support agent for an e-commerce platform.\n\n"
    "Your responsibilities include:\n"
    "- Providing order status updates\n"
    "- Tracking shipments\n"
    "- Explaining delivery timelines\n"
    "- Clarifying shipping policies\n\n"
    "Guidelines:\n"
    "- If an order ID is required and missing, ask for it politely\n"
    "- Use tools only when real order data is needed\n"
    "- Never fabricate order details\n"
    "- Use clear, assistive, and reassuring language\n"
    "- Always ask if the user needs further help\n"
)

order_shipping_agent = create_agent(
    model=LLM,
    tools=[order_and_shipping_tool],
    system_prompt=ORDER_SHIPPING_SYSTEM_PROMPT,
    debug=False,  
)


# -----------------------------------------------------------------------------
# Node Tool (Supervisor → Order & Shipping Agent)
# -----------------------------------------------------------------------------
@tool(
    description=(
        "Handles order and shipping queries such as order status, shipment "
        "tracking, delivery timelines, and shipping policy questions by "
        "delegating to the Order & Shipping support agent."
    ),
)
def order_and_shipping_node(state: GraphState) -> str:
    """
    Entry point for order and shipping related queries.

    Args:
        state (GraphState): Shared graph state containing the user's query.

    Returns:
        str: Final response text safe for the end user.
    """
    query = state.get("query")

    if not query or not isinstance(query, str):
        logger.warning("Missing or invalid query in GraphState")
        return "I didn’t catch your order or shipping question. Could you please rephrase it?"

    try:
        response: Dict[str, Any] = order_shipping_agent.invoke(
            {"messages": [("user", query)]}
        )

        messages = response.get("messages", [])
        if not messages:
            logger.error("Order & Shipping agent returned no messages")
            return "Something went wrong while checking your order details."

        last_message = messages[-1]
        return last_message.content

    except Exception:
        logger.exception("Order & Shipping agent execution failed")
        return (
            "Sorry, I ran into an issue while processing your order or shipping request. "
            "Please try again shortly."
        )
