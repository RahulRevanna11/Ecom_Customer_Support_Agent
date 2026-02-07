from langchain.tools import tool
@tool
def account_login_tool(query: str) -> str:
    """
    Provides automated help responses for common account and login-related queries.

    The function analyzes a user’s query to determine whether they need help with
    password recovery, account creation, or updating account details, and returns
    step-by-step guidance accordingly.

    Args:
        query (str): A user’s natural-language question or request related to
            account login, registration, password reset, or profile updates.

    Returns:
        str: A helpful instructional message based on the detected intent in
        the query. If no specific intent is detected, a general account-help
        message is returned.
    """
    query = query.lower()

    if "forgot" in query or "reset" in query:
        return (
            "To reset your password:\n"
            "1. Go to the login page\n"
            "2. Click 'Forgot Password'\n"
            "3. Enter your registered email\n"
            "4. Follow the link sent to your email"
        )

    if "create" in query or "sign up" in query or "register" in query:
        return (
            "To create an account:\n"
            "1. Click 'Sign Up'\n"
            "2. Enter your email and password\n"
            "3. Verify your email\n"
            "4. Login to start using the service"
        )

    if "change" in query or "update" in query:
        return (
            "You can update your account details from the Profile section "
            "after logging in."
        )

    return (
        "For account-related help, you can reset your password, "
        "create a new account, or update your profile."
    )
