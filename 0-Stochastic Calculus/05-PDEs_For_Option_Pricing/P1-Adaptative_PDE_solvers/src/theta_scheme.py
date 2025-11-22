# src/theta_scheme.py
import numpy as np

from .tridiagonal import solve_tridiagonal
from .grid import TimeSpaceGrid


def solve_european_bs_log_theta(
    grid: TimeSpaceGrid,
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    u_T: np.ndarray,
    theta: float = 0.5,
) -> np.ndarray:
    """
    Solve the European option pricing PDE in log-space with a θ-scheme.

    PDE in log-space:
        v_t + L v = 0,   L = (σ²/2) ∂²_x + (r - σ²/2) ∂_x - r

    Discretisation:
        (u^{n+1} - u^n)/k + θ L_h u^n + (1-θ) L_h u^{n+1} = 0

    Inputs
    ------
    grid  : TimeSpaceGrid
    a,b,c : tridiagonal coeffs of L_h (length N)
    u_T   : payoff at T on the full spatial grid (N+2 points)
    theta : θ in [0,1] (0: explicite, 0.5: CN, 1: implicite)

    Output
    ------
    u : array (M+1, N+2), u[n, i] ≈ u(t_n, x_i)
        n=0 -> t=0, n=M -> t=T
    """
    M = grid.M
    N = grid.N
    k = grid.k

    u = np.zeros((M + 1, N + 2), dtype=float)

    # terminal condition at T
    u[-1, :] = u_T

    # (I - k θ L_h) → diagonales pour les N points intérieurs
    main_diag = 1.0 - k * theta * b
    lower_diag = -k * theta * a[1:]   # size N-1
    upper_diag = -k * theta * c[:-1]  # size N-1

    for n in range(M - 1, -1, -1):
        u_next = u[n + 1, :].copy()

        # L_h u^{n+1} sur les points intérieurs
        Lu_next = (
            a * u_next[:-2] +
            b * u_next[1:-1] +
            c * u_next[2:]
        )

        # RHS = u^{n+1} + k (1-θ) L_h u^{n+1}
        rhs = u_next[1:-1] + k * (1.0 - theta) * Lu_next

        # Solve (I - k θ L_h) u^n = RHS
        u[n, 1:-1] = solve_tridiagonal(
            lower_diag,
            main_diag,
            upper_diag,
            rhs
        )

        # Bords : ici Dirichlet 0 (option “knock-out” si on sort du domaine)
        u[n, 0] = 0.0
        u[n, -1] = 0.0

    return u
