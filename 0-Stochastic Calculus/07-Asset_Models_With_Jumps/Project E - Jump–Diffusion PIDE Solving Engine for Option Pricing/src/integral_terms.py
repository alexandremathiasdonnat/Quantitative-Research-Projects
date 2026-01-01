"""
integral_terms.py

Discretisation of the jump integral term in the PIDE:

    I_jump u(s) = λ ∫ [u(se^y) - u(s)] f_Y(y) dy

We work on a LOG-UNIFORM price grid:

    S_i = S_min * exp(i * dlogS),   i = 0, ..., N-1

This makes the mapping s -> s * e^y a simple shift in log-space,
so we can build a dense matrix J such that:

    (J @ u)_i ≈ I_jump u(S_i).

Inputs (lambda, jump_model, grid bounds) come from the dashboard notebook.
"""

from __future__ import annotations

import numpy as np
from typing import Tuple

from .jump_models import JumpModel


def build_jump_integral_matrix(
    S_grid: np.ndarray,
    lam: float,
    jump_model: JumpModel,
    y_min: float = -1.0,
    y_max: float = 1.0,
    Ny: int = 201,
) -> np.ndarray:
    """Build dense matrix J approximating the jump integral operator.

    Parameters
    ----------
    S_grid : np.ndarray, shape (N,)
        Log-uniform grid of underlying prices.
    lam : float
        Jump intensity λ.
    jump_model : JumpModel
        MertonJumpModel or KouJumpModel instance.
    y_min, y_max : float
        Truncation range for jump sizes Y. Integrals outside are ignored.
        In practice, we choose a range large enough to capture most
        of the distribution mass (e.g. ±5 * sigma_J for Merton).
    Ny : int
        Number of quadrature points in [y_min, y_max].

    Returns
    -------
    J : np.ndarray, shape (N, N)
        Dense matrix such that (J @ u)_i approximates λ ∫(u(S_i e^y) - u(S_i)) f_Y(y) dy.

    Notes
    -----
    - This is O(N^2) to build and O(N^2) to apply, which is fine for small N (~200–400).
    - The grid MUST be log-uniform: log(S_{i+1}) - log(S_i) constant.
      We do not enforce it programmatically here;
      when building S_grid in the notebook or in the solver.
    """
    S_grid = np.asarray(S_grid, dtype=float)
    N = S_grid.size

    logS = np.log(S_grid)
    dlogS = logS[1] - logS[0]

    # Quadrature nodes in y
    y_nodes = np.linspace(y_min, y_max, Ny)
    dy = y_nodes[1] - y_nodes[0]

    pdf_vals = jump_model.pdf(y_nodes)

    # Preallocate integral matrix
    J = np.zeros((N, N), dtype=float)

    # For each state i, approximate integral using interpolation on the grid
    for i in range(N):
        # log of s * e^y = logS[i] + y
        logS_targets = logS[i] + y_nodes
        # Corresponding fractional indices on the log-uniform grid
        idx_float = (logS_targets - logS[0]) / dlogS

        # Linear interpolation between floor and ceil indices
        idx_floor = np.floor(idx_float).astype(int)
        idx_ceil = idx_floor + 1
        w_ceil = idx_float - idx_floor
        w_floor = 1.0 - w_ceil

        # Clamp indices to be inside [0, N-1]
        idx_floor_clipped = np.clip(idx_floor, 0, N - 1)
        idx_ceil_clipped = np.clip(idx_ceil, 0, N - 1)

        # Build "row" weights on u-vector for u(se^y)
        row_weights = np.zeros(N, dtype=float)
        # accumulate contributions from all y_nodes
        for k in range(Ny):
            j_f = idx_floor_clipped[k]
            j_c = idx_ceil_clipped[k]
            w_f = w_floor[k]
            w_c = w_ceil[k]

            weight = lam * pdf_vals[k] * dy  # global prefactor for this y_k

            if 0 <= j_f < N:
                row_weights[j_f] += weight * w_f
            if 0 <= j_c < N:
                row_weights[j_c] += weight * w_c

        # Now (row_weights @ u) approximates λ ∫ u(s e^y) f_Y(y) dy
        # We still need to subtract λ * u(s) * ∫f_Y(y) dy.
        integral_pdf = lam * np.sum(pdf_vals * dy)
        # Fill row i of J: u -> λ ∫u(se^y)f_Y(y)dy - λ u(s) ∫f_Y(y)dy
        J[i, :] = row_weights
        J[i, i] -= integral_pdf

    return J
