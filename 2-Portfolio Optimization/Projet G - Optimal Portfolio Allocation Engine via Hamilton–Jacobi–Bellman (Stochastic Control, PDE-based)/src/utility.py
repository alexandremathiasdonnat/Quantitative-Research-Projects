# src/utility.py
"""
Utility functions for the investor.

We use CRRA (power) utility:
    U(W) = W^(1-gamma)/(1-gamma)   if gamma != 1
    U(W) = log(W)                  if gamma == 1

We also provide analytical derivatives U'(W), U''(W),
which are useful both conceptually and for validation.

Important
---------
- CRRA is only defined for W > 0. The simulation and grids are built accordingly.
"""

import numpy as np


def crra_utility(W: np.ndarray, gamma: float) -> np.ndarray:
    W = np.asarray(W)
    if gamma == 1.0:
        return np.log(np.maximum(W, 1e-16))
    return (np.maximum(W, 1e-16) ** (1.0 - gamma)) / (1.0 - gamma)


def crra_u1(W: np.ndarray, gamma: float) -> np.ndarray:
    """
    U'(W).
    """
    W = np.asarray(W)
    if gamma == 1.0:
        return 1.0 / np.maximum(W, 1e-16)
    return np.maximum(W, 1e-16) ** (-gamma)


def crra_u2(W: np.ndarray, gamma: float) -> np.ndarray:
    """
    U''(W).
    """
    W = np.asarray(W)
    if gamma == 1.0:
        return -1.0 / (np.maximum(W, 1e-16) ** 2)
    return -gamma * (np.maximum(W, 1e-16) ** (-gamma - 1.0))
