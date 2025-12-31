"""
pide_operator.py

Build the full generator matrix L for the PIDE:

    ∂u/∂t = L u,

where L contains:
- diffusion part: 0.5 σ^2 S^2 u_SS
- drift part: μ̃ S u_S - r u
- jump integral: λ ∫ (u(Se^y) - u(S)) f_Y(y) dy

All scalars (r, q, sigma, lambda, etc.) are passed from the notebook
via pricing_api; no file I/O occurs here.
"""

from __future__ import annotations

import numpy as np

from .integral_terms import build_jump_integral_matrix
from .jump_models import JumpModel, adjusted_risk_neutral_drift


def build_diffusion_tridiagonal(
    S_grid: np.ndarray,
    r: float,
    q: float,
    sigma: float,
    mu_tilde: float,
) -> np.ndarray:
    """Build diffusion+drift+discount operator on a price grid.

    We discretize in S with standard second-order central differences.

    L_diff u_i ≈ 0.5 σ^2 S_i^2 u_SS + μ̃ S_i u_S - r u_i.

    Parameters
    ----------
    S_grid : np.ndarray, shape (N,)
        Price grid.
    r, q, sigma, mu_tilde : float
        Model parameters; mu_tilde is the risk-neutral drift
        for the diffusion part, computed in jump_models.

    Returns
    -------
    L_diff : np.ndarray, shape (N, N)
        Tridiagonal-ish dense matrix for diffusion + drift + discount.
    """
    S_grid = np.asarray(S_grid, dtype=float)
    N = S_grid.size
    L = np.zeros((N, N), dtype=float)

    # Use non-uniform grid formulas in general; but here S_grid is log-uniform.
    # We still use generic finite differences based on neighbouring distances.
    for i in range(1, N - 1):
        S_i = S_grid[i]
        S_im1 = S_grid[i - 1]
        S_ip1 = S_grid[i + 1]

        h_im1 = S_i - S_im1
        h_i = S_ip1 - S_i

        # second derivative u_SS at S_i
        # generic second-order formula on non-uniform grid
        a = 2.0 / (h_im1 * (h_im1 + h_i))
        b = -2.0 / (h_im1 * h_i)
        c = 2.0 / (h_i * (h_im1 + h_i))

        # first derivative u_S at S_i (central)
        d = -h_i / (h_im1 * (h_im1 + h_i))
        e = (h_i - h_im1) / (h_im1 * h_i)
        f = h_im1 / (h_i * (h_im1 + h_i))

        # combine into L u_i = 0.5 σ^2 S_i^2 u_SS + μ̃ S_i u_S - r u_i
        L[i, i - 1] += 0.5 * sigma ** 2 * S_i ** 2 * a + mu_tilde * S_i * d
        L[i, i] += 0.5 * sigma ** 2 * S_i ** 2 * b + mu_tilde * S_i * e - r
        L[i, i + 1] += 0.5 * sigma ** 2 * S_i ** 2 * c + mu_tilde * S_i * f

    # Boundaries: simple Dirichlet-type operator; real boundary conditions
    # will be imposed in the solver by forcing u[0], u[-1].
    L[0, 0] = -r
    L[-1, -1] = -r

    return L


def build_generator_matrix(
    S_grid: np.ndarray,
    r: float,
    q: float,
    sigma: float,
    lam: float,
    jump_model: JumpModel | None,
    y_min: float = -1.0,
    y_max: float = 1.0,
    Ny: int = 201,
) -> np.ndarray:
    """Build full generator matrix L = L_diff + L_jump.

    Parameters
    ----------
    S_grid : np.ndarray, shape (N,)
        Price grid.
    r, q, sigma : float
        Standard diffusive Black–Scholes parameters.
    lam : float
        Jump intensity λ. If lam == 0, we return the pure BS operator.
    jump_model : JumpModel or None
        Jump size distribution. If None, pure Black–Scholes is used.
    y_min, y_max : float
        Truncation bounds for jump sizes.
    Ny : int
        Number of quadrature points for jump integral.

    Returns
    -------
    L : np.ndarray, shape (N, N)
        Generator matrix for the PIDE.
    """
    if lam < 0:
        raise ValueError("Jump intensity λ must be non-negative.")

    if lam == 0.0 or jump_model is None:
        # Pure Black–Scholes generator
        mu_tilde = r - q
        L_diff = build_diffusion_tridiagonal(S_grid, r, q, sigma, mu_tilde)
        return L_diff

    # Drift adjusted for presence of jumps
    mu_tilde = adjusted_risk_neutral_drift(r, q, lam, jump_model)

    L_diff = build_diffusion_tridiagonal(S_grid, r, q, sigma, mu_tilde)
    L_jump = build_jump_integral_matrix(
        S_grid=S_grid,
        lam=lam,
        jump_model=jump_model,
        y_min=y_min,
        y_max=y_max,
        Ny=Ny,
    )

    return L_diff + L_jump
