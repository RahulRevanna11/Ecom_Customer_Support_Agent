from typing import Optional

from langchain.tools import tool


@tool
def order_and_shipping_tool(intent: str, order_id: Optional[str] = None) -> str:
    """
    Retrieve customer order and shipping information.

    Supported intents:
    - order_status: Current processing state of an order. Requires order_id.
    - track_order: Real-time shipping or tracking location. Requires order_id.
    - delivery_time: General shipping speed estimates.
    - shipping_policy: Shipping costs and free delivery thresholds.
    """

    normalized_intent = intent.lower().strip()

    if normalized_intent == "order_status":
        if not order_id:
            return "Please provide your order ID to check the order status."

        return (
            f"Order {order_id} is currently being processed and "
            "is expected to ship within 24 hours."
        )

    if normalized_intent == "track_order":
        if not order_id:
            return "Please provide your order ID to track your shipment."

        return f"Order {order_id} is in transit. Estimated delivery is 3-5 business days."

    if normalized_intent == "delivery_time":
        return (
            "Standard delivery takes 3-5 business days. "
            "Express delivery takes 1-2 business days."
        )

    if normalized_intent == "shipping_policy":
        return (
            "We offer standard and express shipping. "
            "Shipping is free on orders above $50."
        )

    return (
        "I can help with order status, tracking, delivery timelines, "
        "and shipping policies."
    )
