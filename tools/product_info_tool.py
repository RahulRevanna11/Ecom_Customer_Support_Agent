from langchain.tools import tool
from typing import Optional


@tool
def product_info_tool(
    product_name: Optional[str] = None,
    info_type: str = "overview"
) -> str:
    """
    Retrieve basic product information for customer inquiries.

    This tool is used by the Product Information agent to answer questions
    related to product details such as pricing, availability, features,
    and general descriptions.

    Parameters:
        product_name (str, optional):
            Name of the product the user is asking about.
            Example: "Smart Fitness Band"

        info_type (str):
            Type of information requested. Supported values:
            - "overview": General description of the product
            - "price": Product pricing information
            - "availability": Stock and availability status
            - "features": Key features and highlights

    Returns:
        str:
            A human-readable response containing the requested product
            information or a clarification message if required data is missing.

    Notes:
        - This implementation simulates real product data.
        - In a production environment, this function would fetch data from
          a product catalog service or database.
    """

    if not product_name:
        return (
            "Please provide the product name so I can share the "
            "relevant details."
        )

    if info_type == "price":
        return f"The price of {product_name} is $49.99."

    if info_type == "availability":
        return f"{product_name} is currently in stock and available for order."

    if info_type == "features":
        return (
            f"{product_name} offers a durable design, easy setup, "
            "and comes with a 1-year warranty."
        )

    # Default: overview
    return (
        f"{product_name} is a reliable and popular product designed "
        "to meet everyday customer needs."
    )
