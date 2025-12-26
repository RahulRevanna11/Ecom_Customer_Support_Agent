from dotenv import load_dotenv
load_dotenv()

from graph.workflow import app


# query = "Why i am not able to sign up in system?"4
query = "Why my order status and my order id is 1234?"

result = app.invoke({
    "query": query
})


print(result["query"])
print(result["category"])
# print(result["tone"])
print(result["response"])