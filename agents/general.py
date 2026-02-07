from typing import Dict, Any
import logging

from langchain.agents import create_agent
from langchain.tools import tool

from state import GraphState
from model import LLM
# import state


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)







@tool(
  
    description=(
        "Handles general user interactions such as greetings, basic questions, "
        "and high-level guidance about system capabilities when no specialized "
        "support agent is required."
    ),
)
def general_node(state: GraphState) -> str:
    """
    Entry point for general user interactions.

    Args:
        state (GraphState): Shared graph state containing the user's query.

    Returns:
        str: Final user-safe response text.
    """
    GENERAL_SUPPORT_SYSTEM_PROMPT = (
    "You are a General Support assistant for an e-commerce platform.\n\n"
    "Your responsibilities include:\n"
    "- Greeting users and engaging politely\n"
    "- Answering general questions\n"
    "- Explaining what kind of help the system can provide\n"
    "- Guiding users to the right type of support\n\n"
    "Guidelines:\n"
    "- Do not provide account, order, refund, or product-specific details\n"
    "- If a request requires a specialized agent, explain that and guide the user\n"
    "- Be friendly, concise, and helpful\n"
    "- Always ask how else you can assist\n"
    f"CONVERSATION HISTORY (for context only): {state['history']}"

)
    general_support_agent = create_agent(
    model=LLM,
    tools=[],  
    system_prompt=GENERAL_SUPPORT_SYSTEM_PROMPT,
    debug=False,  
)
    query = state.get("query")

    if not query or not isinstance(query, str):
        logger.warning("Missing or invalid query in GraphState")
        return "Hi! How can I help you today?"

    try:
        response: Dict[str, Any] = general_support_agent.invoke(
            {"messages": [("user", query)]}
        )

        messages = response.get("messages", [])
        if not messages:
            logger.error("General support agent returned no messages")
            return "Hello! Let me know how I can assist you."

        last_message = messages[-1]
        return last_message.content

    except Exception:
        logger.exception("General support agent execution failed")
        return (
            "Sorry, I ran into a small issue while responding. "
            "How else can I help you today?"
        )
