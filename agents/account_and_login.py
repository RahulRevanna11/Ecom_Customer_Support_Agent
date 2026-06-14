import logging

from langchain.agents import create_agent
from langchain.tools import tool

from agents.common import get_query, run_agent
from constants.settings import ACCOUNT_LOGIN_SYSTEM_PROMPT
from model import LLM
from state import GraphState
from tools.account_login_tool import account_login_tool


logger = logging.getLogger(__name__)

account_login_agent = create_agent(
    model=LLM,
    tools=[account_login_tool],
    system_prompt=ACCOUNT_LOGIN_SYSTEM_PROMPT,
    debug=False,
)


def handle_account_and_login(state: GraphState) -> str:
    """Handle account and login related customer requests."""

    query = get_query(state)
    if not query:
        logger.warning("Invalid or missing user query in graph state")
        return "I didn't receive a valid request. Could you please rephrase?"

    try:
        return run_agent(account_login_agent, query, logger)
    except Exception:
        logger.exception("Account and login agent failed")
        return (
            "Sorry, I ran into an internal issue while handling your login request. "
            "Please try again in a moment."
        )


@tool(
    description=(
        "Handles account and login requests such as sign-in, password reset, "
        "account creation, and login troubleshooting."
    ),
)
def account_and_login_node(state: GraphState) -> str:
    return handle_account_and_login(state)
