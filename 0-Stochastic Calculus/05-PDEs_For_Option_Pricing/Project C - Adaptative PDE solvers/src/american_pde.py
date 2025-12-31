# src/american_pde.py
import numpy as np

from .tridiagonal import solve_tridiagonal
from .grid import TimeSpaceGrid


def solve_american_put_bs_log_theta(
    grid: TimeSpaceGrid,
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    payoff_T: np.ndarray,
    theta: float = 1.0,
) -> np.ndarray:
    """
    American put in BS log-space via θ-scheme + projection (Brennan–Schwartz style).

    PDE (inequality):
        v_t + L v ≤ 0,  v ≥ payoff,  (v - payoff)(v_t + L v) = 0

    On discretise comme pour l'européenne, puis à chaque pas de temps:
        - on résout le système linéaire
        - on projette : v^n_i = max(v^n_i, payoff_i)
    """
    M = grid.M
    N = grid.N
    k = grid.k

    u = np.zeros((M + 1, N + 2), dtype=float)

    # terminal condition = payoff at T
    u[-1, :] = payoff_T.copy()

    # (I - k θ L_h)
    main_diag = 1.0 - k * theta * b
    lower_diag = -k * theta * a[1:]
    upper_diag = -k * theta * c[:-1]

    payoff = payoff_T.copy()

    for n in range(M - 1, -1, -1):
        u_next = u[n + 1, :].copy()

        # L_h u^{n+1}
        Lu_next = (
            a * u_next[:-2] +
            b * u_next[1:-1] +
            c * u_next[2:]
        )

        rhs = u_next[1:-1] + k * (1.0 - theta) * Lu_next

        # Solve linear system on interior nodes
        u[n, 1:-1] = solve_tridiagonal(
            lower_diag,
            main_diag,
            upper_diag,
            rhs
        )

        # Dirichlet 0 aux bords
        u[n, 0] = 0.0
        u[n, -1] = 0.0

        # Projection American : pas d'arbitrage, valeur ≥ payoff immédiat
        u[n, :] = np.maximum(u[n, :], payoff)

    return u
