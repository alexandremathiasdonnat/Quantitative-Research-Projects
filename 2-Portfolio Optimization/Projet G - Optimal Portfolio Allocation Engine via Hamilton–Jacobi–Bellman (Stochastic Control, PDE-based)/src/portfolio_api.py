# src/portfolio_api.py
"""
High-level API for the notebook/dashboard.

This is the single entry-point layer, so the notebook stays clean:
- solve_hjb(params)
- simulate_strategies(params)
- evaluate_results(results)

This mirrors a production research pattern:
inputs -> engine -> results -> evaluation -> plots
"""

from dataclasses import dataclass
import numpy as np

from .hjb_solver import HJBSolverParams, solve_hjb
from .simulation import SimulationParams, simulate_strategies
from .evaluation import evaluate_all
from .policies import (
    policy_buy_and_hold,
    policy_constant_mix,
    policy_vol_target,
    policy_mean_variance,
    policy_merton_closed_form,
    policy_hjb_from_surface,
)


@dataclass(frozen=True)
class EngineInputs:
    # market
    mu: float
    sigma: float
    r: float
    T: float
    W0: float
    # investor
    gamma: float
    # numerical
    hjb: HJBSolverParams
    sim: SimulationParams
    # implementation layer (buy-side realism)
    use_costs: bool = False
    cost_rate: float = 0.0

def solve_hjb_engine(inputs: EngineInputs):
    """
    Solve HJB and return surfaces to be used by policies and plots.
    """
    t_grid, W_grid, V, pi_star = solve_hjb(
        mu=inputs.mu,
        sigma=inputs.sigma,
        r=inputs.r,
        T=inputs.T,
        gamma=inputs.gamma,
        solver=inputs.hjb,
    )
    return {"t_grid": t_grid, "W_grid": W_grid, "V": V, "pi_star": pi_star}


def build_policies(inputs: EngineInputs, hjb_solution: dict) -> dict:
    """
    Construct all benchmark strategies + HJB optimal.
    """
    t_grid = hjb_solution["t_grid"]
    W_grid = hjb_solution["W_grid"]
    pi_star = hjb_solution["pi_star"]

    policies = {
        "Buy&Hold_100%Risky": policy_buy_and_hold(pi_const=1.0),
        "ConstantMix_60_40": policy_constant_mix(pi_const=0.60),
        "VolTarget_10%": policy_vol_target(target_vol=0.10, max_leverage=2.0),
        "MeanVariance_lambda3": policy_mean_variance(lambda_risk=3.0, pi_clip=2.0),
        "MertonClosedForm": policy_merton_closed_form(gamma=inputs.gamma, pi_clip=2.0),
        "HJB_Optimal": policy_hjb_from_surface(t_grid=t_grid, W_grid=W_grid, pi_surface=pi_star, pi_clip=3.0),
    }
    return policies


def simulate_strategies_engine(inputs: EngineInputs, policies: dict):
    """
    Monte Carlo simulation for all strategies (optional transaction costs).
    """
    sim_res = simulate_strategies(
        policies=policies,
        mu=inputs.mu,
        sigma=inputs.sigma,
        r=inputs.r,
        T=inputs.T,
        W0=inputs.W0,
        sim=inputs.sim,
        use_costs=inputs.use_costs,
        cost_rate=inputs.cost_rate,
    )
    return sim_res



def evaluate_results_engine(inputs: EngineInputs, sim_results: dict):
    """
    Compute buy-side evaluation metrics.
    """
    # dt used in simulation is adjusted to hit exactly T:
    t = sim_results["t"]
    dt = t[1] - t[0]
    metrics = evaluate_all(sim_results["wealth_paths"], dt=dt, gamma=inputs.gamma)
    return metrics
