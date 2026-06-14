import logging

from langchain.agents import create_agent
from langchain.tools import tool

from agents.common import get_query, run_agent
from model import LLM
from state import GraphState
from tools.refunds_returns_tool import refunds_returns_tool


logger = logging.getLogger(__name__)


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
    "- If required information is missing, ask politely\n"
    "- Use clear, calm, and reassuring language\n"
    "- Always ask if the customer needs further assistance."
)

refunds_returns_agent = create_agent(
    model=LLM,
    tools=[refunds_returns_tool],
    system_prompt=REFUNDS_RETURNS_SYSTEM_PROMPT,
    debug=False,
)


def handle_refunds_and_returns(state: GraphState) -> str:
    """Handle refunds, returns, eligibility, and refund status requests."""

    query = get_query(state)
    if not query:
        logger.warning("Invalid or missing user query in graph state")
        return "I didn't quite catch your refund or return question. Could you please rephrase?"

    try:
        return run_agent(refunds_returns_agent, query, logger)
    except Exception:
        logger.exception("Refunds and returns agent failed")
        return (
            "Sorry, I ran into an issue while handling your refund or return request. "
            "Please try again in a moment."
        )


@tool(
    description=(
        "Handles refunds and returns requests including policies, eligibility, "
        "return initiation, and refund status."
    ),
)
def refunds_and_returns_node(state: GraphState) -> str:
    return handle_refunds_and_returns(state)
