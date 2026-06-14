import logging

from langchain.agents import create_agent
from langchain.tools import tool

from agents.common import get_query, run_agent
from model import LLM
from state import GraphState
from tools.product_info_tool import product_info_tool


logger = logging.getLogger(__name__)


PRODUCT_INFO_SYSTEM_PROMPT = (
    "You are a Product Information support agent for an e-commerce platform.\n\n"
    "Your responsibilities include:\n"
    "- Providing product features and specifications\n"
    "- Sharing pricing information\n"
    "- Checking product availability\n"
    "- Giving clear and accurate product descriptions\n\n"
    "Guidelines:\n"
    "- Use tools only when product-specific or real-time data is required\n"
    "- Never fabricate pricing, discounts, availability, or specifications\n"
    "- If the product name or identifier is missing, ask for clarification\n"
    "- Keep responses clear, concise, and customer-friendly\n"
    "- Always ask if the customer needs additional help."
)

product_info_agent = create_agent(
    model=LLM,
    tools=[product_info_tool],
    system_prompt=PRODUCT_INFO_SYSTEM_PROMPT,
    debug=False,
)


def handle_product_info(state: GraphState) -> str:
    """Handle product feature, price, availability, and description requests."""

    query = get_query(state)
    if not query:
        logger.warning("Invalid or missing user query in graph state")
        return "Could you please tell me which product you'd like information about?"

    try:
        return run_agent(product_info_agent, query, logger)
    except Exception:
        logger.exception("Product information agent failed")
        return (
            "Sorry, something went wrong while fetching product information. "
            "Please try again in a moment."
        )


@tool(
    description=(
        "Provides product details such as features, pricing, availability, "
        "and descriptions."
    ),
)
def product_info_node(state: GraphState) -> str:
    return handle_product_info(state)
