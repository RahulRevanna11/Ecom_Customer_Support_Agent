from langchain.tools import tool


@tool
def account_login_tool(query: str) -> str:
    """
    Provide automated help for common account and login-related queries.

    Args:
        query: Natural-language question about login, registration, password
            reset, or profile updates.

    Returns:
        A helpful instructional message based on the detected intent.
    """

    normalized_query = query.lower()

    if "forgot" in normalized_query or "reset" in normalized_query:
        return (
            "To reset your password:\n"
            "1. Go to the login page\n"
            "2. Click 'Forgot Password'\n"
            "3. Enter your registered email\n"
            "4. Follow the link sent to your email"
        )

    if (
        "create" in normalized_query
        or "sign up" in normalized_query
        or "register" in normalized_query
    ):
        return (
            "To create an account:\n"
            "1. Click 'Sign Up'\n"
            "2. Enter your email and password\n"
            "3. Verify your email\n"
            "4. Log in to start using the service"
        )

    if "change" in normalized_query or "update" in normalized_query:
        return "You can update your account details from the Profile section after logging in."

    return (
        "For account-related help, you can reset your password, "
        "create a new account, or update your profile."
    )
