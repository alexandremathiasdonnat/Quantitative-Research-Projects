"""
pide_solver.py

Crank–Nicolson (θ-scheme) solver for the PIDE in log-uniform S.

We solve in "time to maturity" τ ∈ [0, T]:

    ∂u/∂τ = L u,     u(0, S) = payoff(S).

Backward-in-calendar-time is equivalent; this forward-τ formulation
is numerically simpler.

All parameters (T, K, r, q, sigma, lambda, model type, grid settings)
are provided directly by the notebook through pricing_api.
No file I/O here.
"""

from __future__ import annotations

import numpy as np
from typing import Literal, Dict, Any

from .jump_models import MertonJumpModel, KouJumpModel
from .pide_operator import build_generator_matrix


ModelType = Literal["BlackScholes", "Merton", "Kou"]


def build_log_uniform_grid(S_min: float, S_max: float, NS: int) -> np.ndarray:
    """Build log-uniform grid on [S_min, S_max]."""
    log_min, log_max = np.log(S_min), np.log(S_max)
    return np.exp(np.linspace(log_min, log_max, NS))


def european_call_payoff(S: np.ndarray, K: float) -> np.ndarray:
    """Vanilla European call payoff max(S-K, 0)."""
    return np.maximum(S - K, 0.0)


def apply_call_boundary_conditions(
    u: np.ndarray,
    S_grid: np.ndarray,
    K: float,
    r: float,
    tau: float,
) -> np.ndarray:
    """Enforce Dirichlet boundary conditions for a call.

    At S ~ 0: call ≈ 0
    At S large: call ≈ S - K e^{-r τ}

    Parameters
    ----------
    u : np.ndarray, shape (N,)
        Current solution at time τ.
    S_grid : np.ndarray, shape (N,)
        Price grid.
    K, r, tau : float
        Strike, risk-free rate, current time to maturity.

    Returns
    -------
    u_bc : np.ndarray
        Solution with boundaries overwritten.
    """
    u[0] = 0.0
    u[-1] = S_grid[-1] - K * np.exp(-r * tau)
    return u


def solve_pide_european_call(
    model: ModelType,
    S0: float,
    K: float,
    T: float,
    r: float,
    q: float,
    sigma: float,
    lam: float = 0.0,
    mu_J: float | None = None,
    sigma_J: float | None = None,
    p: float | None = None,
    eta1: float | None = None,
    eta2: float | None = None,
    S_min: float | None = None,
    S_max: float | None = None,
    NS: int = 200,
    NT: int = 200,
    theta: float = 0.5,
    y_min: float = -1.0,
    y_max: float = 1.0,
    Ny: int = 201,
) -> Dict[str, Any]:
    """Solve PIDE for a European call using a θ-scheme (Crank–Nicolson).

    Parameters
    ----------
    model : {"BlackScholes", "Merton", "Kou"}
        Model type.
    S0, K, T, r, q, sigma : float
        Standard market and diffusion parameters.
    lam : float, optional
        Jump intensity λ. Ignored for BlackScholes.
    mu_J, sigma_J : float, optional
        Merton jump parameters (mean, std of normal jump).
    p, eta1, eta2 : float, optional
        Kou jump parameters.
    S_min, S_max : float, optional
        Price grid bounds. If None, set from S0 and K.
    NS, NT : int
        Number of grid points in S and in time (τ).
    theta : float
        θ in θ-scheme. 0.5 = Crank–Nicolson.
    y_min, y_max, Ny
        Jump-size integration bounds and resolution.

    Returns
    -------
    result : dict
        {
            "S_grid": np.ndarray, shape (NS,),
            "tau_grid": np.ndarray, shape (NT+1,),
            "U": np.ndarray, shape (NT+1, NS),  # U[n, i] = price at tau_n, S_i
            "price_S0": float,
            "model": str
        }
    """
    if S_min is None:
        S_min = max(1e-6, 0.1 * min(S0, K))
    if S_max is None:
        S_max = 4.0 * max(S0, K)

    # Build price grid (log-uniform)
    S_grid = build_log_uniform_grid(S_min, S_max, NS)

    # Time grid in τ (0 = now, T = maturity)
    tau_grid = np.linspace(0.0, T, NT + 1)
    dt = tau_grid[1] - tau_grid[0]

    # Terminal condition at τ = 0 (payoff)
    U = np.zeros((NT + 1, NS), dtype=float)
    U[0, :] = european_call_payoff(S_grid, K)

    # Choose jump model if needed
    jump_model = None
    if model == "Merton":
        if mu_J is None or sigma_J is None:
            raise ValueError("Merton model requires mu_J and sigma_J.")
        from .jump_models import MertonJumpModel

        jump_model = MertonJumpModel(mu_J=mu_J, sigma_J=sigma_J)
    elif model == "Kou":
        if p is None or eta1 is None or eta2 is None:
            raise ValueError("Kou model requires p, eta1, eta2.")
        from .jump_models import KouJumpModel

        jump_model = KouJumpModel(p=p, eta1=eta1, eta2=eta2)
    elif model == "BlackScholes":
        lam = 0.0
        jump_model = None
    else:
        raise ValueError(f"Unknown model: {model}")

    # Build generator matrix L (constant in time)
    L = build_generator_matrix(
        S_grid=S_grid,
        r=r,
        q=q,
        sigma=sigma,
        lam=lam,
        jump_model=jump_model,
        y_min=y_min,
        y_max=y_max,
        Ny=Ny,
    )

    N = NS
    I = np.eye(N)

    # θ-scheme matrices:
    # U^{n+1} = U^n + dt [θ L U^{n+1} + (1-θ) L U^n]
    # => (I - dt θ L) U^{n+1} = (I + dt (1-θ) L) U^n
    A = I - dt * theta * L
    B = I + dt * (1.0 - theta) * L

    # Impose fixed boundary rows in A and B (Dirichlet)
    # row 0: u_0^{n+1} = boundary_0  => A[0,:]=[1,0,...,0], B[0,:]=0
    A[0, :] = 0.0
    A[0, 0] = 1.0
    B[0, :] = 0.0

    A[-1, :] = 0.0
    A[-1, -1] = 1.0
    B[-1, :] = 0.0

    # Time stepping
    for n in range(0, NT):
        tau_n = tau_grid[n]       # current τ
        tau_np1 = tau_grid[n + 1] # next τ

        u_n = U[n, :].copy()

        # Right-hand side
        rhs = B @ u_n

        # Insert boundary conditions into rhs at n+1
        # Use τ_{n+1} for discount in upper boundary
        rhs[0] = 0.0
        rhs[-1] = S_grid[-1] - K * np.exp(-r * tau_np1)

        # Solve linear system
        u_np1 = np.linalg.solve(A, rhs)
        # Enforce boundary explicitly as safety
        u_np1 = apply_call_boundary_conditions(u_np1, S_grid, K, r, tau_np1)

        U[n + 1, :] = u_np1

    # Find index closest to S0 to read price
    idx_S0 = int(np.round((np.log(S0) - np.log(S_min)) /
                          (np.log(S_max) - np.log(S_min)) * (NS - 1)))
    idx_S0 = max(0, min(NS - 1, idx_S0))
    price_S0 = float(U[-1, idx_S0])

    return {
        "S_grid": S_grid,
        "tau_grid": tau_grid,
        "U": U,
        "price_S0": price_S0,
        "model": model,
    }
