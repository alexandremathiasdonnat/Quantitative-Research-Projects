# src/policies.py
"""
Comparative buy-side strategies (benchmarks).

We implement the following policies as functions producing pi_t at each time:

- Buy & Hold:
  *Interpretation*: choose one constant risky fraction and keep it.

- Constant Mix (e.g. 60/40):
  constant pi = 0.6

- Volatility Targeting:
  dynamic pi_t = target_vol / sigma
  (clipped to a max leverage)

- Mean-Variance (static Markowitz style):
  pi = (mu - r) / (lambda * sigma^2)
  where lambda is a risk-aversion-like parameter (not CRRA gamma).
  (This is the continuous-time analogue for a single risky asset.)

- HJB Optimal Policy:
  pi*(t, W) extracted from the HJB solver surface by interpolation.

Notes
-----
- In the pure Merton setup, HJB pi* should be close to the Merton fraction,
  hence almost constant (flat heatmap).
"""

from dataclasses import dataclass
import numpy as np

from .hjb_equation import merton_fraction


@dataclass(frozen=True)
class PolicySpec:
    name: str


def policy_buy_and_hold(pi_const: float):
    def _pi(t: float, W: np.ndarray, **kwargs) -> np.ndarray:
        return np.full_like(W, fill_value=pi_const, dtype=float)
    return _pi


def policy_constant_mix(pi_const: float = 0.60):
    def _pi(t: float, W: np.ndarray, **kwargs) -> np.ndarray:
        return np.full_like(W, fill_value=pi_const, dtype=float)
    return _pi


def policy_vol_target(target_vol: float = 0.10, max_leverage: float = 2.0):
    """
    pi = target_vol / sigma, clipped.

    For a single risky asset with constant sigma, this becomes constant.
    Still included because it's a standard systematic buy-side heuristic.
    """
    def _pi(t: float, W: np.ndarray, sigma: float, **kwargs) -> np.ndarray:
        raw = target_vol / max(sigma, 1e-12)
        raw = np.clip(raw, -max_leverage, max_leverage)
        return np.full_like(W, fill_value=raw, dtype=float)
    return _pi


def policy_mean_variance(lambda_risk: float = 3.0, pi_clip: float = 2.0):
    """
    Static mean-variance-style allocation in continuous time for 1 risky asset:
        pi = (mu - r) / (lambda * sigma^2)
    This resembles Merton but with lambda instead of CRRA gamma.

    We clip for realism.
    """
    def _pi(t: float, W: np.ndarray, mu: float, r: float, sigma: float, **kwargs) -> np.ndarray:
        raw = (mu - r) / (max(lambda_risk, 1e-12) * max(sigma, 1e-12) ** 2)
        raw = float(np.clip(raw, -pi_clip, pi_clip))
        return np.full_like(W, fill_value=raw, dtype=float)
    return _pi


def policy_merton_closed_form(gamma: float, pi_clip: float = 2.0):
    """
    Closed-form Merton fraction (useful as a reference baseline).
    """
    def _pi(t: float, W: np.ndarray, mu: float, r: float, sigma: float, **kwargs) -> np.ndarray:
        raw = merton_fraction(mu=mu, r=r, sigma=sigma, gamma=gamma)
        raw = float(np.clip(raw, -pi_clip, pi_clip))
        return np.full_like(W, fill_value=raw, dtype=float)
    return _pi


def policy_hjb_from_surface(t_grid: np.ndarray, W_grid: np.ndarray, pi_surface: np.ndarray, pi_clip: float = 3.0):
    """
    Interpolate pi*(t, W) from the precomputed HJB policy surface.

    Parameters
    ----------
    t_grid : [nT]
    W_grid : [nW]
    pi_surface : [nT, nW]
        Optimal policy computed by the solver.
    """
    t_grid = np.asarray(t_grid)
    W_grid = np.asarray(W_grid)
    pi_surface = np.asarray(pi_surface)

    def _interp_1d(x_grid: np.ndarray, y_grid: np.ndarray, x: np.ndarray) -> np.ndarray:
        # simple linear interpolation (no scipy dependency)
        x = np.asarray(x)
        return np.interp(x, x_grid, y_grid)

    def _pi(t: float, W: np.ndarray, **kwargs) -> np.ndarray:
        # clamp t within grid
        t_clamped = float(np.clip(t, t_grid[0], t_grid[-1]))

        # find nearest time indices for linear interpolation in time
        if t_clamped <= t_grid[0]:
            row = pi_surface[0, :]
            out = _interp_1d(W_grid, row, W)
            return np.clip(out, -pi_clip, pi_clip)

        if t_clamped >= t_grid[-1]:
            row = pi_surface[-1, :]
            out = _interp_1d(W_grid, row, W)
            return np.clip(out, -pi_clip, pi_clip)

        j = np.searchsorted(t_grid, t_clamped)  # t_grid[j-1] < t <= t_grid[j]
        t0, t1 = t_grid[j - 1], t_grid[j]
        w = (t_clamped - t0) / max(t1 - t0, 1e-12)

        row0 = pi_surface[j - 1, :]
        row1 = pi_surface[j, :]
        pi0 = _interp_1d(W_grid, row0, W)
        pi1 = _interp_1d(W_grid, row1, W)
        out = (1.0 - w) * pi0 + w * pi1
        return np.clip(out, -pi_clip, pi_clip)

    return _pi
