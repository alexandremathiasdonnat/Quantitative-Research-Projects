# src/operators.py
import numpy as np

from .grid import TimeSpaceGrid


def bs_log_operator_tridiag(
    grid: TimeSpaceGrid,
    r: float,
    sigma: float,
):
    """
    Build the tridiagonal coefficients (a, b, c) of the spatial operator L_h
    for Black–Scholes in log-space:

        L = (σ²/2) ∂²/∂x² + (r - σ²/2) ∂/∂x - r

    Discretisation (central differences) on the interior nodes 1..N:
        (L_h u)_i = a_i u_{i-1} + b_i u_i + c_i u_{i+1}
    """
    N = grid.N
    h = grid.h

    a = np.zeros(N)
    b = np.zeros(N)
    c = np.zeros(N)

    sigma2 = sigma ** 2

    # Coeffs in front of u_{i-1}, u_i, u_{i+1}
    # cf. what we had derived: σ²/(2h²), r - σ²/2 over 2h, etc.
    for i in range(N):
        a[i] = sigma2 / (2 * h**2) - (r - sigma2 / 2) / (2 * h)
        b[i] = - sigma2 / (h**2) - r
        c[i] = sigma2 / (2 * h**2) + (r - sigma2 / 2) / (2 * h)

    return a, b, c
