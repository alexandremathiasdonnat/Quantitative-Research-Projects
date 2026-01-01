# src/market_models.py
"""
Market dynamics used throughout the project.

We consider a continuous-time market with:
- a risky asset S_t following GBM
- a risk-free asset growing at constant rate r

Risky asset:
    dS_t = mu * S_t dt + sigma * S_t dB_t

Wealth dynamics for a self-financing investor who allocates a fraction pi_t to the risky asset:
    dW_t = [ (r + pi_t (mu - r)) W_t ] dt + [ pi_t sigma W_t ] dB_t

Notes
-----
- We interpret pi_t as a *fraction of wealth* in the risky asset (can be >1 if leveraged, negative if short).
- In the "pure" Merton (CRRA + GBM) case, the optimal pi* is constant.
  However we still implement a full HJB numerical engine because:
  (1) it is the architecture we need for extensions (constraints, costs, multi-asset),
  (2) it demonstrates end-to-end portfolio stochastic control.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MarketParams:
    mu: float
    sigma: float
    r: float


def gbm_step(S: np.ndarray, mu: float, sigma: float, dt: float, z: np.ndarray) -> np.ndarray:
    """
    One Euler exact step for GBM (exact discretization).
    S_{t+dt} = S_t * exp((mu - 0.5 sigma^2) dt + sigma sqrt(dt) z)

    Parameters
    ----------
    S : np.ndarray
        Current prices.
    mu, sigma : float
        GBM drift and volatility.
    dt : float
        Time step.
    z : np.ndarray
        Standard normal increments (same shape as S).

    Returns
    -------
    np.ndarray
        Next-step prices.
    """
    return S * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)


def wealth_step(W: np.ndarray, pi: np.ndarray, mu: float, sigma: float, r: float, dt: float, z: np.ndarray) -> np.ndarray:
    """
    One step of wealth dynamics under fraction allocation pi.

    Discretization (log-Euler style, stable for positive wealth):
        W_{t+dt} = W_t * exp( (r + pi*(mu-r) - 0.5*(pi*sigma)^2) dt + (pi*sigma) sqrt(dt) z )

    This is consistent with the exact solution of log wealth when pi is constant over dt.

    Parameters
    ----------
    W : np.ndarray
        Current wealth.
    pi : np.ndarray
        Allocation fraction in risky asset at time t (same shape as W).
    mu, sigma, r : float
        Market parameters.
    dt : float
        Step size.
    z : np.ndarray
        Standard normal increment(s).

    Returns
    -------
    np.ndarray
        Next wealth values (positive).
    """
    drift = (r + pi * (mu - r) - 0.5 * (pi * sigma) ** 2) * dt
    diff = (pi * sigma) * np.sqrt(dt) * z
    return W * np.exp(drift + diff)
