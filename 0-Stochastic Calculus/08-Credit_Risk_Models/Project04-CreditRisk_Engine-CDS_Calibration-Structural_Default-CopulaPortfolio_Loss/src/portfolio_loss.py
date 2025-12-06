"""
Portfolio loss computation given default times.

We take:
    - Exposures at default (EAD_i),
    - Recoveries (R_i),
    - Maturities T_i,
    - Simulated default times τ_i,

and compute the loss in each scenario:
    L = sum_i EAD_i * (1 - R_i) * 1{τ_i < T_i}.

We can then derive VaR and Expected Shortfall (ES).

INPUT PROVENANCE
----------------
In the notebook:
    - Portfolio data (names, EAD, recovery, maturity) will typically be
      stored in a pandas DataFrame, either:
        * built manually in the notebook, or
        * loaded from a CSV file.

The DataFrame is then converted to numpy arrays and passed to this module.
"""

from typing import Tuple

import numpy as np


def compute_losses(
    tau: np.ndarray,
    ead: np.ndarray,
    recovery: np.ndarray,
    maturity: np.ndarray,
) -> np.ndarray:
    """
    Compute portfolio losses for each scenario.

    Parameters
    ----------
    tau : np.ndarray
        Default times, shape (n_scenarios, n_names).
    ead : np.ndarray
        Exposures at default EAD_i, shape (n_names,).
    recovery : np.ndarray
        Recoveries R_i, shape (n_names,).
    maturity : np.ndarray
        Maturities T_i (in years), shape (n_names,).

    Returns
    -------
    np.ndarray
        Losses per scenario, shape (n_scenarios,).
    """
    tau = np.asarray(tau, dtype=float)
    ead = np.asarray(ead, dtype=float)
    recovery = np.asarray(recovery, dtype=float)
    maturity = np.asarray(maturity, dtype=float)

    if ead.ndim != 1 or recovery.ndim != 1 or maturity.ndim != 1:
        raise ValueError("ead, recovery, maturity must be 1D arrays.")

    n_scenarios, n_names = tau.shape
    if any(arr.shape[0] != n_names for arr in (ead, recovery, maturity)):
        raise ValueError("Number of names in tau and portfolio vectors must match.")

    # Indicator of default before maturity, shape (n_scenarios, n_names)
    default_indicator = tau < maturity.reshape(1, -1)

    loss_per_name = ead.reshape(1, -1) * (1.0 - recovery.reshape(1, -1)) * default_indicator
    losses = loss_per_name.sum(axis=1)
    return losses


def var_es(
    losses: np.ndarray,
    alpha_var: float = 0.99,
    alpha_es: float = 0.975,
) -> Tuple[float, float]:
    """
    Compute Value-at-Risk (VaR) and Expected Shortfall (ES)
    from an array of simulated losses.

    Parameters
    ----------
    losses : np.ndarray
        Losses per scenario, shape (n_scenarios,).
    alpha_var : float
        Confidence level for VaR (e.g. 0.99).
    alpha_es : float
        Confidence level for ES (e.g. 0.975).

    Returns
    -------
    var_value : float
        VaR at level alpha_var.
    es_value : float
        ES at level alpha_es.
    """
    losses = np.asarray(losses, dtype=float)
    if losses.ndim != 1:
        raise ValueError("losses must be a 1D array.")

    sorted_losses = np.sort(losses)

    # VaR
    idx_var = int(np.floor(alpha_var * len(sorted_losses))) - 1
    idx_var = max(0, min(idx_var, len(sorted_losses) - 1))
    var_value = sorted_losses[idx_var]

    # ES: mean of losses beyond VaR at alpha_es
    idx_es = int(np.floor(alpha_es * len(sorted_losses)))
    idx_es = max(1, min(idx_es, len(sorted_losses)))
    es_value = sorted_losses[idx_es:].mean()

    return var_value, es_value
