from typing import Dict, Any
import logging

from langchain.agents import create_agent
from langchain.tools import tool

from tools.refunds_returns_tool import refunds_returns_tool
from state import GraphState
from model import LLM


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


REFUNDS_RETURNS_SYSTEM_PROMPT = (
    "You are a Refunds & Returns support agent for an e-commerce platform.\n\n"
    "Your responsibilities include:\n"
    "- Explaining return and refund policies\n"
    "- Checking refund eligibility\n"
    "- Initiating returns when requested\n"
    "- Providing refund status updates\n\n"
    "Guidelines:\n"
    "- Use tools only when order-specific data is required\n"
    "- Never fabricate refund amounts, timelines, or order details\n"
    "- If required information (order ID, item, reason) is missing, ask politely\n"
    "- Use clear, calm, and reassuring language\n"
    "- Always ask if the customer needs further assistance\n"
)

refunds_returns_agent = create_agent(
    model=LLM,
    tools=[refunds_returns_tool],
    system_prompt=REFUNDS_RETURNS_SYSTEM_PROMPT,
    debug=False,  
)


# -----------------------------------------------------------------------------
# Node Tool (Supervisor → Refunds & Returns Agent)
# -----------------------------------------------------------------------------
@tool(
   
    description=(
        "Handles refunds and returns requests including policies, eligibility, "
        "return initiation, and refund status by delegating to the "
        "Refunds & Returns support agent."
    ),
)
def refunds_and_returns_node(state: GraphState) -> str:
    """
    Entry point for refunds & returns related queries.

    Args:
        state (GraphState): Shared graph state containing the user's query.

    Returns:
        str: Final user-safe response text.
    """
    query = state.get("query")

    if not query or not isinstance(query, str):
        logger.warning("Missing or invalid query in GraphState")
        return "I didn’t quite catch your refund or return question. Could you please rephrase?"

    try:
        response: Dict[str, Any] = refunds_returns_agent.invoke(
            {"messages": [("user", query)]}
        )

        messages = response.get("messages", [])
        if not messages:
            logger.error("Refunds & Returns agent returned no messages")
            return "Something went wrong while checking your refund or return request."

        last_message = messages[-1]
        return last_message.content

    except Exception:
        logger.exception("Refunds & Returns agent execution failed")
        return (
            "Sorry, I ran into an issue while handling your refund or return request. "
            "Please try again in a moment."
        )
