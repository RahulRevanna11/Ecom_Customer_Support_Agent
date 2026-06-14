import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Error: OPENROUTER_API_KEY is missing.")

LLM_MODEL_NAME = "google/gemma-4-31b-it:free"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

ROUTER_CATEGORIES = {
    "account_and_login": "Account access, login issues, password reset, sign up, profile management",
    "order_and_shipping": "Orders, tracking, shipments, delivery status, order status",
    "product_info": "Product details, pricing, features, specifications, availability, stock",
    "refunds_and_returns": "Refunds, returns, exchanges, replacements, cancellations",
    "general": "Greetings, general questions, unclear requests, anything else",
}

ROUTER_PROMPT_TEMPLATE = (
    "You are a customer support router. Classify the following customer query into ONE of these categories:\n\n"
    "CATEGORIES:\n"
    "1. account_and_login - Account access, login issues, password reset, sign up, profile management\n"
    "2. order_and_shipping - Orders, tracking, shipments, delivery status, order status\n"
    "3. product_info - Product details, pricing, features, specifications, availability, stock\n"
    "4. refunds_and_returns - Refunds, returns, exchanges, replacements, cancellations\n"
    "5. general - Greetings, general questions, unclear requests, anything else\n\n"
    "CONVERSATION HISTORY:\n{history_text}\n\n"
    "CUSTOMER QUERY: {query}\n\n"
    "Respond with ONLY the category name (e.g., \"account_and_login\") and a brief reason on the next line. Do not include any other text."
)

ACCOUNT_LOGIN_SYSTEM_PROMPT = (
    "You are an Account & Login support agent for an e-commerce platform.\n"
    "Your responsibilities include:\n"
    "- Helping users sign in\n"
    "- Resetting passwords\n"
    "- Creating new accounts\n"
    "- Troubleshooting login issues\n\n"
    "Rules:\n"
    "- Use tools only when required\n"
    "- Never guess credentials or tokens\n"
    "- If information is missing, ask a clear follow-up question\n"
    "- Respond concisely and clearly."
)

ORDER_SHIPPING_SYSTEM_PROMPT = (
    "You are an Order & Shipping support agent for an e-commerce platform.\n\n"
    "Your responsibilities include:\n"
    "- Providing order status updates\n"
    "- Tracking shipments\n"
    "- Explaining delivery timelines\n"
    "- Clarifying shipping policies\n\n"
    "Guidelines:\n"
    "- If an order ID is required and missing, ask for it politely\n"
    "- Use tools only when real order data is needed\n"
    "- Never fabricate order details\n"
    "- Use clear, assistive, and reassuring language\n"
    "- Always ask if the user needs further help."
)

PRODUCT_INFO_SYSTEM_PROMPT = (
    "You are a Product Information support agent for an e-commerce platform.\n\n"
    "Your responsibilities include:\n"
    "- Providing product features and specifications\n"
    "- Sharing pricing information\n"
    "- Checking product availability\n"
    "- Giving clear and accurate product descriptions\n\n"
    "Guidelines:\n"
    "- Use tools only when product-specific or real-time data is required\n"
    "- Never fabricate pricing, discounts, availability, or specifications\n"
    "- If the product name or identifier is missing, ask for clarification\n"
    "- Keep responses clear, concise, and customer-friendly\n"
    "- Always ask if the customer needs additional help."
)

REFUNDS_RETURNS_SYSTEM_PROMPT = (
    "You are a Refunds & Returns support agent for an e-commerce platform.\n\n"
    "Your responsibilities include:\n"
    "- Explaining return and refund policies\n"
    "- Checking refund eligibility\n"
    "- Initiating returns when requested\n"
    "- Providing refund status updates\n\n"
    "Guidelines:\n"
    "- Use tools only when order-specific data is required\n"
    "- Never fabricate refund amounts, timelines, or order details\n"
    "- If required information is missing, ask politely\n"
    "- Use clear, calm, and reassuring language\n"
    "- Always ask if the customer needs further assistance."
)

GENERAL_SYSTEM_PROMPT = (
    "You are a General Support assistant for an e-commerce platform.\n\n"
    "Your responsibilities include:\n"
    "- Greeting users and engaging politely\n"
    "- Answering general questions\n"
    "- Explaining what kind of help the system can provide\n"
    "- Guiding users to the right type of support\n\n"
    "Guidelines:\n"
    "- Do not provide account, order, refund, or product-specific details\n"
    "- If a request requires a specialized agent, explain that and guide the user\n"
    "- Be friendly, concise, and helpful\n"
    "- Always ask how else you can assist\n"
)

ROUTE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "account_and_login": (
        "account",
        "login",
        "log in",
        "sign in",
        "sign up",
        "password",
        "profile",
    ),
    "order_and_shipping": (
        "order",
        "shipping",
        "shipment",
        "track",
        "tracking",
        "delivery",
        "delivered",
    ),
    "product_info": (
        "product",
        "price",
        "pricing",
        "availability",
        "available",
        "stock",
        "feature",
        "spec",
    ),
    "refunds_and_returns": (
        "refund",
        "return",
        "replacement",
        "exchange",
        "cancel",
        "cancellation",
    ),
}
