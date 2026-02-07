from dotenv import load_dotenv
load_dotenv()
from agents.supervisor import supervisor
from graph.workflow import app


query = "Why my order status and my order id is 1234?"


state = {
        "query": "Why my order status and my order id is 1234?",
        "history": [],
       
        "response": ""

    }
result = app.invoke(
  state
)


print(result["query"])

print(result["response"])