import sys
import logging
from word_guessing_agent import WordGuessingAgent

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    WordGuessingAgent.run(
        agent_config_file=sys.argv[1],
        parallel_runs=False,
        multiprocessing=False,
        run_limit=1000
    )