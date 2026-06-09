"""Exercise 3 — Bayes factor

    B^r_f = P(T | H_rigged, N) / P(T | H_fair, N)

Evidence under the rigged hypothesis (marginalising over q):

    P(T | H_rigged, N) = integral_0^1 P(T | H_rigged, q, N) * P(q | H_rigged) dq

Total ignorance for q: P(q | H_rigged) = 1 on [0, 1].

Use scipy.integrate.quad, then compute B^r_f.
"""

from scipy import integrate, stats

N = 10
T = 8


def likelihood_fair(T: int, N: int) -> float:
    return stats.binom.pmf(T, N, 0.5)


def likelihood_rigged(T: int, N: int, q: float) -> float:
    return stats.binom.pmf(T, N, q)


def integrand(q: float) -> float:
    return likelihood_rigged(T, N, q)  # uniform prior: P(q|H_rigged) = 1


p_data_given_rigged, _ = integrate.quad(integrand, 0, 1)
print(f"P(T={T} | H_rigged, N={N}) = {p_data_given_rigged}")

# Analytic result for uniform prior: P(T|H_rigged,N) = 1/(N+1)
# Verify with scipy — does your integral match 1/(N+1)?
analytic_rigged = ...  # YOUR CODE

bayes_factor_single = ...  # YOUR CODE: B^r_f for one experiment
print(f"B^r_f (one experiment) = {bayes_factor_single}")

