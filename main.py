from dotenv import load_dotenv

load_dotenv()

from graph.workflow import app
from state import build_initial_state


EXIT_COMMANDS = {"exit", "quit", "q"}


def run_chat() -> None:
    """Run the customer support agent from the terminal."""

    history: list[str] = []

    print("Customer Support Agent")
    print("Type 'exit' to stop.\n")

    while True:
        query = input("USER: ").strip()
        if query.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            break

        if not query:
            print("AI: Please enter a question so I can help.\n")
            continue

        result = app.invoke(build_initial_state(query, history))
        history = result.get("history", history)
        print(f"AI: {result.get('response', '')}\n")


if __name__ == "__main__":
    run_chat()
