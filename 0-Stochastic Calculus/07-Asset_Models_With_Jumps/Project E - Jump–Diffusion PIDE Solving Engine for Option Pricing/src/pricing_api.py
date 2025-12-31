"""
pricing_api.py

API used by the notebook "dashboard".

This is the ONLY module the notebook has to import to:

- price European options under:
    * Black–Scholes
    * Merton jump–diffusion
    * Kou jump–diffusion
- generate implied vol smiles,
- simulate jump–diffusion paths,
- produce standard plots.

All inputs here are provided MANUALLY in the notebook as Python
variables or dictionaries. This file does not read/write any CSV
or other data sources.
"""

from __future__ import annotations

from typing import Dict, Any, Literal, Sequence

import numpy as np

from .pide_solver import solve_pide_european_call
from .simulation import simulate_jump_diffusion_paths
from .plotting import (
    plot_price_surface,
    plot_implied_vol_smile,
    plot_paths,
    black_scholes_call,
)

ModelType = Literal["BlackScholes", "Merton", "Kou"]


def price_option(
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
    """High-level pricing call for a single European call option.

    The notebook is expected to pass all scalar inputs explicitly.
    No files are involved.

    Returns the full grid solution and price at S0.
    """
    result = solve_pide_european_call(
        model=model,
        S0=S0,
        K=K,
        T=T,
        r=r,
        q=q,
        sigma=sigma,
        lam=lam,
        mu_J=mu_J,
        sigma_J=sigma_J,
        p=p,
        eta1=eta1,
        eta2=eta2,
        S_min=S_min,
        S_max=S_max,
        NS=NS,
        NT=NT,
        theta=theta,
        y_min=y_min,
        y_max=y_max,
        Ny=Ny,
    )
    return result


def simulate_jump_paths(
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
    """High-level wrapper to simulate jump–diffusion paths.

    All parameters are provided in the notebook.
    """
    return simulate_jump_diffusion_paths(
        model=model,
        S0=S0,
        T=T,
        r=r,
        q=q,
        sigma=sigma,
        lam=lam,
        mu_J=mu_J,
        sigma_J=sigma_J,
        p=p,
        eta1=eta1,
        eta2=eta2,
        n_paths=n_paths,
        n_steps=n_steps,
        seed=seed,
    )


def generate_smile(
    model: ModelType,
    S0: float,
    strikes: Sequence[float],
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
    grid_kwargs: Dict[str, Any] | None = None,
    plot: bool = True,
) -> Dict[str, Any]:
    """Generate and (optionally) plot implied vol smile for a set of strikes.

    For each strike, we re-run the PIDE solver with the same grid parameters.

    Parameters
    ----------
    grid_kwargs : dict or None
        Extra arguments for the grid (S_min, S_max, NS, NT, theta, y_min, y_max, Ny).

    Returns
    -------
    result : dict
        {
            "strikes": np.ndarray,
            "prices": np.ndarray,
            "ivols": np.ndarray
        }
    """
    if grid_kwargs is None:
        grid_kwargs = {}

    strikes = np.asarray(strikes, dtype=float)
    prices = np.zeros_like(strikes)

    for i, K in enumerate(strikes):
        res = price_option(
            model=model,
            S0=S0,
            K=K,
            T=T,
            r=r,
            q=q,
            sigma=sigma,
            lam=lam,
            mu_J=mu_J,
            sigma_J=sigma_J,
            p=p,
            eta1=eta1,
            eta2=eta2,
            **grid_kwargs,
        )
        prices[i] = res["price_S0"]

    if plot:
        _, ivols = plot_implied_vol_smile(
            strikes=strikes,
            prices=prices,
            S0=S0,
            T=T,
            r=r,
            q=q,
            label=f"{model} jump model",
        )
    else:
        ivols = np.zeros_like(strikes)

    return {"strikes": strikes, "prices": prices, "ivols": ivols}


def compare_with_black_scholes(
    S0: float,
    strikes: Sequence[float],
    T: float,
    r: float,
    q: float,
    jump_smile: Dict[str, Any],
) -> None:
    """Plot BS flat smile vs jump-model smile."""
    strikes = np.asarray(strikes, dtype=float)
    ivols_jump = np.asarray(jump_smile["ivols"], dtype=float)

    # Compute BS price at reference sigma (ATM implied from one strike,
    # or simply use mean implied vol from jump model).
    sigma_ref = float(np.mean(ivols_jump))

    ivols_bs = np.full_like(strikes, sigma_ref)

    import matplotlib.pyplot as plt

    plt.figure()
    moneyness = strikes / S0
    plt.plot(moneyness, ivols_bs, "--", label="Black–Scholes (flat)")
    plt.plot(moneyness, ivols_jump, "o-", label="Jump model")
    plt.xlabel("K / S0")
    plt.ylabel("Implied vol")
    plt.title("Smile: Black–Scholes vs Jump–Diffusion")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()


def quick_dashboard_example() -> None:
    """Minimal example (for the notebook) showing how to use the API.

    This function is just documentation; we will not call it from the notebook.
    """
    S0 = 100.0
    K = 100.0
    T = 1.0
    r = 0.02
    q = 0.0
    sigma = 0.2

    lam = 1.0
    mu_J = -0.1
    sigma_J = 0.2

    # 1) Price one call under Merton
    res = price_option(
        model="Merton",
        S0=S0,
        K=K,
        T=T,
        r=r,
        q=q,
        sigma=sigma,
        lam=lam,
        mu_J=mu_J,
        sigma_J=sigma_J,
        NS=200,
        NT=200,
    )
    print("Merton PIDE price at S0 =", res["price_S0"])

    # 2) Plot price surface
    plot_price_surface(res["S_grid"], res["tau_grid"], res["U"])

    # 3) Generate smile
    strikes = [80, 90, 100, 110, 120]
    smile = generate_smile(
        model="Merton",
        S0=S0,
        strikes=strikes,
        T=T,
        r=r,
        q=q,
        sigma=sigma,
        lam=lam,
        mu_J=mu_J,
        sigma_J=sigma_J,
        grid_kwargs={"NS": 200, "NT": 200},
        plot=True,
    )

    # 4) Compare with Black–Scholes
    compare_with_black_scholes(
        S0=S0,
        strikes=strikes,
        T=T,
        r=r,
        q=q,
        jump_smile=smile,
    )

    # 5) Simulate paths
    sim = simulate_jump_paths(
        model="Merton",
        S0=S0,
        T=T,
        r=r,
        q=q,
        sigma=sigma,
        lam=lam,
        mu_J=mu_J,
        sigma_J=sigma_J,
        n_paths=200,
        n_steps=252,
        seed=42,
    )
    plot_paths(sim["t_grid"], sim["paths"])
