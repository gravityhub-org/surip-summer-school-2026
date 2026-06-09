"""Exercise 2 — Competing hypotheses

H_fair:  the coin is fair
H_rigged: the coin is rigged

    P(T | H_fair, N)  = binom(N, T) * 0.5^T * 0.5^(N-T)
    P(T | H_rigged, q, N) = binom(N, T) * q^T * (1-q)^(N-T)

T is the number of tails; q is the tail probability under H_rigged.

Under which hypothesis is the data more likely?
Uniform prior on q: P(q | H_rigged) = 1 on [0, 1].
"""

import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401
from scipy import stats

plt.style.use(["science", "ieee", "bright"])

N = 10
T = 8


def likelihood_fair(T: int, N: int) -> float:
    """P(T | H_fair, N)"""
    return stats.binom.pmf(T, N, 0.5)


def likelihood_rigged(T: int, N: int, q) -> float:
    """P(T | H_rigged, q, N)"""
    return stats.binom.pmf(T, N, q)


p_data_given_fair = likelihood_fair(T, N)
print(f"P(T={T} | H_fair, N={N}) = {p_data_given_fair}")

q_grid = np.linspace(0, 1, 500)
p_data_vs_q = likelihood_rigged(T, N, q_grid)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(q_grid, p_data_vs_q, lw=2)
ax.axvline(0.5, color="gray", ls="--", label="fair coin (q=0.5)")
ax.set_xlabel("coin bias q")
ax.set_ylabel(f"P(T={T} | H_rigged, q, N={N})")
ax.legend()
plt.tight_layout()
plt.show()

# YOUR ANSWER — which hypothesis is the data more likely under?

