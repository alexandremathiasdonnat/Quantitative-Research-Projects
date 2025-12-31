# src/evaluation.py
"""
Buy-side evaluation metrics for wealth strategies.

We focus on:
- terminal wealth statistics (mean/median)
- quantiles (5%, 95%)
- max drawdown (on wealth path)
- Sharpe ratio (computed on log returns of wealth)
- expected utility (CRRA)

Notes
-----
- Sharpe on wealth returns is not "perfect" (since wealth is not a traded asset),
  but it's a convenient buy-side-style risk-adjusted summary.
"""

from dataclasses import dataclass
import numpy as np

from .utility import crra_utility


def max_drawdown(wealth_path: np.ndarray) -> float:
    """
    Max drawdown of one wealth path.

    wealth_path : shape [n_steps+1]
    """
    w = np.asarray(wealth_path)
    peak = np.maximum.accumulate(w)
    dd = (w - peak) / np.maximum(peak, 1e-16)
    return float(np.min(dd))


def sharpe_ratio_from_wealth_paths(W_paths: np.ndarray, dt: float) -> float:
    """
    Compute annualized Sharpe ratio from wealth paths.

    Use log-returns:
        r_k = log(W_{k+1}/W_k)

    Annualization: assuming dt is in years (e.g. dt=1/252).
    """
    W = np.asarray(W_paths)
    log_ret = np.log(np.maximum(W[:, 1:], 1e-16) / np.maximum(W[:, :-1], 1e-16))
    # average over time then over sims
    r = log_ret.reshape(-1)
    mean = np.mean(r)
    std = np.std(r) + 1e-16
    sharpe = (mean / std) * np.sqrt(1.0 / dt)
    return float(sharpe)


def summarize_strategy(W_paths: np.ndarray, dt: float, gamma: float) -> dict:
    """
    Compute summary statistics for one strategy given simulated wealth paths.
    """
    terminal = W_paths[:, -1]
    mean_w = float(np.mean(terminal))
    med_w = float(np.median(terminal))
    q05 = float(np.quantile(terminal, 0.05))
    q95 = float(np.quantile(terminal, 0.95))

    # max drawdown distribution
    mdds = np.array([max_drawdown(W_paths[i]) for i in range(W_paths.shape[0])])
    mdd_mean = float(np.mean(mdds))

    sharpe = sharpe_ratio_from_wealth_paths(W_paths, dt=dt)
    exp_u = float(np.mean(crra_utility(terminal, gamma=gamma)))

    return {
        "terminal_mean": mean_w,
        "terminal_median": med_w,
        "terminal_q05": q05,
        "terminal_q95": q95,
        "max_drawdown_mean": mdd_mean,
        "sharpe_annualized": sharpe,
        "expected_utility": exp_u,
    }


def evaluate_all(wealth_paths: dict, dt: float, gamma: float) -> dict:
    """
    Evaluate all strategies.
    """
    out = {}
    for name, W_paths in wealth_paths.items():
        out[name] = summarize_strategy(W_paths=W_paths, dt=dt, gamma=gamma)
    return out
