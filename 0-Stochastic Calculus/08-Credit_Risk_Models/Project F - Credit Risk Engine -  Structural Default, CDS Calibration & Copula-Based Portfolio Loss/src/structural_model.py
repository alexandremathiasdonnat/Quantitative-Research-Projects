"""
Structural credit risk model (Merton).

This module implements the Merton model in closed form, with optional
Monte Carlo simulation of the asset value at maturity.

INPUT PROVENANCE
----------------
In the notebook, the inputs will typically come from:
    - Manual definitions for a single company:
        V0, D, mu, sigma_A, T
    - Or from a CSV (via pandas) for multiple firms where each row
      provides firm-specific parameters.

No file reading is done here: this module only consumes numerical
arrays/scalars passed from the notebook or another script.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
from scipy.stats import norm


@dataclass
class MertonParams:
    """
    Parameters for the Merton structural model.

    Attributes
    ----------
    V0 : float
        Initial asset value of the firm.
    D : float
        Face value of debt (default barrier at maturity).
    mu : float
        Drift of the asset value under the chosen measure
        (often risk-free rate r under risk-neutral measure).
    sigma_A : float
        Asset volatility.
    T : float
        Time horizon (years).
    n_paths : int, optional
        Number of Monte Carlo paths for optional simulation.
    """
    V0: float
    D: float
    mu: float
    sigma_A: float
    T: float
    n_paths: int = 10_000


def distance_to_default(params: MertonParams) -> float:
    """
    Compute the distance-to-default (DD) in the Merton model.

    DD = [ln(V0 / D) + (mu - 0.5 * sigma_A^2)*T] / (sigma_A * sqrt(T))

    Parameters
    ----------
    params : MertonParams
        Structural model parameters.

    Returns
    -------
    float
        Distance-to-default (number of standard deviations).
    """
    V0 = params.V0
    D = params.D
    mu = params.mu
    sigma = params.sigma_A
    T = params.T

    num = np.log(V0 / D) + (mu - 0.5 * sigma**2) * T
    den = sigma * np.sqrt(T)
    return num / den


def structural_pd_closed_form(params: MertonParams) -> float:
    """
    Compute the structural default probability using the Merton formula.

    PD = Φ(-DD), where DD is the distance-to-default.

    Parameters
    ----------
    params : MertonParams

    Returns
    -------
    float
        Default probability P(V_T < D) in the Merton model.
    """
    dd = distance_to_default(params)
    return norm.cdf(-dd)


def simulate_terminal_assets(params: MertonParams, random_state: Optional[int] = None) -> np.ndarray:
    """
    Simulate terminal asset values V_T under a lognormal diffusion.

    dV_t = mu * V_t dt + sigma_A * V_t dW_t
    ⇒ ln(V_T) ~ N(ln(V0) + (mu - 0.5 sigma_A^2) T, sigma_A^2 T)

    Parameters
    ----------
    params : MertonParams
    random_state : int, optional
        Seed for reproducibility.

    Returns
    -------
    np.ndarray
        Simulated terminal asset values, shape (n_paths,).
    """
    rng = np.random.default_rng(random_state)
    V0 = params.V0
    mu = params.mu
    sigma = params.sigma_A
    T = params.T
    n = params.n_paths

    mean_ln = np.log(V0) + (mu - 0.5 * sigma**2) * T
    std_ln = sigma * np.sqrt(T)

    ln_VT = rng.normal(loc=mean_ln, scale=std_ln, size=n)
    VT = np.exp(ln_VT)
    return VT


def structural_pd_monte_carlo(
    params: MertonParams,
    random_state: Optional[int] = None,
) -> Tuple[float, np.ndarray]:
    """
    Estimate the default probability by Monte Carlo simulation.

    Default occurs if V_T < D.

    Parameters
    ----------
    params : MertonParams
    random_state : int, optional

    Returns
    -------
    pd_hat : float
        Monte Carlo estimate of the default probability.
    VT : np.ndarray
        Simulated terminal asset values (for plotting).
    """
    VT = simulate_terminal_assets(params, random_state=random_state)
    default_events = VT < params.D
    pd_hat = default_events.mean()
    return pd_hat, VT
