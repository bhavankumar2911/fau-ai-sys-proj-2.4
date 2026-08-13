import math
from pandas import Series


def calculate_entropy(probabilities: list[float]) -> float:
    entropy = 0.0
    for probability in probabilities:
        if 0 < probability < 1:
            entropy -= probability * math.log2(probability)
    return entropy


def calculate_entropy_for_feedback_partition(
    words_in_partition: list[str],
    candidate_probabilities: Series,
    partition_probability: float
) -> float:
    if not words_in_partition or partition_probability == 0:
        return 0.0
    normalized_probabilities = [
        candidate_probabilities[word] / partition_probability
        for word in words_in_partition
        if word in candidate_probabilities.index
    ]
    return calculate_entropy(normalized_probabilities)


def calculate_expected_entropy_after_letter_guess(
    feedback_to_words: dict[str, list[str]],
    candidate_probabilities: Series
) -> float:
    expected_entropy = 0.0
    for feedback, words_in_partition in feedback_to_words.items():
        partition_probability = sum(
            candidate_probabilities[word]
            for word in words_in_partition
            if word in candidate_probabilities.index
        )
        if partition_probability == 0:
            continue
        partition_entropy = calculate_entropy_for_feedback_partition(
            words_in_partition, candidate_probabilities, partition_probability
        )
        expected_entropy += partition_probability * partition_entropy
    return expected_entropy


def calculate_information_gain(current_entropy: float, expected_entropy_after_guess: float) -> float:
    return current_entropy - expected_entropy_after_guess