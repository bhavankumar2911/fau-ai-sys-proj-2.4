from pandas import DataFrame
from clean_data import load_cleaned_cities_dataframe


def load_all_valid_cities() -> DataFrame:
    return load_cleaned_cities_dataframe()


def word_matches_correct_letter_positions(word: str, correct_letter_positions: dict[int, str]) -> bool:
    for position, letter in correct_letter_positions.items():
        if word[position] != letter:
            return False
    return True


def filter_candidates_by_correct_letter_positions(
    candidates: DataFrame,
    correct_letter_positions: dict[int, str]
) -> DataFrame:
    if not correct_letter_positions:
        return candidates
    return candidates[
        candidates['city_ascii'].apply(
            lambda word: word_matches_correct_letter_positions(word, correct_letter_positions)
        )
    ]


def word_contains_any_of_the_letters(word: str, letters: set[str]) -> bool:
    return any(letter in word for letter in letters)


def filter_candidates_by_wrong_letters(candidates: DataFrame, wrong_letters: set[str]) -> DataFrame:
    if not wrong_letters:
        return candidates
    return candidates[
        ~candidates['city_ascii'].apply(
            lambda word: word_contains_any_of_the_letters(word, wrong_letters)
        )
    ]


def filter_candidates_by_eliminated_words(candidates: DataFrame, eliminated_words: set[str]) -> DataFrame:
    if not eliminated_words:
        return candidates
    return candidates[~candidates['city_ascii'].isin(eliminated_words)]


def filter_all_candidates(
    candidates: DataFrame,
    correct_letter_positions: dict[int, str],
    wrong_letters: set[str],
    eliminated_words: set[str]
) -> DataFrame:
    candidates = filter_candidates_by_correct_letter_positions(candidates, correct_letter_positions)
    candidates = filter_candidates_by_wrong_letters(candidates, wrong_letters)
    candidates = filter_candidates_by_eliminated_words(candidates, eliminated_words)
    return candidates