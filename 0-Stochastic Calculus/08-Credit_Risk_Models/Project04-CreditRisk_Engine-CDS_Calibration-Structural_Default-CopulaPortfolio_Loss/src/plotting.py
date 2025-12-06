"""
Standard plotting utilities for the Credit Risk Engine.

This module centralizes Matplotlib visualizations:

    - Distance-to-default and PD comparison (structural vs CDS),
    - Histogram of simulated asset values,
    - Distribution of portfolio losses,
    - VaR markers and tail visualization.

INPUT PROVENANCE
----------------
The notebook:
    - calls computational functions from `credit_api`,
    - then passes the resulting arrays (losses, tau, VT, etc.) to
      the plotting functions here.

No data loading occurs in this module.
"""

from typing import Optional

import numpy as np
import matplotlib.pyplot as plt


def plot_asset_distribution(
    VT: np.ndarray,
    D: float,
    title: str = "Terminal Asset Value Distribution",
) -> None:
    """
    Plot the histogram of simulated terminal asset values.

    Parameters
    ----------
    VT : np.ndarray
        Simulated terminal asset values (e.g. from structural_model).
    D : float
        Debt face value (default barrier).
    title : str
        Figure title.
    """
    VT = np.asarray(VT, dtype=float)

    plt.figure()
    plt.hist(VT, bins=50, alpha=0.7, density=True)
    plt.axvline(D, linestyle="--", label="Debt face value D")
    plt.xlabel("V_T")
    plt.ylabel("Density")
    plt.title(title)
    plt.legend()
    plt.tight_layout()


def plot_pd_comparison(
    maturities: np.ndarray,
    pd_structural: np.ndarray,
    pd_cds: np.ndarray,
    title: str = "Default Probability: Structural vs CDS-implied",
) -> None:
    """
    Plot structural vs CDS-implied default probabilities over maturities.

    Parameters
    ----------
    maturities : np.ndarray
        Maturity grid (years), shape (n_points,).
    pd_structural : np.ndarray
        Structural PDs, shape (n_points,).
    pd_cds : np.ndarray
        CDS-implied PDs, shape (n_points,).
    title : str
        Figure title.
    """
    maturities = np.asarray(maturities, dtype=float)
    pd_structural = np.asarray(pd_structural, dtype=float)
    pd_cds = np.asarray(pd_cds, dtype=float)

    plt.figure()
    plt.plot(maturities, pd_structural, marker="o", label="Structural PD")
    plt.plot(maturities, pd_cds, marker="x", label="CDS-implied PD")
    plt.xlabel("Maturity (years)")
    plt.ylabel("Default probability")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()


def plot_loss_distribution(
    losses: np.ndarray,
    var_level: float = 0.99,
    es_level: float = 0.975,
    var_value: Optional[float] = None,
    es_value: Optional[float] = None,
    title: str = "Portfolio Loss Distribution",
) -> None:
    """
    Plot the distribution of portfolio losses and optionally mark VaR/ES.

    Parameters
    ----------
    losses : np.ndarray
        Losses per scenario.
    var_level : float
        VaR confidence level.
    es_level : float
        ES confidence level.
    var_value : float, optional
        Precomputed VaR value. If None, it will be computed on the fly.
    es_value : float, optional
        Precomputed ES value. If None, it will be approximated on the fly.
    title : str
        Figure title.
    """
    losses = np.asarray(losses, dtype=float)
    sorted_losses = np.sort(losses)

    if var_value is None:
        idx_var = int(np.floor(var_level * len(sorted_losses))) - 1
        idx_var = max(0, min(idx_var, len(sorted_losses) - 1))
        var_value = sorted_losses[idx_var]

    if es_value is None:
        idx_es = int(np.floor(es_level * len(sorted_losses)))
        idx_es = max(1, min(idx_es, len(sorted_losses)))
        es_value = sorted_losses[idx_es:].mean()

    plt.figure()
    plt.hist(losses, bins=50, density=True, alpha=0.7)
    plt.axvline(var_value, linestyle="--", label=f"VaR {int(var_level*100)}%")
    plt.axvline(es_value, linestyle=":", label=f"ES {int(es_level*100)}%")
    plt.xlabel("Loss")
    plt.ylabel("Density")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
