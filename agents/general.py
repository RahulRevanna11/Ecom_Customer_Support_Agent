import logging

from langchain.agents import create_agent
from langchain.tools import tool

from agents.common import get_history, get_query, run_agent
from constants.settings import GENERAL_SYSTEM_PROMPT
from model import LLM
from state import GraphState


logger = logging.getLogger(__name__)


def _build_prompt(state: GraphState) -> str:
    history = get_history(state)
    return f"{GENERAL_SYSTEM_PROMPT}\n\nConversation history for context only: {history}"


def handle_general(state: GraphState) -> str:
    """Handle greetings, unclear requests, and general support questions."""

    query = get_query(state)
    if not query:
        logger.warning("Invalid or missing user query in graph state")
        return "Hi! How can I help you today?"

    general_support_agent = create_agent(
        model=LLM,
        tools=[],
        system_prompt=_build_prompt(state),
        debug=False,
    )

    try:
        return run_agent(general_support_agent, query, logger)
    except Exception:
        logger.exception("General support agent failed")
        return (
            "Sorry, I ran into a small issue while responding. "
            "How else can I help you today?"
        )


@tool(
    description=(
        "Handles general user interactions such as greetings, basic questions, "
        "and high-level guidance when no specialized support agent is required."
    ),
)
def general_node(state: GraphState) -> str:
    return handle_general(state)
