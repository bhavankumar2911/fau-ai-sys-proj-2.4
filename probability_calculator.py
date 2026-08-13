import pandas
from pandas import DataFrame, Series


def calculate_all_candidate_probabilities(candidates: DataFrame) -> Series:
    total_population = candidates['population'].sum()
    word_to_probability: dict[str, float] = {}
    for row_index, row in candidates.iterrows():
        word_to_probability[row['city_ascii']] = row['population'] / total_population
    return pandas.Series(word_to_probability)


def simulate_feedback_if_letter_guessed(letter: str, word: str) -> str:
    if letter in word:
        revealed_positions = list('-' * len(word))
        for position, character in enumerate(word):
            if character == letter:
                revealed_positions[position] = letter
        return ''.join(revealed_positions)
    return "doesn't occur"


def group_candidates_by_feedback_for_letter(letter: str, candidates: DataFrame) -> dict[str, list[str]]:
    feedback_to_words: dict[str, list[str]] = {}
    for word in candidates['city_ascii']:
        feedback = simulate_feedback_if_letter_guessed(letter, word)
        feedback_to_words.setdefault(feedback, []).append(word)
    return feedback_to_words


def calculate_feedback_probability(words_producing_feedback: list[str], candidate_probabilities: Series) -> float:
    return sum(
        candidate_probabilities[word]
        for word in words_producing_feedback
        if word in candidate_probabilities.index
    )


def calculate_conditional_probability(candidate_probability: float, feedback_probability: float) -> float:
    if feedback_probability == 0:
        return 0
    return candidate_probability / feedback_probability