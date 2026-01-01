"""
iv_api.py

API for the Implied Volatility Engine & VIX-like Dashboard.
This module provides a clean, single entry point for the notebook:

- compute_iv_dataframe(options_df, S0, r, q)
- build_iv_surface(iv_df, grid_params)
- compute_vix_like(iv_df, surface, vix_params)
- full_analysis(...) → orchestrates the whole pipeline.

The idea: DataFrame  →  IVs  →  surface  →  VIX-like index  →  plots & interpretation
"""

from typing import Dict, Any, Optional, Tuple

import numpy as np
import pandas as pd

from .implied_vol import add_implied_vol_column
from .surface_builder import build_iv_surface
from .vix_engine import simple_vix_like, vix_like_from_surface


def compute_iv_dataframe(
    options_df: pd.DataFrame,
    S0: float,
    r: float,
    q: float = 0.0,
    initial_guess: float = 0.2,
    tol: float = 1e-6,
) -> pd.DataFrame:
    """
    Compute implied volatility for each option and return an enriched DataFrame.

    Parameters
    ----------
    options_df : DataFrame
        Input market snapshot. Must contain at least:
            'K'            : float (strike)
            'T'            : float (maturity in years)
            'option_type'  : {'call', 'put'}
            'market_price' : float (observed option price)
    S0 : float
        Spot price of the underlying.
    r : float
        Risk-free interest rate (annualized).
    q : float, optional
        Dividend yield (annualized).
    initial_guess : float, optional
        Initial guess for IV.
    tol : float, optional
        Tolerance for the solver.

    Returns
    -------
    iv_df : DataFrame
        Copy of options_df with an additional 'iv' column.

    Notes
    -----
    This function is the only one the notebook needs to call in Section B.
    """
    return add_implied_vol_column(
        options_df,
        S0=S0,
        r=r,
        q=q,
        initial_guess=initial_guess,
        tol=tol,
    )


def build_iv_surface_api(
    iv_df: pd.DataFrame,
    grid_params: Optional[Dict[str, Any]] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Wrapper around build_iv_surface with a convenient dict-based interface.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv'.
    grid_params : dict, optional
        Dictionary with optional keys:
            - 'n_strikes'      : int
            - 'n_maturities'   : int
            - 'method'         : {"linear", "nearest", "rbf"}
            - 'strike_padding' : float
            - 'rbf_kwargs'     : dict

    Returns
    -------
    K_grid : ndarray
    T_grid : ndarray
    IV_surface : ndarray
    """
    grid_params = grid_params or {}
    return build_iv_surface(
        iv_df,
        n_strikes=grid_params.get("n_strikes", 40),
        n_maturities=grid_params.get("n_maturities", 20),
        method=grid_params.get("method", "linear"),
        strike_padding=grid_params.get("strike_padding", 0.05),
        rbf_kwargs=grid_params.get("rbf_kwargs"),
    )


def compute_vix_like_api(
    iv_df: pd.DataFrame,
    S0: float,
    r: float,
    T_target: float,
    K_grid: Optional[np.ndarray] = None,
    T_grid: Optional[np.ndarray] = None,
    IV_surface: Optional[np.ndarray] = None,
    use_surface: bool = False,
    simple_params: Optional[Dict[str, Any]] = None,
) -> Optional[float]:
    """
    Compute a VIX-like index using either the simple or surface-based method.

    Parameters
    ----------
    iv_df : DataFrame
        Must contain 'K', 'T', 'iv'.
    S0 : float
        Spot price.
    r : float
        Risk-free rate.
    T_target : float
        Target maturity (in years).
    K_grid, T_grid, IV_surface : optional
        If provided and use_surface=True, the surface-based approximation
        vix_like_from_surface() is used.
    use_surface : bool
        If True, attempts to use the surface-based method.
        If False or if surface arguments are missing, fall back to simple_vix_like().
    simple_params : dict, optional
        Extra parameters for simple_vix_like():
            - 'moneyness_band'
            - 'maturity_tolerance'
            - 'weights_power'

    Returns
    -------
    vix_level : float or None
        VIX-like level in percentage.
    """
    simple_params = simple_params or {}

    if use_surface and K_grid is not None and T_grid is not None and IV_surface is not None:
        vix_level = vix_like_from_surface(
            K_grid=K_grid,
            T_grid=T_grid,
            IV_surface=IV_surface,
            r=r,
            T_target=T_target,
        )
        if vix_level is not None:
            return vix_level

    # Fallback to simple near-the-money aggregation
    return simple_vix_like(
        iv_df=iv_df,
        S0=S0,
        T_target=T_target,
        moneyness_band=simple_params.get("moneyness_band", 0.1),
        maturity_tolerance=simple_params.get("maturity_tolerance", 0.05),
        weights_power=simple_params.get("weights_power", 2.0),
    )


def full_analysis(
    options_df: pd.DataFrame,
    market_params: Dict[str, float],
    grid_params: Optional[Dict[str, Any]] = None,
    vix_params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Run the full pipeline: IVs, surface, VIX-like.

    Parameters
    ----------
    options_df : DataFrame
        Snapshot of option market data.
    market_params : dict
        Must at least contain:
            - 'S0' : float
            - 'r'  : float
            - 'q'  : float (can be 0.0)
    grid_params : dict, optional
        Parameters for IV surface building.
    vix_params : dict, optional
        Parameters for VIX-like computation:
            - 'T_target'     : float
            - 'use_surface'  : bool
            - 'simple_params': dict

    Returns
    -------
    results : dict
        {
            "iv_df"      : DataFrame with 'iv' column,
            "K_grid"     : ndarray,
            "T_grid"     : ndarray,
            "IV_surface" : ndarray,
            "vix_level"  : float or None
        }

    Notes
    -----
    The dashboard notebook can:
        - call full_analysis() once,
        - use the returned objects for plots + interpretation.
    """
    vix_params = vix_params or {}
    grid_params = grid_params or {}

    S0 = float(market_params["S0"])
    r = float(market_params["r"])
    q = float(market_params.get("q", 0.0))

    # Step 1: compute IVs
    iv_df = compute_iv_dataframe(
        options_df=options_df,
        S0=S0,
        r=r,
        q=q,
    )

    # Step 2: build surface
    K_grid, T_grid, IV_surface = build_iv_surface_api(
        iv_df=iv_df,
        grid_params=grid_params,
    )

    # Step 3: compute VIX-like index
    T_target = float(vix_params.get("T_target", T_grid[len(T_grid) // 2]))
    vix_level = compute_vix_like_api(
        iv_df=iv_df,
        S0=S0,
        r=r,
        T_target=T_target,
        K_grid=K_grid,
        T_grid=T_grid,
        IV_surface=IV_surface,
        use_surface=vix_params.get("use_surface", False),
        simple_params=vix_params.get("simple_params", None),
    )

    return {
        "iv_df": iv_df,
        "K_grid": K_grid,
        "T_grid": T_grid,
        "IV_surface": IV_surface,
        "vix_level": vix_level,
    }
