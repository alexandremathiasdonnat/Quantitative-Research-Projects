# src/hjb_equation.py
"""
HJB equation builder (continuous-time portfolio choice).

State variable: wealth W >= 0
Control: risky fraction pi

Wealth SDE:
    dW = a(pi) W dt + b(pi) W dB
where:
    a(pi) = r + pi (mu - r)
    b(pi) = pi sigma

Value function:
    V(t, W) = sup_{pi} E[ U(W_T) | W_t = W ]

HJB (terminal value problem):
    0 = V_t + max_pi { a(pi) W V_W + 0.5 b(pi)^2 W^2 V_WW }
    V(T, W) = U(W)

For CRRA, the continuous-time analytic optimizer (Merton) is:
    pi* = (mu - r) / (gamma sigma^2)
and is constant (no t, no W dependence) in the unconstrained 1-asset model.

But we compute pi*(t,W) numerically from the discretized HJB to:
- demonstrate the pipeline,
- enable easy extensions (constraints, costs, multi-asset, time-varying coefficients).
"""

import numpy as np


def hjb_hamiltonian(W: np.ndarray, Vw: np.ndarray, Vww: np.ndarray, mu: float, sigma: float, r: float, pi_grid: np.ndarray) -> np.ndarray:
    """
    Compute the Hamiltonian on a grid of pi values:
        H(pi) = a(pi) W Vw + 0.5 b(pi)^2 W^2 Vww

    Parameters
    ----------
    W : np.ndarray
        Wealth grid points (shape: [nW]).
    Vw, Vww : np.ndarray
        First and second derivatives w.r.t wealth at a fixed time (shape: [nW]).
    mu, sigma, r : float
        Market params.
    pi_grid : np.ndarray
        Candidate controls (shape: [nPi]).

    Returns
    -------
    H : np.ndarray
        Hamiltonian values, shape [nPi, nW].
    """
    W = np.asarray(W)
    Vw = np.asarray(Vw)
    Vww = np.asarray(Vww)
    pi_grid = np.asarray(pi_grid)

    a = r + pi_grid[:, None] * (mu - r)
    b = (pi_grid[:, None] * sigma)

    H = a * (W[None, :] * Vw[None, :]) + 0.5 * (b**2) * ((W[None, :] ** 2) * Vww[None, :])
    return H


def merton_fraction(mu: float, r: float, sigma: float, gamma: float) -> float:
    """
    Closed-form Merton fraction for CRRA under GBM.

    pi* = (mu - r) / (gamma sigma^2)
    """
    if sigma <= 0:
        raise ValueError("sigma must be > 0")
    if gamma <= 0:
        raise ValueError("gamma must be > 0 for CRRA risk aversion")
    return (mu - r) / (gamma * sigma**2)
