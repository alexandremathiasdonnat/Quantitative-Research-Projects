"""
plotting.py

Visualization utilities for the Implied Volatility & VIX Dashboard.

This module focuses on:
- Smiles: IV(K) at fixed maturity.
- Term structures: IV(T) at fixed strike.
- 3D surfaces and heatmaps of IV(K, T).
- Basic histograms and call/put comparisons.

All functions accept an existing matplotlib Axes (when possible),
but create one by default if not provided. This makes them easy to
reuse in a notebook or in scripts.
"""

from typing import Optional, Sequence

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  # needed for 3D projection


def plot_iv_smile(
    iv_df: pd.DataFrame,
    maturity: float,
    ax: Optional[plt.Axes] = None,
    label: Optional[str] = None,
):
    """
    Plot implied volatility smile IV(K) for a given maturity T.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv'.
    maturity : float
        Target maturity in years (we pick the closest available T).
    ax : matplotlib Axes, optional
        Axes to draw on. If None, create a new figure and axes.
    label : str, optional
        Label for the curve (useful when overlaying several maturities).

    Notes
    -----
    The function:
    - selects the subset of options with maturity closest to `maturity`,
    - plots K on the x-axis and IV on the y-axis.
    """
    if ax is None:
        fig, ax = plt.subplots()

    valid = iv_df.dropna(subset=["iv"])
    if valid.empty:
        ax.set_title("No implied vol data available")
        return ax

    # Choose the closest maturity to the requested one
    unique_T = np.sort(valid["T"].unique())
    idx = np.argmin(np.abs(unique_T - maturity))
    T_closest = unique_T[idx]

    slice_df = valid[valid["T"] == T_closest].sort_values("K")

    ax.plot(slice_df["K"], slice_df["iv"], marker="o", linestyle="-", label=label or f"T={T_closest:.3f}")
    ax.set_xlabel("Strike K")
    ax.set_ylabel("Implied volatility")
    ax.set_title(f"IV Smile (T ≈ {T_closest:.3f} years)")
    ax.grid(True)
    if label is not None:
        ax.legend()

    return ax


def plot_term_structure(
    iv_df: pd.DataFrame,
    strike: float,
    ax: Optional[plt.Axes] = None,
):
    """
    Plot term structure of implied volatility IV(T) for a given strike K.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv'.
    strike : float
        Target strike K (we pick the closest available K).
    ax : matplotlib Axes, optional
        Axes to draw on.

    Notes
    -----
    The function:
    - picks the closest strike to `strike`,
    - plots maturity T on the x-axis and IV on the y-axis.
    """
    if ax is None:
        fig, ax = plt.subplots()

    valid = iv_df.dropna(subset=["iv"])
    if valid.empty:
        ax.set_title("No implied vol data available")
        return ax

    unique_K = np.sort(valid["K"].unique())
    idx = np.argmin(np.abs(unique_K - strike))
    K_closest = unique_K[idx]

    slice_df = valid[valid["K"] == K_closest].sort_values("T")

    ax.plot(slice_df["T"], slice_df["iv"], marker="o", linestyle="-")
    ax.set_xlabel("Maturity T (years)")
    ax.set_ylabel("Implied volatility")
    ax.set_title(f"Term Structure (K ≈ {K_closest:.2f})")
    ax.grid(True)

    return ax


def plot_iv_surface_3d(
    K_grid: np.ndarray,
    T_grid: np.ndarray,
    IV_surface: np.ndarray,
    elev: int = 25,
    azim: int = -135,
):
    """
    Plot the full implied volatility surface as a 3D surface.

    Parameters
    ----------
    K_grid : ndarray, shape (n_strikes,)
    T_grid : ndarray, shape (n_maturities,)
    IV_surface : ndarray, shape (n_maturities, n_strikes)
    elev, azim : int
        Elevation and azimuth angles for the 3D view.

    Notes
    -----
    This is the “signature” visualization of the project:
    - K is on the x-axis
    - T is on the y-axis
    - IV(K, T) on the z-axis
    """
    KK, TT = np.meshgrid(K_grid, T_grid)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(KK, TT, IV_surface, cmap="viridis", alpha=0.9)

    ax.set_xlabel("Strike K")
    ax.set_ylabel("Maturity T (years)")
    ax.set_zlabel("Implied volatility")
    ax.set_title("Implied Volatility Surface")

    fig.colorbar(surf, shrink=0.5, aspect=10, label="IV")
    ax.view_init(elev=elev, azim=azim)

    return ax


def plot_iv_heatmap(
    K_grid: np.ndarray,
    T_grid: np.ndarray,
    IV_surface: np.ndarray,
):
    """
    Plot a heatmap of the implied volatility surface.

    Parameters
    ----------
    K_grid : ndarray
    T_grid : ndarray
    IV_surface : ndarray, shape (n_maturities, n_strikes)

    Notes
    -----
    This is the 2D complement to the 3D surface:
    - color encodes IV,
    - axes are K and T.
    """
    fig, ax = plt.subplots()

    extent = [K_grid.min(), K_grid.max(), T_grid.min(), T_grid.max()]
    im = ax.imshow(
        IV_surface,
        origin="lower",
        extent=extent,
        aspect="auto",
        cmap="viridis",
    )
    ax.set_xlabel("Strike K")
    ax.set_ylabel("Maturity T (years)")
    ax.set_title("Implied Volatility Heatmap")
    cbar = fig.colorbar(im)
    cbar.set_label("IV")

    return ax


def plot_iv_histogram(
    iv_df: pd.DataFrame,
    ax: Optional[plt.Axes] = None,
    bins: int = 30,
):
    """
    Plot histogram of implied volatilities in the DataFrame.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'iv'.
    ax : matplotlib Axes, optional
        Axes to draw on.
    bins : int
        Number of bins for the histogram.

    Notes
    -----
    This helps detect:
    - presence of outliers,
    - clustering of IV levels,
    - regime shifts between maturities/strikes.
    """
    if ax is None:
        fig, ax = plt.subplots()

    valid_iv = iv_df["iv"].dropna()
    if valid_iv.empty:
        ax.set_title("No implied vol data available")
        return ax

    ax.hist(valid_iv, bins=bins, alpha=0.7, edgecolor="black")
    ax.set_xlabel("Implied volatility")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Implied Volatilities")
    ax.grid(True)

    return ax


def plot_call_put_iv_comparison(
    iv_df: pd.DataFrame,
    maturity: float,
    ax: Optional[plt.Axes] = None,
):
    """
    Compare call vs put implied vol along strikes at a given maturity.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv', 'option_type'.
    maturity : float
        Target maturity in years (closest T is picked).
    ax : matplotlib Axes, optional

    Notes
    -----
    This helps visualize possible call/put IV asymmetry.
    """
    if ax is None:
        fig, ax = plt.subplots()

    valid = iv_df.dropna(subset=["iv"])
    if valid.empty:
        ax.set_title("No implied vol data available")
        return ax

    unique_T = np.sort(valid["T"].unique())
    idx = np.argmin(np.abs(unique_T - maturity))
    T_closest = unique_T[idx]

    slice_df = valid[valid["T"] == T_closest]

    calls = slice_df[slice_df["option_type"].str.lower() == "call"].sort_values("K")
    puts = slice_df[slice_df["option_type"].str.lower() == "put"].sort_values("K")

    if not calls.empty:
        ax.plot(calls["K"], calls["iv"], marker="o", linestyle="-", label="Calls")
    if not puts.empty:
        ax.plot(puts["K"], puts["iv"], marker="x", linestyle="--", label="Puts")

    ax.set_xlabel("Strike K")
    ax.set_ylabel("Implied volatility")
    ax.set_title(f"Call vs Put IV (T ≈ {T_closest:.3f} years)")
    ax.grid(True)
    ax.legend()

    return ax
