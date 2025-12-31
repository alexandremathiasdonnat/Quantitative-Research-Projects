"""
Copula-based simulation of correlated default times.

We consider:
    - Gaussian copula
    - t-copula (with ν degrees of freedom)

Given:
    - marginal intensities λ_i (constant per name),
    - a correlation matrix for the copula,
we generate correlated U(0,1) uniforms and transform them into
exponential default times via inverse CDF.

INPUT PROVENANCE
----------------
In the notebook, the user typically provides:
    - λ vector:
        - manually,
        - or inferred from CDS calibration for each name.
    - correlation matrix:
        - hard-coded in the notebook for small portfolios, or
        - read from a CSV correlation matrix (pandas).

This module only deals with numpy arrays, not data files.
"""

from typing import Literal, Optional

import numpy as np
from scipy.stats import norm, t as student_t, chi2


def _check_correlation_matrix(corr: np.ndarray) -> np.ndarray:
    """
    Validate and slightly symmetrize the correlation matrix.

    Parameters
    ----------
    corr : np.ndarray
        Square correlation matrix.

    Returns
    -------
    np.ndarray
        Symmetric, positive semi-definite matrix (assumed).
    """
    corr = np.asarray(corr, dtype=float)
    if corr.shape[0] != corr.shape[1]:
        raise ValueError("Correlation matrix must be square.")

    # Symmetrize
    corr = 0.5 * (corr + corr.T)

    # Basic checks
    if not np.allclose(np.diag(corr), 1.0, atol=1e-6):
        raise ValueError("Correlation matrix must have ones on the diagonal.")

    return corr


def gaussian_copula_uniforms(
    corr: np.ndarray,
    n_scenarios: int,
    random_state: Optional[int] = None,
) -> np.ndarray:
    """
    Generate correlated uniforms via Gaussian copula.

    Steps:
        1. Generate Z ~ N(0, Σ) using Cholesky factor.
        2. Map each component through Φ to obtain U in (0,1).

    Parameters
    ----------
    corr : np.ndarray
        Correlation matrix Σ, shape (n_names, n_names).
    n_scenarios : int
        Number of Monte Carlo scenarios.
    random_state : int, optional
        Seed.

    Returns
    -------
    np.ndarray
        Uniform samples of shape (n_scenarios, n_names).
    """
    rng = np.random.default_rng(random_state)
    corr = _check_correlation_matrix(corr)
    n = corr.shape[0]

    L = np.linalg.cholesky(corr)  # lower-triangular
    Z = rng.normal(size=(n_scenarios, n))
    Y = Z @ L.T  # correlated Gaussian
    U = norm.cdf(Y)
    return U


def t_copula_uniforms(
    corr: np.ndarray,
    df: int,
    n_scenarios: int,
    random_state: Optional[int] = None,
) -> np.ndarray:
    """
    Generate correlated uniforms via t-copula.

    Construction:
        - Draw Z ~ N(0, Σ) with correlation matrix Σ.
        - Draw s ~ χ²_ν independently.
        - Define T = Z / sqrt(s / ν), which has multivariate t dist.
        - Map each component through univariate t CDF T_ν to get U.

    Parameters
    ----------
    corr : np.ndarray
        Correlation matrix Σ.
    df : int
        Degrees of freedom ν (> 2 typically).
    n_scenarios : int
        Number of scenarios.
    random_state : int, optional

    Returns
    -------
    np.ndarray
        Uniform samples of shape (n_scenarios, n_names).
    """
    if df <= 2:
        raise ValueError("Degrees of freedom df should be > 2 for a stable t-copula.")

    rng = np.random.default_rng(random_state)
    corr = _check_correlation_matrix(corr)
    n = corr.shape[0]

    L = np.linalg.cholesky(corr)
    Z = rng.normal(size=(n_scenarios, n))
    Y = Z @ L.T

    s = chi2.rvs(df, size=n_scenarios, random_state=rng)
    scale = np.sqrt(s / df).reshape(-1, 1)  # shape (n_scenarios, 1)
    T_var = Y / scale

    U = student_t.cdf(T_var, df=df)
    return U


def simulate_default_times_copula(
    lam: np.ndarray,
    corr: np.ndarray,
    copula_type: Literal["gaussian", "t"] = "gaussian",
    df: int = 5,
    n_scenarios: int = 100_000,
    random_state: Optional[int] = None,
) -> np.ndarray:
    """
    Simulate correlated default times using a copula.

    For each name i:
        - Marginal: τ_i ~ Exp(λ_i)
        - Dependence: Gaussian or t-copula with given correlation.

    Inverse CDF:
        τ_i = -ln(1 - U_i) / λ_i   with U_i ~ U(0,1).

    Parameters
    ----------
    lam : np.ndarray
        Hazard rates λ_i, shape (n_names,).
    corr : np.ndarray
        Correlation matrix, shape (n_names, n_names).
    copula_type : {"gaussian", "t"}
        Type of copula.
    df : int
        Degrees of freedom for t-copula.
    n_scenarios : int
        Number of Monte Carlo scenarios.
    random_state : int, optional

    Returns
    -------
    np.ndarray
        Default times τ of shape (n_scenarios, n_names).
    """
    lam = np.asarray(lam, dtype=float)
    if lam.ndim != 1:
        raise ValueError("lam must be a 1D array of hazard rates.")
    n_names = lam.shape[0]

    if copula_type == "gaussian":
        U = gaussian_copula_uniforms(corr, n_scenarios, random_state)
    elif copula_type == "t":
        U = t_copula_uniforms(corr, df, n_scenarios, random_state)
    else:
        raise ValueError("copula_type must be 'gaussian' or 't'.")

    if U.shape[1] != n_names:
        raise ValueError("Correlation matrix dimension does not match lam length.")

    # Inverse exponential CDF: F^{-1}(u) = -ln(1 - u) / λ
    # Clip U to avoid log(0).
    eps = 1e-12
    U_clipped = np.clip(U, eps, 1.0 - eps)
    tau = -np.log(1.0 - U_clipped) / lam
    return tau
