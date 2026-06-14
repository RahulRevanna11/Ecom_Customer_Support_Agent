from typing import Optional

from langchain.tools import tool


@tool
def product_info_tool(
    product_name: Optional[str] = None,
    info_type: str = "overview",
) -> str:
    """
    Retrieve basic product information for customer inquiries.

    Supported info_type values are overview, price, availability, and features.
    This implementation simulates product data; production code should fetch
    from a catalog service or database.
    """

    if not product_name:
        return "Please provide the product name so I can share the relevant details."

    normalized_info_type = info_type.lower().strip()

    if normalized_info_type == "price":
        return f"The price of {product_name} is $49.99."

    if normalized_info_type == "availability":
        return f"{product_name} is currently in stock and available for order."

    if normalized_info_type == "features":
        return (
            f"{product_name} offers a durable design, easy setup, "
            "and comes with a 1-year warranty."
        )

    return (
        f"{product_name} is a reliable and popular product designed "
        "to meet everyday customer needs."
    )
