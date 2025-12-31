"""
simulation.py

Path simulation for jump–diffusion processes (Merton and Kou).

We simulate in log-space:

    d log S_t = (r - q - 0.5 σ^2 - λ (E[e^Y]-1)) dt
                + σ dW_t + sum_{jumps} Y_k.

Inputs (model parameters, number of paths, steps) are all provided
by the notebook as floats/ints; there is no file loading here.
"""

from __future__ import annotations

import numpy as np
from typing import Literal, Dict, Any

from .jump_models import MertonJumpModel, KouJumpModel


ModelType = Literal["BlackScholes", "Merton", "Kou"]


def _simulate_merton_increment(
    lam: float,
    dt: float,
    mu_J: float,
    sigma_J: float,
    rng: np.random.Generator,
    size: int,
) -> np.ndarray:
    """Generate jump increments sum Y_k over one time-step for Merton model.

    N ~ Poisson(lam dt), Y_k ~ N(mu_J, sigma_J^2).
    sum_jumps = sum_{k=1}^N Y_k.

    We vectorize over 'size' independent paths.
    """
    # Number of jumps per path
    N_jumps = rng.poisson(lam * dt, size=size)
    increments = np.zeros(size, dtype=float)

    # For efficiency, draw all needed jumps at once
    total_jumps = int(N_jumps.sum())
    if total_jumps > 0:
        Y_all = rng.normal(loc=mu_J, scale=sigma_J, size=total_jumps)
        idx = 0
        for i, n in enumerate(N_jumps):
            if n > 0:
                increments[i] = Y_all[idx : idx + n].sum()
                idx += n
    return increments


def _simulate_kou_increment(
    lam: float,
    dt: float,
    p: float,
    eta1: float,
    eta2: float,
    rng: np.random.Generator,
    size: int,
) -> np.ndarray:
    """Generate jump increments sum Y_k over one time-step for Kou model."""
    N_jumps = rng.poisson(lam * dt, size=size)
    increments = np.zeros(size, dtype=float)

    total_jumps = int(N_jumps.sum())
    if total_jumps > 0:
        # For each jump: decide sign, then exponential magnitude
        U = rng.uniform(size=total_jumps)
        is_up = U < p

        # Magnitudes
        # Up: Y ~ Exp(eta1) on y>0; we need density ~ eta1 exp(-eta1 y).
        Y_up = rng.exponential(scale=1.0 / eta1, size=total_jumps)
        Y_down = -rng.exponential(scale=1.0 / eta2, size=total_jumps)

        Y_all = np.where(is_up, Y_up, Y_down)

        idx = 0
        for i, n in enumerate(N_jumps):
            if n > 0:
                increments[i] = Y_all[idx : idx + n].sum()
                idx += n
    return increments


def simulate_jump_diffusion_paths(
    model: ModelType,
    S0: float,
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
    n_paths: int = 1000,
    n_steps: int = 252,
    seed: int | None = None,
) -> Dict[str, Any]:
    """Simulate jump–diffusion paths for the underlying S_t.

    All parameters are passed directly from the notebook.

    Returns a dict with:
        "t_grid": shape (n_steps+1,)
        "paths": shape (n_paths, n_steps+1)
    """
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    t_grid = np.linspace(0.0, T, n_steps + 1)

    paths = np.zeros((n_paths, n_steps + 1), dtype=float)
    paths[:, 0] = S0

    if model == "BlackScholes":
        lam_eff = 0.0
        exp_jump_E = 1.0
    elif model == "Merton":
        if mu_J is None or sigma_J is None:
            raise ValueError("Merton model requires mu_J and sigma_J.")
        lam_eff = lam
        # E[e^Y] = exp(mu_J + 0.5 sigma_J^2)
        exp_jump_E = float(np.exp(mu_J + 0.5 * sigma_J ** 2))
    elif model == "Kou":
        if p is None or eta1 is None or eta2 is None:
            raise ValueError("Kou model requires p, eta1, eta2.")
        lam_eff = lam
        # E[e^Y] = p * eta1 / (eta1 - 1) + (1-p) * eta2 / (eta2 + 1)
        if eta1 <= 1.0:
            raise ValueError("Kou model requires eta1 > 1 for E[e^Y].")
        exp_jump_E = p * eta1 / (eta1 - 1.0) + (1.0 - p) * eta2 / (eta2 + 1.0)
    else:
        raise ValueError(f"Unknown model: {model}")

    # Risk-neutral drift in log-space
    drift_log = (r - q - 0.5 * sigma ** 2 - lam_eff * (exp_jump_E - 1.0))

    for n in range(n_steps):
        # Brownian increment
        dW = np.sqrt(dt) * rng.standard_normal(size=n_paths)

        if model == "BlackScholes":
            jump_increments = np.zeros(n_paths)
        elif model == "Merton":
            jump_increments = _simulate_merton_increment(
                lam=lam_eff,
                dt=dt,
                mu_J=mu_J,
                sigma_J=sigma_J,
                rng=rng,
                size=n_paths,
            )
        else:  # Kou
            jump_increments = _simulate_kou_increment(
                lam=lam_eff,
                dt=dt,
                p=p,
                eta1=eta1,
                eta2=eta2,
                rng=rng,
                size=n_paths,
            )

        log_S_prev = np.log(paths[:, n])
        log_S_next = log_S_prev + drift_log * dt + sigma * dW + jump_increments
        paths[:, n + 1] = np.exp(log_S_next)

    return {"t_grid": t_grid, "paths": paths, "model": model}
