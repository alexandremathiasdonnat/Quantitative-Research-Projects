"""
Simple hazard-rate models for default times.

We only consider a constant hazard rate λ (homogeneous Poisson process),
so default time τ ~ Exp(λ).

INPUT PROVENANCE
----------------
λ will be either:
    - chosen manually in the notebook (toy examples), or
    - calibrated from CDS spreads via `cds_pricing.calibrate_lambda`.

This module does not allocate or read data files.
"""

from typing import Union, Sequence, Optional

import numpy as np


def sample_default_times(
    lam: Union[float, np.ndarray],
    n_scenarios: int,
    random_state: Optional[int] = None,
) -> np.ndarray:
    """
    Sample exponential default times for one or several names.

    Parameters
    ----------
    lam : float or np.ndarray
        Hazard rate λ for each name. If scalar, same λ for all names.
        If array-like of shape (n_names,), each name has its own λ_i.
    n_scenarios : int
        Number of Monte Carlo scenarios.
    random_state : int, optional
        Seed for reproducibility.

    Returns
    -------
    np.ndarray
        Default times of shape (n_scenarios, n_names).
    """
    rng = np.random.default_rng(random_state)
    lam = np.asarray(lam, dtype=float)

    if lam.ndim == 0:
        lam = lam[None]  # make it 1D

    n_names = lam.shape[0]

    # Use inverse transform: τ = -ln(U) / λ
    U = rng.uniform(size=(n_scenarios, n_names))
    tau = -np.log(U) / lam
    return tau


def pd_constant_intensity(lam: float, T: float) -> float:
    """
    Closed-form default probability under constant intensity.

    PD(T) = 1 - exp(-λ T).

    Parameters
    ----------
    lam : float
        Hazard rate.
    T : float
        Horizon (years).

    Returns
    -------
    float
        Default probability over [0, T].
    """
    return 1.0 - np.exp(-lam * T)
