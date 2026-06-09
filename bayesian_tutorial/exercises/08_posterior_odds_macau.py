"""Exercise 8 — Posterior odds (Macau casino)

    O^r_f = P(H_rigged | d, I) / P(H_fair | d, I)
          = B^r_f * P(H_rigged | I) / P(H_fair | I)

Macau context:
- Only < 1 in 10,000 casinos are rigged
- Prior odds rigged : fair = 1 : 10,000

Conclusion: is the coin rigged in Macau?
"""

from scipy import integrate, stats

T_repeat = 8
N_repeat = 10
n_eight = 8

p_one_fair = stats.binom.pmf(T_repeat, N_repeat, 0.5)
p_one_rigged, _ = integrate.quad(
    lambda q: stats.binom.pmf(T_repeat, N_repeat, q), 0, 1
)
bf_one = p_one_rigged / p_one_fair
bf_eight = bf_one**n_eight

prior_odds_macau = ...  # YOUR CODE: P(H_rigged|I) / P(H_fair|I)

posterior_odds_macau = ...  # YOUR CODE: bf_eight * prior_odds_macau
print(f"posterior odds O^r_f = {posterior_odds_macau}")

# YOUR ANSWER — is the coin rigged in Macau?

