"""Exercise 5 — Repeating the experiment

You repeat the experiment 7 times. Each experiment gives 8 tails in 10 tosses.

Is the coin rigged?
"""

from scipy import integrate, stats

n_experiments = 7
T_repeat = 8  # tails per experiment
N_repeat = 10

p_one_fair = stats.binom.pmf(T_repeat, N_repeat, 0.5)

p_one_rigged, _ = integrate.quad(
    lambda q: stats.binom.pmf(T_repeat, N_repeat, q), 0, 1
)

bf_one = p_one_rigged / p_one_fair
print(f"Bayes factor for one experiment (8 tails / 10): {bf_one}")

# Independent datasets: multiply marginal likelihoods
bf_seven = ...  # YOUR CODE
print(f"Bayes factor for {n_experiments} experiments: {bf_seven}")

# YOUR ANSWER — is the coin rigged?

