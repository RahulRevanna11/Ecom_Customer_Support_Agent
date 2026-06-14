from langchain_openai import ChatOpenAI

from constants.settings import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL_NAME

llm_model = ChatOpenAI(
    model=LLM_MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
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