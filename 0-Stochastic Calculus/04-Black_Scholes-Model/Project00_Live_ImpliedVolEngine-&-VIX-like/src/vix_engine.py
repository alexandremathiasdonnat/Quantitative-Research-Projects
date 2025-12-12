"""
vix_engine.py

Simplified VIX-like index construction.

This module exposes two main ideas:
- A very simple VIX-like index based on near-the-money implied vols.
- A more "formula-like" approximation inspired by the official VIX recipe.

Both approaches are pedagogical; the goal is to:
- Aggregate the IV smile into a single "market fear" number.
- Show the link between option prices, implied vol and volatility indices.
"""

from typing import Optional, Tuple

import numpy as np
import pandas as pd


def _select_near_the_money_slice(
    iv_df: pd.DataFrame,
    S0: float,
    T_target: float,
    moneyness_band: float = 0.1,
    maturity_tolerance: float = 0.05,
) -> pd.DataFrame:
    """
    Filter options near a given maturity and near-the-money.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv'.
    S0 : float
        Spot price.
    T_target : float
        Target maturity in years (e.g. ~30 days = 30/365).
    moneyness_band : float
        Keep strikes with K/S0 in [1 - band, 1 + band].
    maturity_tolerance : float
        Keep maturities in [T_target - tol, T_target + tol].

    Returns
    -------
    DataFrame
        Subset of iv_df compatible with the band and maturity window.
    """
    if iv_df.empty:
        return iv_df

    lower_T = max(0.0, T_target - maturity_tolerance)
    upper_T = T_target + maturity_tolerance

    df = iv_df.dropna(subset=["iv"]).copy()
    df = df[(df["T"] >= lower_T) & (df["T"] <= upper_T)]

    if df.empty:
        return df

    moneyness = df["K"] / S0
    mask = (moneyness >= 1.0 - moneyness_band) & (moneyness <= 1.0 + moneyness_band)
    return df[mask]


def simple_vix_like(
    iv_df: pd.DataFrame,
    S0: float,
    T_target: float,
    moneyness_band: float = 0.1,
    maturity_tolerance: float = 0.05,
    weights_power: float = 2.0,
) -> Optional[float]:
    """
    Compute a simple VIX-like index from near-the-money implied vols.

    Idea
    ----
    - Select options with maturity ~ T_target and strikes near S0.
    - Take a weighted average of their implied vols.
    - Return annualized volatility as a percentage.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv'.
    S0 : float
        Spot price.
    T_target : float
        Target maturity (in years).
    moneyness_band : float
        Range around ATM (K/S0 ∈ [1 - band, 1 + band]).
    maturity_tolerance : float
        Acceptable deviation around T_target (in years).
    weights_power : float
        Weight options by 1 / (distance_to_ATM^power).
        Higher power → stronger focus on pure ATM.

    Returns
    -------
    vix_level : float or None
        Annualized volatility in percentage (e.g. 20.0 for 20%),
        or None if there is not enough data.

    Notes
    -----
    This is deliberately simple and transparent. It is perfect to:
    - show how IVs from many options collapse into a single scalar,
    - build an internal "fear gauge" for the dashboard.
    """
    slice_df = _select_near_the_money_slice(
        iv_df,
        S0=S0,
        T_target=T_target,
        moneyness_band=moneyness_band,
        maturity_tolerance=maturity_tolerance,
    )

    if slice_df.empty:
        return None

    # Distance to ATM in absolute moneyness
    m = slice_df["K"] / S0
    dist = np.abs(m - 1.0)
    # Avoid division by zero for perfect ATM
    dist = np.where(dist < 1e-6, 1e-6, dist)

    weights = 1.0 / (dist**weights_power)
    weights = weights / weights.sum()

    iv_values = slice_df["iv"].values
    iv_atm_weighted = float(np.sum(weights * iv_values))

    # Annualize already in IV (sigma is annualized) : just express in %
    vix_level_pct = iv_atm_weighted * 100.0
    return vix_level_pct


def vix_like_from_surface(
    K_grid: np.ndarray,
    T_grid: np.ndarray,
    IV_surface: np.ndarray,
    r: float,
    T_target: float,
) -> Optional[float]:
    """
    Slightly more "formula-like" VIX approximation using the surface.

    Simplified formula (in spirit of VIX):
        VIX^2 ~ (2 / T) * Σ [ ΔK_i / K_i^2 * e^{rT} * Q(K_i) ]
    where Q(K_i) is the (out-of-the-money) option price at strike K_i.

    Here, for pedagogy:
    - We don't have prices per se on the grid, only IVs.
    - We approximate prices via Black–Scholes on the surface's IV.

    For the dashboard, you can:
    - Either ignore this and use simple_vix_like(),
    - Or keep it as an "advanced" demo.

    Parameters
    ----------
    K_grid : ndarray, shape (n_strikes,)
    T_grid : ndarray, shape (n_maturities,)
    IV_surface : ndarray, shape (n_maturities, n_strikes)
    r : float
        Risk-free rate.
    T_target : float
        Target maturity (in years).

    Returns
    -------
    vix_level : float or None
        Annualized volatility in percentage.

    Notes
    -----
    This function is intentionally lightweight; a full VIX replication
    would require a much more careful construction (OTM calls/puts,
    integration over strikes, etc.).
    """
    # Find the closest maturity index to T_target
    if len(T_grid) == 0 or len(K_grid) == 0:
        return None

    idx_T = int(np.argmin(np.abs(T_grid - T_target)))
    T_closest = float(T_grid[idx_T])
    if T_closest <= 0.0:
        return None

    iv_slice = IV_surface[idx_T, :]
    if np.isnan(iv_slice).all():
        return None

    # Approximate Q(K_i) ∝ IV * K * sqrt(T) 
    # We do not import full BS here to keep the module simple.
    Q = np.maximum(iv_slice, 0.0) * K_grid * np.sqrt(T_closest)

    # Approximate ΔK_i as finite differences on the K grid
    dK = np.diff(K_grid)
    if len(dK) == 0:
        return None
    # For simplicity, use midpoint ΔK
    dK = np.concatenate(([dK[0]], dK))

    integrand = (dK / (K_grid**2)) * np.exp(r * T_closest) * Q
    # Replace NaNs by zero in integrand
    integrand = np.nan_to_num(integrand, nan=0.0)

    vix_sq = (2.0 / T_closest) * np.sum(integrand)
    if vix_sq <= 0.0:
        return None

    vix_level = np.sqrt(vix_sq) * 100.0
    return float(vix_level)
