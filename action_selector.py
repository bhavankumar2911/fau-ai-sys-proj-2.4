from pandas import DataFrame, Series


def get_most_probable_candidate(candidate_probabilities: Series) -> tuple[str | None, float]:
    best_word: str | None = None
    best_probability = 0.0
    for word, probability in candidate_probabilities.items():
        if probability > best_probability:
            best_probability = probability
            best_word = word
    return best_word, best_probability


def should_guess_word(word_probability: float, guess_count: int, total_candidates: int) -> bool:
    if total_candidates == 1:
        return True
    if word_probability > 0.7:
        return True
    if guess_count < 3 and word_probability > 0.5:
        return True
    return False


def select_action(
    candidates: DataFrame,
    candidate_probabilities: Series,
    ranked_letters: list[tuple[str, float]],
    guess_count: int
) -> str:
    if len(candidates) == 1:
        return candidates.iloc[0]['city_ascii']

    most_probable_word, word_probability = get_most_probable_candidate(candidate_probabilities)

    if should_guess_word(word_probability, guess_count, len(candidates)):
        return most_probable_word

    return ranked_letters[0][0]