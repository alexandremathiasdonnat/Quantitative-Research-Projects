# src/payoffs.py
import numpy as np


def call_payoff_log(x: np.ndarray, K: float) -> np.ndarray:
    """
    Payoff (S_T - K)+ in log-space, x = ln S.

    S = exp(x)
    """
    S = np.exp(x)
    return np.maximum(S - K, 0.0)


def put_payoff_log(x: np.ndarray, K: float) -> np.ndarray:
    """
    Payoff (K - S_T)+ in log-space, x = ln S.
    """
    S = np.exp(x)
    return np.maximum(K - S, 0.0)
