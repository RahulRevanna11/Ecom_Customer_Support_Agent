from tools.account_login_tool import account_login_tool
from state import GraphState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from model import LLM


agent_executor = create_agent(
model=LLM,
tools=[account_login_tool],
system_prompt=(
        "You are an Account & Login support agent. "
        "Help users with login issues, password resets, and account creation. "
        "Use tools if they help you complete the task. "
        "If no tool is needed, respond directly."
    ),
debug=True,
)



def account_and_login_node(state: GraphState) -> GraphState:
    result = agent_executor.invoke({
        "messages": [("user", state["query"])]
    })

    return {
      **state,
        "response": result["messages"][-1].content
    }

