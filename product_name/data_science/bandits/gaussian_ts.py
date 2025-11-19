import numpy as np
from math import sqrt

def sample_bandit(mean: float, variance: float) -> float:
    """Draw one sample from posterior N(mean, variance)."""
    return np.random.normal(mean, sqrt(variance))


def update_bandit_params(bandit, reward: float):
    """
    Update mean and variance incrementally.
    """
    n = bandit.trial + 1

    old_mean = bandit.mean
    new_mean = old_mean + (reward - old_mean) / n

    old_variance = bandit.variance
    new_variance = (
        ((n - 1) * old_variance)
        + (reward - old_mean) * (reward - new_mean)
    ) / n

    bandit.mean = new_mean
    bandit.variance = new_variance
    bandit.trial = n

    return bandit
