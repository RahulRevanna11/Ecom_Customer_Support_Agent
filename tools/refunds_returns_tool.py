from langchain.tools import tool
from typing import Optional


@tool
def refunds_returns_tool(
    order_id: Optional[str] = None,
    request_type: str = "policy"
) -> str:
    """
    Handle customer inquiries related to refunds and returns.

    This tool provides information about return policies, refund eligibility,
    return status, and basic return instructions.

    Parameters:
        order_id (str, optional):
            Order identifier related to the return or refund.
            Example: "ORD123456"

        request_type (str):
            Type of request. Supported values:
            - "policy": General return and refund policy
            - "status": Status of a return or refund
            - "initiate": Instructions to start a return or refund

    Returns:
        str:
            A user-friendly message addressing the refund or return inquiry.

    Notes:
        - This is a simulated implementation.
        - In production, this would connect to order and payment services.
    """

    if request_type == "policy":
        return (
            "You can return most items within 30 days of delivery. "
            "Refunds are processed back to the original payment method "
            "within 5–7 business days after the return is received."
        )

    if request_type == "status":
        if not order_id:
            return "Please provide your order ID to check the return or refund status."
        return (
            f"The refund for order {order_id} is currently being processed. "
            "You will be notified once it is completed."
        )

    if request_type == "initiate":
        if not order_id:
            return "Please provide your order ID to start a return or refund."
        return (
            f"You can initiate a return for order {order_id} by visiting "
            "the 'My Orders' section and selecting 'Request Return'."
        )

    return "I'm not sure how to help with that return or refund request."
