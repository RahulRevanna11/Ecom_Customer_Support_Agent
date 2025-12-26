from model import LLM
def categorize_node(state):
    prompt=f"""
    Categorize the customer query into exactly one of the following categories.
    Return only the category name with no explanation or extra text.
    
    Categories: Technical, Billing, Order & Shipping, Returns & Refunds, Product Information, Account & Login, General
    
    Query: {state["query"]}
    """
    response=LLM.invoke(prompt)
    return {"category":response.content}