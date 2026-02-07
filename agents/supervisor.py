import re
from model import LLM
from agents.account_and_login import account_and_login_node
from agents.general import general_node
from agents.order_and_shipping import order_and_shipping_node
from agents.product_info import product_info_node
from langchain.agents import create_agent
from state import SupervisorOutput
import json



from langchain.tools import tool



def supervisor(state):
    SUPERVISOR_PROMPT = f"""
You are a routing supervisor in a customer support system.

Your role is CONTROL ONLY. You do not chat with the user.


AVAILABLE TOOLS:
- account_and_login_tool → login issues, password reset, account access
- order_and_shipping_tool → order status, tracking, shipping
- general_tool → greetings, unclear or unsupported requests

After the tool executes, you must decide whether more
information is required from the user.

You MUST return a VALID JSON object with EXACTLY this schema:

{{
  "response": "<tool response to show the user>",
}}

STRICT RULES:
- ALWAYS call exactly one tool.
- ALWAYS return valid JSON.
- Use true/false as BOOLEAN values (not strings).
- Do NOT include any text outside the JSON.

CONVERSATION HISTORY (for context only):
{state["history"]}
"""


    agent = create_agent(
        model=LLM,
        tools=[
            account_and_login_node,
            order_and_shipping_node,
            general_node,
            product_info_node,
            
        ],
        system_prompt=SUPERVISOR_PROMPT,
        debug=False,
            response_format=SupervisorOutput,  # 🔥 THIS IS THE FIX

    )
    print(f"Query : {state['query']}")
    st='***********************************************************************************************************************************************'
    result = agent.invoke({"messages": [("user", state["query"])]})
    # print('')
 
    last_message = result['messages'][-1].content

    # print(st)
    # print(last_message)
    

    # print(st)
    # print(result)

    # structured = result["response"]
    
    cleaned = re.sub(r"```json|```", "", last_message).strip()
  
    # Parse JSON
    response = json.loads(cleaned)



    print("*************************************************************************************************************")
    # print(tool_response)
    # supervisor_output = json.loads(last_message)

    # supervisor_output = json.loads(last_message)
    # print(last_message)
    # print(st)
    # print(supervisor_output)
    # response = supervisor_output["response"]
    print(f"response:{response}")


    state["history"].append(f"USER: {state['query']}")
    state["history"].append(f"AI: {response}")

    return {
        **state,
        "response": response,
       
    }