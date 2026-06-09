"""Exercise 1 — Binomial probability

Suppose:
- The probability that a coin returns tail is p = 0.5
- We toss the coin N = 10 times and get T = 8 tails

What is the probability of getting 8 tails in 10 tosses?

    P(T | p, N) = binom(N, T) * p^T * (1-p)^(N-T)

scipy.stats.binom implements this distribution.

More likely to be rigged?  (answer after computing the probability)
"""

from scipy import stats

N = 10  # number of tosses
T = 8  # number of tails
p_fair = 0.5

# scipy.stats.binom.pmf(k, n, p) -> P(X = k) for X ~ Binomial(n, p)
binom = stats.binom(n=N, p=p_fair)

# Compute P(T = 8) and express as a fraction if possible
p_eight_tails = ...  # YOUR CODE
print(f"P(T={T} | p={p_fair}, N={N}) = {p_eight_tails}")

# YOUR ANSWER — more likely to be rigged?

