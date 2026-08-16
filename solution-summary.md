# Solution Summary

The agent treats the game as a repeated process of reducing uncertainty about the hidden city. It uses the population of each city as prior knowledge and selects letters according to their expected information gain. The following steps describe the decision process used for every turn.

## Step 1: Prepare the candidate words

Before a game, the city data is cleaned to match the assignment constraints. Only cities with a population of at least 100,000 are retained. Names containing spaces, hyphens, or diacritics are removed, the remaining names are converted to upper case, and duplicate names are discarded. These cities form the initial candidate list.

## Step 2: Read and store the feedback

For each turn, the agent receives the most recent feedback and the complete list of previous guesses. It stores three types of information:

- revealed letter positions from feedback such as `-O-ON--`;
- letters that received `doesn't occur`;
- full-city guesses that received `wrong word`.

Status messages are not interpreted as positional feedback. A rejected city only means that this one city is impossible; it provides no information about individual letters.

## Step 3: Filter impossible candidates

The agent starts with the full cleaned list and removes every city that conflicts with the information collected so far. A remaining candidate must contain every revealed letter at its revealed position, must not contain an absent letter, and must not equal a rejected full-city guess.

If exactly one candidate remains, the agent immediately guesses that city. Otherwise, it uses the remaining candidates to choose the next action.

## Step 4: Calculate the probability of each candidate

The assignment chooses cities with probability proportional to their population. Therefore, for every remaining candidate, the agent calculates:

$$
P(\text{candidate city}) =
\frac{\text{population of candidate city}}
{\sum \text{population of all remaining candidates}}
$$

This is the key prior used throughout the decision process. A large city is more likely than a small city even when both are consistent with the feedback.

## Step 5: Measure the current uncertainty

The agent calculates the entropy of the current candidate probabilities:

$$
H(\text{remaining candidates}) =
-\sum P(\text{candidate city})\log_2 P(\text{candidate city})
$$

This answers: “How uncertain is the agent about the hidden city before making the next guess?”

## Step 6: Evaluate each available letter

For every letter that has not already been guessed, the agent imagines every possible feedback result.

For example, when considering a letter, each candidate city produces either `doesn't occur` or a particular pattern of revealed positions. The agent groups together all cities that would produce the same feedback. Each group represents one possible outcome of guessing that letter.

For every group, the agent:

1. adds the probabilities of its cities to obtain the probability of that feedback;
2. normalizes the probabilities inside the group;
3. calculates the entropy that would remain after receiving that feedback.

The weighted average of these possible remaining entropies is the expected uncertainty after guessing the letter:

$$
E[\text{remaining uncertainty} \mid \text{letter guess}] =
\sum P(\text{possible feedback})
H(\text{candidates after that feedback})
$$

The information gain of the letter is then:

$$
IG(\text{letter guess}) =
H(\text{remaining candidates}) -
E[\text{remaining uncertainty} \mid \text{letter guess}]
$$

The agent ranks all available letters and keeps the letter with the largest information gain. This is more informative than choosing only the most frequent letter because it accounts for the exact feedback pattern that the letter can reveal.

## Step 7: Decide between a letter and a full-city guess

The agent also identifies the most probable remaining city. A full-city guess is selected when it is the only candidate, when its probability is above 70%, or when it is above 50% during the first three actions. Otherwise, the agent chooses the highest-ranked letter from Step 6.

These thresholds are a heuristic for balancing information gathering against the chance of ending the game immediately. If a full-city guess is wrong, the next turn removes it from the candidate list and repeats the same process.

## Step 8: Repeat until the city is found

Each new feedback message updates the stored knowledge, changes the candidate set, changes the probability distribution, and therefore may change the best action. The loop continues until the agent submits the correct city.

The implementation and local test runner use the standard feedback model: a successful letter guess reveals all occurrences of that letter and the feedback length matches the target word length. Server competition remains necessary to measure the official average number of guesses over 1,000 games.
