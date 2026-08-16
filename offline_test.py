import sys

from word_guessing_agent import WordGuessingAgent


def get_feedback(action: str, target: str) -> str:
    if len(action) > 1:
        return "correct word" if action == target else "wrong word"

    if action not in target:
        return "doesn't occur"

    return "".join(character if character == action else "-" for character in target)


def run_game(target: str, maximum_actions: int = 50) -> None:
    agent = WordGuessingAgent("offline-test", {})
    guesses: list[str] = []
    feedback = ""

    for action_number in range(1, maximum_actions + 1):
        action = agent.get_action({"feedback": feedback, "guesses": guesses}, None)
        guesses.append(action)
        feedback = get_feedback(action, target)
        print(f"{action_number}: {action} -> {feedback}")

        if feedback == "correct word":
            print(f"Solved {target} in {action_number} actions.")
            return

    raise RuntimeError(f"The agent did not solve {target} in {maximum_actions} actions.")


if __name__ == "__main__":
    target_city = sys.argv[1].upper() if len(sys.argv) > 1 else "TOKYO"
    run_game(target_city)
