from typing import Optional

from langchain.tools import tool


@tool
def refunds_returns_tool(
    order_id: Optional[str] = None,
    request_type: str = "policy",
) -> str:
    """
    Handle customer inquiries related to refunds and returns.

    Supported request_type values are policy, status, and initiate.
    This implementation simulates return data; production code should connect
    to order and payment services.
    """

    normalized_request_type = request_type.lower().strip()

    if normalized_request_type == "policy":
        return (
            "You can return most items within 30 days of delivery. "
            "Refunds are processed back to the original payment method "
            "within 5-7 business days after the return is received."
        )

    if normalized_request_type == "status":
        if not order_id:
            return "Please provide your order ID to check the return or refund status."
        return (
            f"The refund for order {order_id} is currently being processed. "
            "You will be notified once it is completed."
        )

    if normalized_request_type == "initiate":
        if not order_id:
            return "Please provide your order ID to start a return or refund."
        return (
            f"You can initiate a return for order {order_id} by visiting "
            "the 'My Orders' section and selecting 'Request Return'."
        )

    return "I'm not sure how to help with that return or refund request."
