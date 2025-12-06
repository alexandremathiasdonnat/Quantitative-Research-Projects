# src/tridiagonal.py
import numpy as np


def solve_tridiagonal(
    lower: np.ndarray,
    diag: np.ndarray,
    upper: np.ndarray,
    rhs: np.ndarray,
) -> np.ndarray:
    """
    Solve a tridiagonal system Ax = rhs using Thomas algorithm.

    A has:
        - lower diag (length N-1)
        - main diag  (length N)
        - upper diag (length N-1)
    """
    N = len(diag)

    # Copy to avoid modifying inputs
    a = lower.astype(float).copy()
    b = diag.astype(float).copy()
    c = upper.astype(float).copy()
    d = rhs.astype(float).copy()

    # Forward elimination
    for i in range(1, N):
        w = a[i - 1] / b[i - 1]
        b[i] = b[i] - w * c[i - 1]
        d[i] = d[i] - w * d[i - 1]

    # Backward substitution
    x = np.zeros(N)
    x[-1] = d[-1] / b[-1]
    for i in range(N - 2, -1, -1):
        x[i] = (d[i] - c[i] * x[i + 1]) / b[i]

    return x
