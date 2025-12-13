# src/simulation.py
"""
Monte Carlo simulation of wealth trajectories under multiple strategies.

Key design principle:
- All strategies are evaluated on the *same Brownian scenarios* to ensure fairness.

We simulate:
    W_{t+dt} = W_t * exp( (r + pi*(mu-r) - 0.5 (pi*sigma)^2) dt + (pi*sigma) sqrt(dt) z )

This is a stable multiplicative scheme that keeps wealth positive.

Outputs
-------
- wealth_paths[strategy_name] : array [n_sims, n_steps+1]
- pi_paths[strategy_name]     : array [n_sims, n_steps] (controls used each step)
"""

from dataclasses import dataclass
import numpy as np

from .market_models import wealth_step


@dataclass(frozen=True)
class SimulationParams:
    n_sims: int
    dt: float
    seed: int = 42


def simulate_strategies(
    policies: dict,
    mu: float,
    sigma: float,
    r: float,
    T: float,
    W0: float,
    sim: SimulationParams,
    use_costs: bool = False,
    cost_rate: float = 0.0,
):
    """
    Simulate wealth paths for each strategy.

    Transaction costs (optional)
    ----------------------------
    If use_costs=True, we apply a proportional turnover cost when rebalancing:
        cost = cost_rate * |pi_new - pi_old| * W
    and we reduce wealth immediately before the market evolution step.

    This is a practical buy-side implementation layer:
    we do NOT change the HJB solver, we evaluate strategies net-of-costs.
    """
    if W0 <= 0:
        raise ValueError("W0 must be > 0.")
    if use_costs and cost_rate < 0:
        raise ValueError("cost_rate must be >= 0.")

    n_steps = int(np.ceil(T / sim.dt))
    dt = T / n_steps  # adjust to hit exactly T
    t = np.linspace(0.0, T, n_steps + 1)

    rng = np.random.default_rng(sim.seed)
    Z = rng.standard_normal(size=(sim.n_sims, n_steps))

    wealth_paths = {}
    pi_paths = {}

    for name, policy in policies.items():
        W = np.full(sim.n_sims, W0, dtype=float)
        W_path = np.zeros((sim.n_sims, n_steps + 1), dtype=float)
        P_path = np.zeros((sim.n_sims, n_steps), dtype=float)

        # track previous allocation for turnover costs
        pi_prev = np.zeros(sim.n_sims, dtype=float)

        W_path[:, 0] = W

        for k in range(n_steps):
            tk = t[k]

            # propose new allocation based on current wealth
            pi_new = policy(tk, W, mu=mu, r=r, sigma=sigma)
            P_path[:, k] = pi_new

            # apply turnover costs (wealth is reduced immediately)
            if use_costs and cost_rate > 0:
                turnover = np.abs(pi_new - pi_prev)
                W = W * (1.0 - cost_rate * turnover)
                W = np.maximum(W, 1e-16)  # keep strictly positive

            # evolve wealth with the chosen allocation on the same Brownian increment
            W = wealth_step(W=W, pi=pi_new, mu=mu, sigma=sigma, r=r, dt=dt, z=Z[:, k])
            W_path[:, k + 1] = W

            # update previous allocation
            pi_prev = pi_new

        wealth_paths[name] = W_path
        pi_paths[name] = P_path

    return {"t": t, "Z": Z, "wealth_paths": wealth_paths, "pi_paths": pi_paths}

