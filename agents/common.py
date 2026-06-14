import logging
from typing import Any, Dict

from state import GraphState


def get_query(state: GraphState) -> str:
    """Return the current user query, or an empty string when invalid."""

    query = state.get("query", "")
    return query.strip() if isinstance(query, str) else ""


def get_history(state: GraphState) -> list[str]:
    """Return a mutable conversation history list."""

    history = state.get("history")
    return history if isinstance(history, list) else []


def extract_last_message(response: Dict[str, Any]) -> str:
    """Extract the final model message text from a LangChain agent response."""

    messages = response.get("messages", [])
    if not messages:
        raise ValueError("Agent returned no messages")

    content = getattr(messages[-1], "content", "")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Agent returned an empty final message")

    return content.strip()


def run_agent(agent: Any, query: str, logger: logging.Logger) -> str:
    """Invoke a LangChain agent and return its final response text."""

    response = agent.invoke({"messages": [("user", query)]})
    logger.debug("Agent response: %s", response)
    return extract_last_message(response)
