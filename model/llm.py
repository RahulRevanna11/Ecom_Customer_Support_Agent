from langchain_google_genai import ChatGoogleGenerativeAI
llm_model = ChatGoogleGenerativeAI(
      model="gemini-2.5-flash-lite",
    temperature=0.7,
    verbose=True
)

# from langchain_xai import ChatXAI

# llm_model = ChatXAI(
#     model="grok-3-mini",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )