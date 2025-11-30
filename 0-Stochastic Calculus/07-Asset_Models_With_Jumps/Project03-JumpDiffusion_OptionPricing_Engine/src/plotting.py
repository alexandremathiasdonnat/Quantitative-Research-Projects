"""
plotting.py

Plot utilities for:
- price surfaces,
- volatility smiles,
- path simulations.

These functions take numpy arrays produced by pide_solver / simulation
and matplotlib axes or create their own figures.

All inputs (arrays, strikes, prices) come from the notebook or from
other modules; there is no file access here.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from typing import Sequence, Tuple


def plot_price_surface(
    S_grid: np.ndarray,
    tau_grid: np.ndarray,
    U: np.ndarray,
    title: str = "PIDE price surface",
) -> None:
    """Plot price surface U(tau, S)."""
    T = tau_grid[-1]
    # Convert tau (time-to-maturity) to actual time t = T - tau if you want;
    # here we just show tau.
    Tau, S = np.meshgrid(tau_grid, S_grid, indexing="ij")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(S, Tau, U, linewidth=0.0, antialiased=True)
    ax.set_xlabel("S")
    ax.set_ylabel("tau")
    ax.set_zlabel("price")
    ax.set_title(title)
    plt.tight_layout()


# --- Black–Scholes helpers for implied vol -------------------------------

def _norm_cdf(x: np.ndarray) -> np.ndarray:
    """Standard normal CDF using error function."""
    return 0.5 * (1.0 + np.erf(x / np.sqrt(2.0)))


def black_scholes_call(
    S0: float,
    K: float,
    T: float,
    r: float,
    q: float,
    sigma: float,
) -> float:
    """Black–Scholes European call price."""
    if T <= 0:
        return max(S0 - K, 0.0)

    import math

    d1 = (math.log(S0 / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    from math import erf, sqrt

    def cdf(z: float) -> float:
        return 0.5 * (1.0 + erf(z / sqrt(2.0)))

    return S0 * math.exp(-q * T) * cdf(d1) - K * math.exp(-r * T) * cdf(d2)


def implied_vol_call_bisection(
    price: float,
    S0: float,
    K: float,
    T: float,
    r: float,
    q: float,
    tol: float = 1e-6,
    max_iter: int = 100,
    sigma_low: float = 1e-4,
    sigma_high: float = 5.0,
) -> float:
    """Implied vol for a call via simple bisection."""
    if T <= 0:
        return 0.0

    pl = black_scholes_call(S0, K, T, r, q, sigma_low)
    ph = black_scholes_call(S0, K, T, r, q, sigma_high)

    # If price is out of range, just clip.
    if price <= pl:
        return sigma_low
    if price >= ph:
        return sigma_high

    for _ in range(max_iter):
        mid = 0.5 * (sigma_low + sigma_high)
        pm = black_scholes_call(S0, K, T, r, q, mid)
        if abs(pm - price) < tol:
            return mid
        if pm > price:
            sigma_high = mid
        else:
            sigma_low = mid
    return 0.5 * (sigma_low + sigma_high)


def plot_implied_vol_smile(
    strikes: Sequence[float],
    prices: Sequence[float],
    S0: float,
    T: float,
    r: float,
    q: float,
    label: str = "Jump model",
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute and plot implied vol smile from given prices."""
    strikes = np.asarray(strikes, dtype=float)
    prices = np.asarray(prices, dtype=float)

    ivols = np.zeros_like(strikes, dtype=float)
    for i, K in enumerate(strikes):
        ivols[i] = implied_vol_call_bisection(
            price=float(prices[i]),
            S0=S0,
            K=float(K),
            T=T,
            r=r,
            q=q,
        )

    plt.figure()
    moneyness = strikes / S0
    plt.plot(moneyness, ivols, marker="o", label=label)
    plt.xlabel("K / S0")
    plt.ylabel("Implied vol")
    plt.title("Implied vol smile")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    return strikes, ivols


def plot_paths(
    t_grid: np.ndarray,
    paths: np.ndarray,
    n_show: int = 20,
    title: str = "Jump–diffusion paths",
) -> None:
    """Plot a subset of simulated paths."""
    n_paths = paths.shape[0]
    n_show = min(n_show, n_paths)

    plt.figure()
    for i in range(n_show):
        plt.plot(t_grid, paths[i, :], alpha=0.7)
    plt.xlabel("t")
    plt.ylabel("S_t")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
