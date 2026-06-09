# Info

- Instructor: Otto
- Pre-requirements: [uv](https://docs.astral.sh/uv/), git

## Setup

```bash
cd bayesian_tutorial
uv sync
uv run jupyter notebook macau_coin.ipynb
```

## Exercises (script alternative)

Same exercises as the notebook, as standalone scripts in `exercises/`:

```bash
uv run python exercises/01_binomial.py
uv run python exercises/03_bayes_factor.py
# ... etc.
```

# Syllabus

By the end of the tutorial, the students will be able to:
- Compute a Bayes factor to determine whether a coin used in a casino @ Macau is biased or not
- Compute the coin bias posterior distribution
- Apply Bayesian analysis to a real-world problem: Microlensing gravitational-wave detection

# Syllabus table

| Time | Topic | Type |
| --- | --- | --- |
| 10min | Macau story | Slide |
| 20min | Compute coin toss probability (Binomial) | Hands-on |
| 10min | Introduce "fair" and "rigged" hypothesis | Slide |
| 20min | Compute Bayes factor | Hands-on |
| 10min | Evaluate results: Is there enough evidence | Hands-on |
| 15min | Break | - |
| 20min | Evaluate posterior odds | Hands-on |
| 10min | Plot the coin bias posterior | Hands-on |
| 10min | Introduce lensing detection problem | Slide |
| 20min | Free time | - |
| 5min | Wrap up | Slide |
