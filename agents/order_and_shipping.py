import logging

from langchain.agents import create_agent
from langchain.tools import tool

from agents.common import get_query, run_agent
from constants.settings import ORDER_SHIPPING_SYSTEM_PROMPT
from model import LLM
from state import GraphState
from tools.order_and_shipping_tool import order_and_shipping_tool


logger = logging.getLogger(__name__)

order_shipping_agent = create_agent(
    model=LLM,
    tools=[order_and_shipping_tool],
    system_prompt=ORDER_SHIPPING_SYSTEM_PROMPT,
    debug=False,
)


def handle_order_and_shipping(state: GraphState) -> str:
    """Handle order status, tracking, delivery, and shipping policy requests."""

    query = get_query(state)
    if not query:
        logger.warning("Invalid or missing user query in graph state")
        return "I didn't catch your order or shipping question. Could you please rephrase it?"

    try:
        return run_agent(order_shipping_agent, query, logger)
    except Exception:
        logger.exception("Order and shipping agent failed")
        return (
            "Sorry, I ran into an issue while processing your order or shipping request. "
            "Please try again shortly."
        )


@tool(
    description=(
        "Handles order and shipping queries such as order status, shipment "
        "tracking, delivery timelines, and shipping policy questions."
    ),
)
def order_and_shipping_node(state: GraphState) -> str:
    return handle_order_and_shipping(state)
