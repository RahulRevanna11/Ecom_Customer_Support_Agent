from typing import List, Optional

from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class GraphState(TypedDict, total=False):
    """Shared state passed between LangGraph nodes."""

    query: str
    response: str
    history: List[str]
    route: str  # Store the routing decision from the LLM


class SupervisorOutput(BaseModel):
    """Structured output returned by the supervisor."""

    response: str = Field(description="Final response to show the customer.")


def build_initial_state(query: str, history: Optional[List[str]] = None) -> GraphState:
    """Create a valid initial graph state for one customer turn."""

    return {
        "query": query,
        "history": list(history or []),
        "response": "",
    }
