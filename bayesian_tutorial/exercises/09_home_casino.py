"""Exercise 9 — Home casino

- ~50% of friends say the casino cheats
- Prior odds rigged : fair = 1 : 1
- Same data: 8 tails in 10 tosses, repeated 7 times

Is the coin rigged now?
"""

from scipy import integrate, stats

T_home = 8
N_home = 10
n_experiments = 7

p_one_fair_tails = stats.binom.pmf(T_home, N_home, 0.5)
p_one_rigged_tails, _ = integrate.quad(
    lambda q: stats.binom.pmf(T_home, N_home, q), 0, 1
)
bf_one_tails = p_one_rigged_tails / p_one_fair_tails
bf_seven_tails = bf_one_tails**n_experiments

prior_odds_home = ...  # YOUR CODE
posterior_odds_home = ...  # YOUR CODE
print(f"posterior odds O^r_f = {posterior_odds_home}")

# YOUR ANSWER — is the coin rigged now?

