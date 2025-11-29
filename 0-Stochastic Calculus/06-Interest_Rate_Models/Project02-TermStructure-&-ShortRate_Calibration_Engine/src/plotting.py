# src/plotting.py

"""
Plotting utilities for term-structure and calibration diagnostics.
"""

from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np


def plot_zc_yields_vs_model(
    maturities: Iterable[float],
    market_yields: Iterable[float],
    model_yields: Iterable[float],
    title: str | None = None,
) -> None:
    """
    Plot market vs model zero-coupon yields.
    """
    maturities = np.asarray(maturities, dtype=float)
    market_yields = np.asarray(market_yields, dtype=float)
    model_yields = np.asarray(model_yields, dtype=float)

    plt.figure()
    plt.plot(maturities, market_yields * 100, "o-", label="Market yields")
    plt.plot(maturities, model_yields * 100, "s--", label="Model yields")
    plt.xlabel("Maturity (years)")
    plt.ylabel("Yield (%)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.title(title or "Zero-Coupon Yields: Market vs Model")
    plt.tight_layout()


def plot_zc_prices_error(
    maturities: Iterable[float],
    market_prices: Iterable[float],
    model_prices: Iterable[float],
    title: str | None = None,
) -> None:
    """
    Plot absolute errors between market and model zero-coupon prices.
    """
    maturities = np.asarray(maturities, dtype=float)
    market_prices = np.asarray(market_prices, dtype=float)
    model_prices = np.asarray(model_prices, dtype=float)

    errors = model_prices - market_prices

    plt.figure()
    plt.bar(maturities, errors, width=0.1)
    plt.xlabel("Maturity (years)")
    plt.ylabel("Model - Market price")
    plt.grid(True, axis="y", alpha=0.3)
    plt.title(title or "ZC Price Errors (Model - Market)")
    plt.tight_layout()


def plot_forward_curve(
    maturities: np.ndarray,
    forward_rates: np.ndarray,
    title: str | None = None,
) -> None:
    """
    Plot a forward rate curve F(0, T) for visualization.
    """
    maturities = np.asarray(maturities, dtype=float)
    forward_rates = np.asarray(forward_rates, dtype=float)

    plt.figure()
    plt.plot(maturities, forward_rates * 100, "o-")
    plt.xlabel("Maturity (years)")
    plt.ylabel("Forward rate (%)")
    plt.grid(True, alpha=0.3)
    plt.title(title or "Forward Rate Curve")
    plt.tight_layout()
