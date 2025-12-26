from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage,AIMessage

from langchain.messages import HumanMessage, SystemMessage,AIMessage
from tools.order_and_shipping_tool import order_and_shipping_tool
from state import GraphState
from model import LLM




agent_executor = create_agent(
model=LLM,
tools=[order_and_shipping_tool],
debug=True,
)



agent_executor = create_agent(
model=LLM,
tools=[order_and_shipping_tool],
system_prompt=(
      "You are an Order & Shipping support agent.\n"
        "Your job is to help users with:\n"
        "- Order status\n"
        "- Shipment tracking\n"
        "- Delivery timelines\n"
        "- Shipping policies\n\n"
        "If the request involves checking or tracking an order, "
        "extract the order ID if provided.\n"
        "Use tools when real order information is required.\n"
    ),
debug=True,
)



def order_and_shipping_node(state: GraphState) -> GraphState:
    result = agent_executor.invoke({
        "messages": [("user", state["query"])]
    })

  
    return {
      **state,
        "response": result["messages"][-1].content
    }


