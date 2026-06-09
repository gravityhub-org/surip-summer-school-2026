"""Exercise 10 — Posterior on coin bias q

What can we tell about the coin?

    P(q | H_rigged, d) = P(d | H_rigged, q) * P(q | H_rigged) / P(d | H_rigged)

Uniform prior: P(q | H_rigged) = 1 on [0, 1].
With n independent experiments each with T tails in N tosses, the posterior is a Beta distribution:

    P(q | H_rigged, d) ~ Beta(alpha, beta)

Use scipy.stats.beta — find alpha, beta from the data, then plot the posterior.
"""

import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401
from scipy import stats

plt.style.use(["science", "ieee", "bright"])

T_home = 8
N_home = 10
n_experiments_posterior = 7

total_tails = n_experiments_posterior * T_home
total_heads = n_experiments_posterior * (N_home - T_home)

# Uniform prior on q => alpha0 = beta0 = 1
alpha = ...  # YOUR CODE
beta = ...  # YOUR CODE

posterior = stats.beta(a=alpha, b=beta)

q_plot = np.linspace(0, 1, 500)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(q_plot, posterior.pdf(q_plot), lw=2, label="posterior P(q|d)")
ax.axvline(0.5, color="gray", ls="--", label="fair coin")
ax.set_xlabel("coin bias q")
ax.set_ylabel("density")
ax.legend()
plt.tight_layout()
plt.show()

posterior_mean = ...  # YOUR CODE
credible_interval = posterior.interval(0.68)  # ~1-sigma for Beta
print(f"posterior mean q = {posterior_mean}")
print(f"68% credible interval: {credible_interval}")

# YOUR ANSWER — what does the posterior tell you about the coin bias?

