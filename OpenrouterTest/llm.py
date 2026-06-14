import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI

api_key=os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("Error: OPENROUTER_API_KEY is missing.")


llm = ChatOpenAI(
    model="google/gemma-4-31b-it:free",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)
response = llm.invoke("Explain quantum computing")

# Use dot notation as required by the native OpenAI python SDK
print(response.content)
