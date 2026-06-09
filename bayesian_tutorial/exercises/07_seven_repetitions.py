"""Exercise 7 — Seven repetitions

You repeat the experiment 7 times (each: 8 tails in 10 tosses).

A rigged coin is ~150x more likely to generate the data than a fair coin.

1. Is the coin rigged?
2. It's still probably not rigged. Why?
   (Think about prior odds and context — see news story in slides.)
"""

from scipy import integrate, stats

T_repeat = 8
N_repeat = 10
n_seven = 7

p_one_fair = stats.binom.pmf(T_repeat, N_repeat, 0.5)
p_one_rigged, _ = integrate.quad(
    lambda q: stats.binom.pmf(T_repeat, N_repeat, q), 0, 1
)
bf_one = p_one_rigged / p_one_fair

bf_seven = bf_one**n_seven
print(f"Bayes factor after {n_seven} experiments: {bf_seven}")

# YOUR ANSWERS:
