def parse_correct_letter_positions_from_feedback(feedback: str) -> dict[int, str]:
    correct_letter_positions: dict[int, str] = {}
    if not feedback or any(character != '-' and not character.isupper() for character in feedback):
        return correct_letter_positions

    for position, character in enumerate(feedback):
        if character != '-':
            correct_letter_positions[position] = character
    return correct_letter_positions


def update_correct_letter_positions(existing_positions: dict[int, str], feedback: str) -> dict[int, str]:
    new_positions = parse_correct_letter_positions_from_feedback(feedback)
    existing_positions.update(new_positions)
    return existing_positions


def update_wrong_letters(existing_wrong_letters: set[str], last_guess: str, last_feedback: str) -> set[str]:
    if len(last_guess) == 1 and last_feedback == "doesn't occur":
        existing_wrong_letters.add(last_guess)
    return existing_wrong_letters


def update_eliminated_words(existing_eliminated_words: set[str], last_guess: str, last_feedback: str) -> set[str]:
    if len(last_guess) > 1 and last_feedback == 'wrong word':
        existing_eliminated_words.add(last_guess)
    return existing_eliminated_words
