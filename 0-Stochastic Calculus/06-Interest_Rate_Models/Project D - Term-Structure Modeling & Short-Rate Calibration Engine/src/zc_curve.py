# src/zc_curve.py

"""
Utilities to convert zero-coupon yields to prices and to interpolate
the term structure.

We assume continuously-compounded yields:
    P(0, T) = exp(-y(T) * T)
"""

from typing import Iterable

import numpy as np
import pandas as pd


def yields_to_prices(maturities: Iterable[float], yields: Iterable[float]) -> np.ndarray:
    """
    Convert zero-coupon yields to prices using continuous compounding.

    Parameters
    ----------
    maturities : iterable of float
        Times to maturity in years (T > 0).
    yields : iterable of float
        Zero-coupon yields y(T) in decimal, same length as maturities.

    Returns
    -------
    prices : ndarray of shape (n_maturities,)
        Zero-coupon prices P(0, T) = exp(-y(T) * T).
    """
    maturities = np.asarray(maturities, dtype=float)
    yields = np.asarray(yields, dtype=float)

    if maturities.shape != yields.shape:
        raise ValueError("maturities and yields must have the same shape.")

    return np.exp(-yields * maturities)


def interpolate_zc_prices(
    maturities: np.ndarray,
    prices: np.ndarray,
    new_maturities: np.ndarray,
    method: str = "log_linear",
) -> np.ndarray:
    """
    Interpolate a zero-coupon price curve to new maturities.

    Two simple methods:
        - 'linear' in price space,
        - 'log_linear' in log-price space (common in practice).

    Parameters
    ----------
    maturities : ndarray
        Original maturities (in years), strictly increasing.
    prices : ndarray
        Original ZC prices P(0, T) corresponding to maturities.
    new_maturities : ndarray
        New maturities at which to interpolate.
    method : {'linear', 'log_linear'}
        Interpolation scheme.

    Returns
    -------
    new_prices : ndarray
        Interpolated ZC prices.
    """
    maturities = np.asarray(maturities, dtype=float)
    prices = np.asarray(prices, dtype=float)
    new_maturities = np.asarray(new_maturities, dtype=float)

    if method not in {"linear", "log_linear"}:
        raise ValueError("method must be 'linear' or 'log_linear'.")

    if method == "linear":
        return np.interp(new_maturities, maturities, prices)

    # log-linear interpolation: interpolate log P, then exponentiate
    log_p = np.log(prices)
    log_p_new = np.interp(new_maturities, maturities, log_p)
    return np.exp(log_p_new)


def prices_to_yields(maturities: np.ndarray, prices: np.ndarray) -> np.ndarray:
    """
    Convert zero-coupon prices back to continuously-compounded yields.

    y(T) = - ln(P(0,T)) / T

    Parameters
    ----------
    maturities : ndarray
        Times to maturity in years (T > 0).
    prices : ndarray
        Zero-coupon prices.

    Returns
    -------
    yields : ndarray
        Zero-coupon yields.
    """
    maturities = np.asarray(maturities, dtype=float)
    prices = np.asarray(prices, dtype=float)

    if np.any(maturities <= 0):
        raise ValueError("All maturities must be > 0 for yield computation.")

    return -np.log(prices) / maturities
