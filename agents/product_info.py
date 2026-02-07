from typing import Dict, Any
import logging

from langchain.agents import create_agent
from langchain.tools import tool

from tools.product_info_tool import product_info_tool
from state import GraphState
from model import LLM


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
    "- Always ask if the customer needs additional help\n"
)

product_info_agent = create_agent(
    model=LLM,
    tools=[product_info_tool],
    system_prompt=PRODUCT_INFO_SYSTEM_PROMPT,
    debug=False, 
)



@tool(

    description=(
        "Provides product details such as features, pricing, availability, "
        "and descriptions by delegating to the Product Information support agent."
    ),
)
def product_info_node(state: GraphState) -> str:
    """
    Entry point for product information related queries.

    Args:
        state (GraphState): Shared graph state containing the user's query.

    Returns:
        str: Final user-safe response text.
    """
    query = state.get("query")

    if not query or not isinstance(query, str):
        logger.warning("Missing or invalid query in GraphState")
        return "Could you please tell me which product you’d like information about?"

    try:
        response: Dict[str, Any] = product_info_agent.invoke(
            {"messages": [("user", query)]}
        )

        messages = response.get("messages", [])
        if not messages:
            logger.error("Product Info agent returned no messages")
            return "I wasn’t able to retrieve the product details right now."

        last_message = messages[-1]
        return last_message.content

    except Exception:
        logger.exception("Product Info agent execution failed")
        return (
            "Sorry, something went wrong while fetching product information. "
            "Please try again in a moment."
        )
