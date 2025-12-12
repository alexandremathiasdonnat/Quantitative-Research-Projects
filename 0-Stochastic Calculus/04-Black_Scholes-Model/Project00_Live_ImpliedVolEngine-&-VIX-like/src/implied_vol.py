"""
implied_vol.py

Low-level utilities to work with Black–Scholes prices and implied volatility.

This module provides:
- Closed-form Black–Scholes pricing for calls and puts.
- Vega (derivative of price wrt volatility).
- Robust implied volatility solvers (Newton + bisection fallback).
- A helper that adds an 'iv' column to an options DataFrame.

Expected input DataFrame structure:
    columns = ['K', 'T', 'option_type', 'market_price', ...]
"""

from typing import Optional
import numpy as np
import pandas as pd
from scipy.stats import norm


def bs_price(
    S: float,
    K: float,
    T: float,
    r: float,
    q: float,
    sigma: float,
    option_type: str = "call",
) -> float:
    """
    Black–Scholes price of a European call or put with continuous dividend yield.

    Parameters
    ----------
    S : float
        Spot price of the underlying at time t.
    K : float
        Strike price of the option.
    T : float
        Time-to-maturity in years (T > 0).
    r : float
        Risk-free interest rate (annualized).
    q : float
        Continuous dividend yield (annualized).
    sigma : float
        Volatility (annualized) of the underlying.
    option_type : {"call", "put"}
        Type of the option.

    Returns
    -------
    float
        Theoretical Black–Scholes price.

    Notes
    -----
    - This function is scalar on purpose; the dashboard will call it
      many times under the hood.
    - No arbitrage sanity checks are enforced here; they are handled
      by the implied volatility layer.
    """
    if T <= 0 or sigma <= 0:
        # Degenerate case: option is basically worth its intrinsic value
        intrinsic = max(0.0, (S - K) if option_type == "call" else (K - S))
        return intrinsic

    # Classic d1, d2 definitions under Black–Scholes with dividend yield
    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT

    if option_type.lower() == "call":
        price = np.exp(-q * T) * S * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)
    elif option_type.lower() == "put":
        price = np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(-q * T) * S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'.")

    return float(price)


def bs_vega(
    S: float,
    K: float,
    T: float,
    r: float,
    q: float,
    sigma: float,
) -> float:
    """
    Black–Scholes Vega (sensitivity of price wrt volatility).

    Returns
    -------
    float
        Vega = dPrice/dSigma

    Notes
    -----
    Vega is always positive for standard options. It is used by Newton's
    method to update volatility guesses when inverting the BS formula.
    """
    if T <= 0 or sigma <= 0:
        return 0.0

    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrtT)
    vega = np.exp(-q * T) * S * norm.pdf(d1) * sqrtT
    return float(vega)


def _implied_vol_newton(
    market_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    q: float,
    option_type: str,
    initial_guess: float = 0.2,
    tol: float = 1e-6,
    max_iter: int = 50,
) -> Optional[float]:
    """
    Try to solve for implied volatility using Newton's method.

    Returns
    -------
    float or None
        Implied volatility if convergence is reached, otherwise None.

    Notes
    -----
    Newton is very fast when the initial guess is reasonable and Vega
    is not too small. It can fail if:
    - The option is deep ITM/OTM (vega ~ 0).
    - The market price is not compatible with BS-no-arbitrage bounds.
    """
    sigma = max(initial_guess, 1e-4)

    for _ in range(max_iter):
        price = bs_price(S, K, T, r, q, sigma, option_type)
        diff = price - market_price

        if abs(diff) < tol:
            return float(sigma)

        vega = bs_vega(S, K, T, r, q, sigma)
        if vega < 1e-8:  # too small, Newton becomes unstable
            return None

        # Newton update
        sigma -= diff / vega

        # Keep volatility in a reasonable band
        if sigma <= 0:
            sigma = 1e-4
        if sigma > 5.0:
            sigma = 5.0

    return None


def _implied_vol_bisection(
    market_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    q: float,
    option_type: str,
    sigma_lower: float = 1e-4,
    sigma_upper: float = 5.0,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> Optional[float]:
    """
    Robust but slower implied volatility via bisection.

    Returns
    -------
    float or None
        Implied volatility if a root is bracketed, else None.

    Notes
    -----
    Bisection requires that the target price lies between the BS prices
    at sigma_lower and sigma_upper. If not, there is no solution in this
    range and we return None.
    """
    price_low = bs_price(S, K, T, r, q, sigma_lower, option_type)
    price_high = bs_price(S, K, T, r, q, sigma_upper, option_type)

    # Check if the market price is bracketed
    if not (min(price_low, price_high) <= market_price <= max(price_low, price_high)):
        return None

    low, high = sigma_lower, sigma_upper

    for _ in range(max_iter):
        mid = 0.5 * (low + high)
        price_mid = bs_price(S, K, T, r, q, mid, option_type)

        if abs(price_mid - market_price) < tol:
            return float(mid)

        if (price_mid < market_price) == (price_low < market_price):
            low, price_low = mid, price_mid
        else:
            high, price_high = mid, price_mid

    return float(0.5 * (low + high))


def implied_vol(
    market_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    q: float,
    option_type: str,
    initial_guess: float = 0.2,
    tol: float = 1e-6,
) -> Optional[float]:
    """
    Compute implied volatility using a hybrid method:
    - First, try Newton's method for speed.
    - If it fails, fall back to bisection for robustness.

    Parameters
    ----------
    market_price : float
        Observed market price of the option.
    S, K, T, r, q : float
        Standard Black–Scholes inputs.
    option_type : {"call", "put"}
        Option type.
    initial_guess : float, optional
        Starting value for Newton's method.
    tol : float, optional
        Tolerance for convergence.

    Returns
    -------
    float or None
        Implied volatility if solved, otherwise None (NaN placeholder in dashboard).
    """
    if market_price <= 0.0:
        return None

    # Quick no-arbitrage sanity check (approximate)
    intrinsic = max(0.0, (S - K) if option_type == "call" else (K - S))
    if market_price < intrinsic:
        # Market price below intrinsic → inconsistent with any non-negative vol
        return None

    # Try Newton
    sigma = _implied_vol_newton(
        market_price,
        S,
        K,
        T,
        r,
        q,
        option_type,
        initial_guess=initial_guess,
        tol=tol,
    )
    if sigma is not None:
        return sigma

    # Fallback to bisection
    sigma = _implied_vol_bisection(
        market_price,
        S,
        K,
        T,
        r,
        q,
        option_type,
        tol=tol,
    )
    return sigma


def add_implied_vol_column(
    options_df: pd.DataFrame,
    S0: float,
    r: float,
    q: float = 0.0,
    initial_guess: float = 0.2,
    tol: float = 1e-6,
) -> pd.DataFrame:
    """
    Compute implied volatility for each row of an options DataFrame.

    Parameters
    ----------
    options_df : DataFrame
        Must contain at least:
            'K'            : float
            'T'            : float (in years)
            'option_type'  : {'call', 'put'}
            'market_price' : float
    S0 : float
        Spot price of the underlying.
    r : float
        Risk-free rate (annualized).
    q : float, optional
        Dividend yield (annualized). Default is 0.0.
    initial_guess : float, optional
        Initial guess for Newton's method.
    tol : float, optional
        Tolerance for convergence.

    Returns
    -------
    DataFrame
        Copy of options_df with an additional 'iv' column (float).
        Rows where IV cannot be found get NaN.

    Notes
    -----
    This is the main entry point used by the dashboard:
    - Section B will call this once after loading the CSV.
    - All downstream plots and the VIX engine will rely on this 'iv' column.
    """
    df = options_df.copy()

    iv_list = []
    for _, row in df.iterrows():
        K = float(row["K"])
        T = float(row["T"])
        option_type = str(row["option_type"]).lower()
        market_price = float(row["market_price"])

        sigma = implied_vol(
            market_price=market_price,
            S=S0,
            K=K,
            T=T,
            r=r,
            q=q,
            option_type=option_type,
            initial_guess=initial_guess,
            tol=tol,
        )
        iv_list.append(np.nan if sigma is None else float(sigma))

    df["iv"] = iv_list
    return df
