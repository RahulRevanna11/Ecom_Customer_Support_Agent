import logging

from langchain.agents import create_agent
from langchain.tools import tool

from agents.common import get_query, run_agent
from model import LLM
from state import GraphState
from tools.account_login_tool import account_login_tool


logger = logging.getLogger(__name__)


ACCOUNT_LOGIN_SYSTEM_PROMPT = (
    "You are an Account & Login support agent for an e-commerce platform.\n"
    "Your responsibilities include:\n"
    "- Helping users sign in\n"
    "- Resetting passwords\n"
    "- Creating new accounts\n"
    "- Troubleshooting login issues\n\n"
    "Rules:\n"
    "- Use tools only when required\n"
    "- Never guess credentials or tokens\n"
    "- If information is missing, ask a clear follow-up question\n"
    "- Respond concisely and clearly."
)

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
