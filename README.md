# Guess the Word Agent

This project implements a Python agent for Assignment 2.4, *Guess the Word*. The agent uses the supplied World Cities dataset to maintain a set of possible target cities and chooses actions using population-weighted probabilities and expected information gain.

## Requirements

- Python 3.10 or newer
- The packages in `requirements.txt`
- The assignment repository next to this directory, containing `client.py` and `worldcities.csv`
- A server configuration JSON file when running against the assignment server

Create a virtual environment and install the dependencies:

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

## Preparing the city list

Run the following command once from this directory:

```bash
venv/bin/python clean_data.py
```

It creates `valid_cities.csv` from `../assignment/worldcities.csv`. The preprocessing keeps cities with a population of at least 100,000 and removes names containing spaces, hyphens, or diacritics. The file is generated locally and is intentionally not tracked in Git.

## Running the agent

To run the agent against the assignment server, provide the path to the configuration JSON supplied for the target environment:

```bash
venv/bin/python main.py path/to/config.json
```

The provided client handles the HTTP protocol. `main.py` starts up to 1,000 sequential runs.

## Offline test

An offline runner is available for testing without the server:

```bash
venv/bin/python offline_test.py TOKYO
```

Replace `TOKYO` with any city in `valid_cities.csv`. The runner uses the real agent and simulates the standard feedback protocol: revealed letter positions, `doesn't occur`, `wrong word`, and `correct word`.

## Repository structure

- `main.py`: server entry point.
- `word_guessing_agent.py`: stateful agent and action loop.
- `candidate_word_manager.py`: candidate filtering.
- `probability_calculator.py`, `entropy_calculator.py`, `letter_evaluator.py`: probabilistic scoring and information-gain calculation.
- `action_selector.py`: choice between a letter and a city guess.
- `feedback_parser.py`: interpretation of server feedback.
- `clean_data.py`: generation and loading of the city candidate list.
- `offline_test.py`: local standard-rules game runner.
- `solution-summary.md`: explanation of the solution design.
