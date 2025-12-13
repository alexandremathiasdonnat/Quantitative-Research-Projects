# src/plotting.py
"""
Plotting helpers for the dashboard.

We keep plotting separate from business logic to keep the notebook clean.

Plots:
- heatmap of optimal policy pi*(t,W)
- sample wealth trajectories
- terminal wealth histograms
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_policy_heatmap(t_grid: np.ndarray, W_grid: np.ndarray, pi_star: np.ndarray, title: str = "HJB Optimal Policy π*(t,W)"):
    """
    Heatmap of optimal risky fraction.
    """
    T, M = pi_star.shape
    # mesh orientation: time on x-axis, wealth on y-axis
    plt.figure()
    plt.imshow(
        pi_star.T,
        aspect="auto",
        origin="lower",
        extent=[t_grid[0], t_grid[-1], W_grid[0], W_grid[-1]],
    )
    plt.colorbar(label="π* (risky fraction)")
    plt.xlabel("time t")
    plt.ylabel("wealth W")
    plt.title(title)
    plt.show()


def plot_wealth_trajectories(t: np.ndarray, wealth_paths: dict, n_paths: int = 30, title: str = "Wealth Trajectories (sample)"):
    """
    Plot a small sample of paths for each strategy (overlay).
    """
    plt.figure()
    for name, W in wealth_paths.items():
        n = min(n_paths, W.shape[0])
        for i in range(n):
            plt.plot(t, W[i], alpha=0.15)
    plt.xlabel("time t")
    plt.ylabel("wealth W_t")
    plt.title(title)
    plt.show()


def plot_terminal_histograms(wealth_paths: dict, bins: int = 60, title: str = "Terminal Wealth Distribution"):
    """
    Overlay terminal wealth histograms for strategies.
    """
    plt.figure()
    for name, W in wealth_paths.items():
        terminal = W[:, -1]
        plt.hist(terminal, bins=bins, alpha=0.35, label=name)
    plt.xlabel("W_T")
    plt.ylabel("frequency")
    plt.title(title)
    plt.legend()
    plt.show()
