from typing import Dict, Any
import logging

from langchain.agents import create_agent
from langchain.tools import tool

from tools.account_login_tool import account_login_tool
from state import GraphState
from model import LLM


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
    "- Respond concisely and clearly"
)

account_login_agent = create_agent(
    model=LLM,
    tools=[account_login_tool],
    system_prompt=ACCOUNT_LOGIN_SYSTEM_PROMPT,
    debug=False,  
)


# -----------------------------------------------------------------------------
# Node Tool (Supervisor → Account/Login Agent)
# -----------------------------------------------------------------------------
@tool(
    description=(
        "Handles account and login requests such as sign-in, password reset, "
        "account creation, and login troubleshooting by delegating to the "
        "Account & Login support agent."
    ),
)
def account_and_login_node(state: GraphState) -> str:
    """
    Entry point for account & login related queries.

    Args:
        state (GraphState): Shared graph state containing user query.

    Returns:
        str: Final agent response text.
    """
    query = state.get("query")

    if not query or not isinstance(query, str):
        logger.warning("Invalid or missing user query in GraphState")
        return "I didn’t receive a valid request. Could you please rephrase?"

    try:
        response: Dict[str, Any] = account_login_agent.invoke(
            {"messages": [("user", query)]}
        )

        messages = response.get("messages", [])
        if not messages:
            logger.error("Agent returned no messages")
            return "Something went wrong while processing your request."

        last_message = messages[-1]
        return last_message.content

    except Exception as exc:
        logger.exception("Account & Login agent failed")
        return (
            "Sorry — I ran into an internal issue while handling your login request. "
            "Please try again in a moment."
        )
