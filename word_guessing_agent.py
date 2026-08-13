from typing import Any
from client import Agent, AgentConfig, RequestInfo
from candidate_word_manager import load_all_valid_cities, filter_all_candidates
from feedback_parser import update_correct_letter_positions, update_wrong_letters, update_eliminated_words
from probability_calculator import calculate_all_candidate_probabilities
from entropy_calculator import calculate_entropy
from letter_evaluator import rank_all_available_letters
from action_selector import select_action, get_most_probable_candidate


class WordGuessingAgent(Agent):
    def __init__(self, run_id: str, agent_config: AgentConfig) -> None:
        super().__init__(run_id, agent_config)
        self.all_candidates = load_all_valid_cities()
        self.current_candidates = self.all_candidates
        self.correct_letter_positions: dict[int, str] = {}
        self.wrong_letters: set[str] = set()
        self.eliminated_words: set[str] = set()
        self.guess_count = 0

    def get_action(self, percept: dict[str, Any], request_info: RequestInfo) -> str:
        feedback: str = percept['feedback']
        guesses: list[str] = percept['guesses']

        self.correct_letter_positions = update_correct_letter_positions(self.correct_letter_positions, feedback)

        if guesses:
            last_guess = guesses[-1]
            self.wrong_letters = update_wrong_letters(self.wrong_letters, last_guess, feedback)
            self.eliminated_words = update_eliminated_words(self.eliminated_words, last_guess, feedback)

        self.current_candidates = filter_all_candidates(
            self.all_candidates,
            self.correct_letter_positions,
            self.wrong_letters,
            self.eliminated_words
        )

        if len(self.current_candidates) == 1:
            action = self.current_candidates.iloc[0]['city_ascii']
            self.guess_count += 1
            return action

        candidate_probabilities = calculate_all_candidate_probabilities(self.current_candidates)
        current_entropy = calculate_entropy(list(candidate_probabilities.values))

        ranked_letters = rank_all_available_letters(
            self.current_candidates,
            candidate_probabilities,
            current_entropy,
            self.correct_letter_positions,
            self.wrong_letters,
            guesses
        )

        if not ranked_letters:
            action, _ = get_most_probable_candidate(candidate_probabilities)
            self.guess_count += 1
            return action

        action = select_action(self.current_candidates, candidate_probabilities, ranked_letters, self.guess_count)
        self.guess_count += 1
        return action