"""
High-level API for the Credit Risk Engine.

This module exposes clean functions that will be called from the main
Jupyter notebook dashboard. It hides the internal implementation details of:
    - Structural model (Merton),
    - CDS intensity calibration,
    - Copula-based portfolio simulation,
    - VaR/ES computation.

INPUT PROVENANCE
----------------
The notebook is responsible for:
    - Building company-level parameters (either manually or from CSV).
    - Building portfolio-level parameters:
        * EAD, recovery, maturity,
        * hazard rates (manual or calibrated from CDS),
        * correlation matrix,
        * copula type and number of scenarios.

All of those are passed here as plain numbers or numpy arrays.
"""

from dataclasses import dataclass
from typing import Literal, Optional, Dict, Any, Tuple

import numpy as np

from .structural_model import MertonParams, structural_pd_closed_form, distance_to_default
from .cds_pricing import CDSParams, calibrate_lambda, implied_pd_from_lambda
from .copula_simulation import simulate_default_times_copula
from .portfolio_loss import compute_losses, var_es


# ---- Structural API ----------


def compute_structural_pd(
    V0: float,
    D: float,
    mu: float,
    sigma_A: float,
    T: float,
) -> Dict[str, float]:
    """
    Compute structural default probability and distance-to-default
    for a single firm using the Merton model.

    Parameters
    ----------
    V0 : float
        Initial asset value.
    D : float
        Debt face value (default barrier at maturity).
    mu : float
        Asset drift (often risk-free rate under risk-neutral measure).
    sigma_A : float
        Asset volatility.
    T : float
        Horizon (years).

    Returns
    -------
    dict
        {
            "pd_structural": PD(T),
            "distance_to_default": DD
        }
    """
    params = MertonParams(V0=V0, D=D, mu=mu, sigma_A=sigma_A, T=T)
    dd = distance_to_default(params)
    pd = structural_pd_closed_form(params)
    return {
        "pd_structural": pd,
        "distance_to_default": dd,
    }


# CDS Calibration API


def calibrate_cds_lambda(
    spread_bps: float,
    maturity: float,
    recovery: float,
    rate: float,
    payment_frequency: int = 4,
) -> Dict[str, float]:
    """
    Calibrate the constant hazard rate λ from a quoted CDS spread.

    Parameters
    ----------
    spread_bps : float
        Quoted CDS spread (basis points).
    maturity : float
        CDS maturity in years.
    recovery : float
        Recovery rate.
    rate : float
        Flat risk-free rate.
    payment_frequency : int
        Number of premium payments per year.

    Returns
    -------
    dict
        {
            "lambda": λ*,
            "pd_implied": PD(T) under constant intensity
        }
    """
    params = CDSParams(
        spread_bps=spread_bps,
        maturity=maturity,
        recovery=recovery,
        rate=rate,
        payment_frequency=payment_frequency,
    )
    lam_star = calibrate_lambda(params)
    pd_impl = implied_pd_from_lambda(lam_star, maturity)
    return {
        "lambda": lam_star,
        "pd_implied": pd_impl,
    }


# Portfolio Simulation API


@dataclass
class PortfolioParams:
    """
    Parameters describing the credit portfolio.

    Attributes
    ----------
    ead : np.ndarray
        Exposures at default, shape (n_names,).
    recovery : np.ndarray
        Recoveries, shape (n_names,).
    maturity : np.ndarray
        Maturities, shape (n_names,).
    lam : np.ndarray
        Hazard rates λ_i, shape (n_names,).
    corr : np.ndarray
        Correlation matrix, shape (n_names, n_names).
    copula_type : {"gaussian", "t"}
        Type of copula used for dependence modelling.
    df : int
        Degrees of freedom (only for t-copula).
    n_scenarios : int
        Number of Monte Carlo scenarios.
    """
    ead: np.ndarray
    recovery: np.ndarray
    maturity: np.ndarray
    lam: np.ndarray
    corr: np.ndarray
    copula_type: Literal["gaussian", "t"] = "gaussian"
    df: int = 5
    n_scenarios: int = 100_000


def simulate_portfolio_losses(
    portfolio: PortfolioParams,
    random_state: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Simulate correlated defaults and compute the loss distribution.

    Parameters
    ----------
    portfolio : PortfolioParams
        Portfolio and copula configuration.
    random_state : int, optional
        Seed for reproducibility.

    Returns
    -------
    dict
        {
            "losses": np.ndarray of shape (n_scenarios,),
            "tau": default times of shape (n_scenarios, n_names)
        }
    """
    tau = simulate_default_times_copula(
        lam=portfolio.lam,
        corr=portfolio.corr,
        copula_type=portfolio.copula_type,
        df=portfolio.df,
        n_scenarios=portfolio.n_scenarios,
        random_state=random_state,
    )
    losses = compute_losses(
        tau=tau,
        ead=portfolio.ead,
        recovery=portfolio.recovery,
        maturity=portfolio.maturity,
    )
    return {"losses": losses, "tau": tau}


def compute_var_es(
    losses: np.ndarray,
    alpha_var: float = 0.99,
    alpha_es: float = 0.975,
) -> Dict[str, float]:
    """
    Wrapper around var_es to get VaR and ES from simulated losses.

    Parameters
    ----------
    losses : np.ndarray
        Losses per scenario.
    alpha_var : float
        VaR confidence level.
    alpha_es : float
        ES confidence level.

    Returns
    -------
    dict
        {
            "var": VaR_alpha_var,
            "es": ES_alpha_es
        }
    """
    v, e = var_es(losses, alpha_var=alpha_var, alpha_es=alpha_es)
    return {"var": v, "es": e}
