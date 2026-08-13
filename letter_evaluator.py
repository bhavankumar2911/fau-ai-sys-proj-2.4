from pandas import DataFrame, Series
from probability_calculator import group_candidates_by_feedback_for_letter
from entropy_calculator import calculate_expected_entropy_after_letter_guess, calculate_information_gain


def get_available_letters(
    candidates: DataFrame,
    correct_letter_positions: dict[int, str],
    wrong_letters: set[str],
    guesses: list[str]
) -> set[str]:
    all_letters_in_candidates: set[str] = set()
    for word in candidates['city_ascii']:
        all_letters_in_candidates.update(word)

    already_correct_letters = set(correct_letter_positions.values())
    already_guessed_letters = {guess for guess in guesses if len(guess) == 1}

    return all_letters_in_candidates - already_correct_letters - wrong_letters - already_guessed_letters


def evaluate_single_letter(
    letter: str,
    candidates: DataFrame,
    candidate_probabilities: Series,
    current_entropy: float
) -> float:
    feedback_to_words = group_candidates_by_feedback_for_letter(letter, candidates)
    expected_entropy = calculate_expected_entropy_after_letter_guess(feedback_to_words, candidate_probabilities)
    return calculate_information_gain(current_entropy, expected_entropy)


def rank_all_available_letters(
    candidates: DataFrame,
    candidate_probabilities: Series,
    current_entropy: float,
    correct_letter_positions: dict[int, str],
    wrong_letters: set[str],
    guesses: list[str]
) -> list[tuple[str, float]]:
    available_letters = get_available_letters(candidates, correct_letter_positions, wrong_letters, guesses)

    letter_to_information_gain: dict[str, float] = {
        letter: evaluate_single_letter(letter, candidates, candidate_probabilities, current_entropy)
        for letter in available_letters
    }

    return sorted(letter_to_information_gain.items(), key=lambda pair: pair[1], reverse=True)


def get_best_letter(ranked_letters: list[tuple[str, float]]) -> str | None:
    if ranked_letters:
        return ranked_letters[0][0]
    return None