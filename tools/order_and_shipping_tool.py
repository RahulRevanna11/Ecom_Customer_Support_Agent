from langchain.tools import tool
from typing import Optional

@tool
def order_and_shipping_tool(
    intent: str,
    order_id: Optional[str] = None
) -> str:
    """
    Retrieves information regarding customer orders and shipping logistics.
    
    Use this tool when the user asks about:
    1. 'order_status': Current processing state of an order. Requires order_id.
    2. 'track_order': Real-time shipping/tracking location. Requires order_id.
    3. 'delivery_time': General shipping speed estimates (Standard vs Express).
    4. 'shipping_policy': Information about shipping costs and free delivery thresholds.

    Args:
        intent: The specific type of shipping or order query being made.
        order_id: The unique order identifier (e.g., 'ORD123'). Required for status and tracking.
    """

    # ---- Order status ----
    if intent == "order_status":
        if not order_id:
            return "Please provide your order ID to check the order status."

        return (
            f"Order {order_id} is currently being processed and "
            "is expected to ship within 24 hours."
        )

    # ---- Tracking ----
    if intent == "track_order":
        if not order_id:
            return "Please provide your order ID to track your shipment."

        return (
            f"Order {order_id} is in transit. "
            "Estimated delivery is 3–5 business days."
        )

    # ---- Delivery timeline ----
    if intent == "delivery_time":
        return (
            "Standard delivery takes 3–5 business days. "
            "Express delivery takes 1–2 business days."
        )

    # ---- Shipping policy ----
    if intent == "shipping_policy":
        return (
            "We offer standard and express shipping. "
            "Shipping is free on orders above $50."
        )

    return (
        "I can help with order status, tracking, delivery timelines, "
        "and shipping policies."
    )
