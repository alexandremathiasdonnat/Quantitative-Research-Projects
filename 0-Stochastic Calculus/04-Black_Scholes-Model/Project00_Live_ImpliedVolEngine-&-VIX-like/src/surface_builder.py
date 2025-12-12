"""
surface_builder.py

Tools to build an implied volatility surface IV(K, T) from scattered data.

This module:
- Takes a DataFrame with implied volatilities ('iv' column).
- Builds regular grids for strikes and maturities.
- Interpolates implied volatilities on the (K, T) grid.
- Returns a surface suitable for 3D plots and VIX-like aggregation.

Dependencies: SciPy interpolation (griddata, Rbf) for flexibility.
"""

from typing import Tuple, Literal, Dict, Optional

import numpy as np
import pandas as pd
from scipy.interpolate import griddata, Rbf


InterpolationMethod = Literal["linear", "nearest", "rbf"]


def build_regular_grid(
    iv_df: pd.DataFrame,
    n_strikes: int = 40,
    n_maturities: int = 20,
    strike_padding: float = 0.05,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build a regular (K, T) grid based on the observed data.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain columns 'K', 'T' and 'iv'.
    n_strikes : int
        Number of points in the strike grid.
    n_maturities : int
        Number of points in the maturity grid.
    strike_padding : float
        Relative extra band added around [K_min, K_max].

    Returns
    -------
    K_grid : ndarray, shape (n_strikes,)
    T_grid : ndarray, shape (n_maturities,)

    Notes
    -----
    - We keep maturities in the [T_min, T_max] range (no padding).
    - We slightly extend the strike range to avoid visual clipping.
    """
    valid = iv_df.dropna(subset=["iv"])
    if valid.empty:
        raise ValueError("No valid implied volatilities in iv_df.")

    K_min, K_max = valid["K"].min(), valid["K"].max()
    T_min, T_max = valid["T"].min(), valid["T"].max()

    K_span = K_max - K_min
    K_low = K_min - strike_padding * K_span
    K_high = K_max + strike_padding * K_span

    K_grid = np.linspace(K_low, K_high, n_strikes)
    T_grid = np.linspace(T_min, T_max, n_maturities)

    return K_grid, T_grid


def interpolate_iv_surface(
    iv_df: pd.DataFrame,
    K_grid: np.ndarray,
    T_grid: np.ndarray,
    method: InterpolationMethod = "linear",
    rbf_kwargs: Optional[Dict] = None,
) -> np.ndarray:
    """
    Interpolate implied volatilities on a regular (K, T) grid.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv'. Each row is one observed option.
    K_grid : ndarray, shape (n_strikes,)
    T_grid : ndarray, shape (n_maturities,)
    method : {"linear", "nearest", "rbf"}
        Interpolation method:
        - "linear"  : SciPy griddata with linear interpolation (bilinear in 2D).
        - "nearest" : Nearest neighbor extrapolation (safe but rough).
        - "rbf"     : Radial Basis Function interpolation (smooth surface).
    rbf_kwargs : dict, optional
        Extra keyword arguments passed to scipy.interpolate.Rbf.

    Returns
    -------
    IV_surface : ndarray, shape (n_maturities, n_strikes)
        Interpolated implied volatility surface on the regular grid.

    Notes
    -----
    - K_grid is along the x-axis (columns).
    - T_grid is along the y-axis (rows).
    - This surface is used both for plotting and for VIX-like aggregation.
    """
    valid = iv_df.dropna(subset=["iv"])
    if valid.empty:
        raise ValueError("No valid implied volatilities to interpolate.")

    points = np.column_stack([valid["K"].values, valid["T"].values])
    values = valid["iv"].values

    KK, TT = np.meshgrid(K_grid, T_grid)

    if method in ("linear", "nearest"):
        IV_surface = griddata(
            points,
            values,
            (KK, TT),
            method=method,
        )
        # Some points may be NaN (outside convex hull) → fallback to nearest
        if method == "linear" and np.isnan(IV_surface).any():
            IV_surface_nearest = griddata(
                points,
                values,
                (KK, TT),
                method="nearest",
            )
            IV_surface = np.where(np.isnan(IV_surface), IV_surface_nearest, IV_surface)

    elif method == "rbf":
        rbf_kwargs = rbf_kwargs or {"function": "multiquadric", "smooth": 0.0}
        rbf = Rbf(valid["K"].values, valid["T"].values, values, **rbf_kwargs)
        IV_surface = rbf(KK, TT)

    else:
        raise ValueError("Unknown interpolation method: %r" % method)

    return IV_surface


def build_iv_surface(
    iv_df: pd.DataFrame,
    n_strikes: int = 40,
    n_maturities: int = 20,
    method: InterpolationMethod = "linear",
    strike_padding: float = 0.05,
    rbf_kwargs: Optional[Dict] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    High-level helper to build an IV surface from scattered IV data.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv'.
    n_strikes : int
        Number of strikes in the grid.
    n_maturities : int
        Number of maturities in the grid.
    method : {"linear", "nearest", "rbf"}
        Interpolation method.
    strike_padding : float
        Padding ratio for strike range.
    rbf_kwargs : dict, optional
        Extra RBF interpolation parameters.

    Returns
    -------
    K_grid : ndarray
    T_grid : ndarray
    IV_surface : ndarray, shape (n_maturities, n_strikes)

    Notes
    -----
    This is the function that the dashboard will call in Section D:
    - Build grid
    - Interpolate surface
    - Plot 3D + heatmap
    """
    K_grid, T_grid = build_regular_grid(
        iv_df,
        n_strikes=n_strikes,
        n_maturities=n_maturities,
        strike_padding=strike_padding,
    )
    IV_surface = interpolate_iv_surface(
        iv_df,
        K_grid,
        T_grid,
        method=method,
        rbf_kwargs=rbf_kwargs,
    )
    return K_grid, T_grid, IV_surface
