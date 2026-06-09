"""Exercise 6 — Many independent datasets

You have 10 independent datasets d. Each gives 8 tails in 10 tosses.

    P(d | H_rigged, N) = prod_i P(d_i | H_rigged, N)
    P(d | H_fair, N)   = prod_i P(d_i | H_fair, N)

Is the coin rigged now?
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate, stats

T_repeat = 8
N_repeat = 10
n_datasets = 10

p_one_fair = stats.binom.pmf(T_repeat, N_repeat, 0.5)
p_one_rigged, _ = integrate.quad(
    lambda q: stats.binom.pmf(T_repeat, N_repeat, q), 0, 1
)
bf_one = p_one_rigged / p_one_fair

bf_ten = bf_one**n_datasets
print(f"Bayes factor for {n_datasets} identical datasets: {bf_ten}")

n_range = np.arange(1, 11)
bf_growth = bf_one**n_range

fig, ax = plt.subplots(figsize=(7, 4))
ax.semilogy(n_range, bf_growth, "o-", lw=2)
ax.set_xlabel("number of independent experiments")
ax.set_ylabel("B^r_f")
ax.set_title("Bayes factor vs. repeated identical data")
plt.tight_layout()
plt.show()

# YOUR ANSWER — is the coin rigged now?

