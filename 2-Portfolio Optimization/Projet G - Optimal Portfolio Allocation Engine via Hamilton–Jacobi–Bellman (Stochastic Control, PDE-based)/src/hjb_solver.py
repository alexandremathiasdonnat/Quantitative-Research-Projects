# src/hjb_solver.py
"""
Finite-difference HJB solver (backward in time).

We discretize:
- time: t_0 < t_1 < ... < t_N = T
- wealth: W_0 < W_1 < ... < W_M

We solve backward:
    V(t_n, W) from V(t_{n+1}, W) using a semi-implicit / explicit scheme.

For simplicity and robustness in this educational project:
- Derivatives V_W and V_WW are computed by central differences in the interior.
- At each time step, we compute the maximizing pi on a pi_grid using the discrete Hamiltonian.

The PDE:
    V_t + max_pi [ a(pi) W V_W + 0.5 b(pi)^2 W^2 V_WW ] = 0

Backward Euler (discrete):
    V^n = V^{n+1} - dt * max_pi[ ... evaluated at (n+1) ]   (explicit in spatial terms)

This is not the most stable/high-accuracy scheme, but it's:
- clear, modular, easy to extend,
- enough to extract a policy surface and run simulations.

Extensions (not implemented here):
- implicit schemes (solve linear system each step),
- monotone schemes for guaranteed stability,
- constraints and transaction costs (variational inequalities).
"""

from dataclasses import dataclass
import numpy as np

from .hjb_equation import hjb_hamiltonian
from .utility import crra_utility


@dataclass(frozen=True)
class HJBSolverParams:
    n_time: int
    n_wealth: int
    W_min: float
    W_max: float
    pi_min: float = -2.0
    pi_max: float = 2.0
    n_pi: int = 401


def _finite_diff_first(W: np.ndarray, V: np.ndarray) -> np.ndarray:
    """
    Central differences for first derivative V_W on a 1D grid.
    One-sided differences on boundaries.
    """
    dV = np.zeros_like(V)
    dW = np.diff(W)

    # interior
    dV[1:-1] = (V[2:] - V[:-2]) / (W[2:] - W[:-2])

    # boundaries (one-sided)
    dV[0] = (V[1] - V[0]) / dW[0]
    dV[-1] = (V[-1] - V[-2]) / dW[-1]
    return dV


def _finite_diff_second(W: np.ndarray, V: np.ndarray) -> np.ndarray:
    """
    Second derivative V_WW on a non-uniform grid (works for uniform too).
    Uses three-point formula.
    """
    d2V = np.zeros_like(V)

    # interior
    Wm = W[:-2]
    W0 = W[1:-1]
    Wp = W[2:]
    Vm = V[:-2]
    V0 = V[1:-1]
    Vp = V[2:]

    denom = (W0 - Wm) * (Wp - W0) * (Wp - Wm)
    d2V[1:-1] = 2.0 * (Vm * (W0 - Wp) + V0 * (Wp - Wm) + Vp * (Wm - W0)) / denom

    # boundaries: simple second-order one-sided approximations
    # (ok for visualization; can be improved)
    d2V[0] = d2V[1]
    d2V[-1] = d2V[-2]
    return d2V


def solve_hjb(mu: float, sigma: float, r: float, T: float, gamma: float, solver: HJBSolverParams):
    """
    Solve the HJB backward and return:
    - time grid t (shape [n_time])
    - wealth grid W (shape [n_wealth])
    - value function V(t,W) (shape [n_time, n_wealth])
    - optimal policy pi*(t,W) (shape [n_time, n_wealth])

    Notes:
    - Terminal condition V(T,W) = U(W)
    - We compute pi*(t,W) by brute-force maximization over a pi_grid.
    """
    if solver.W_min <= 0:
        raise ValueError("W_min must be > 0 for CRRA utility.")
    if solver.W_max <= solver.W_min:
        raise ValueError("W_max must be > W_min.")
    if solver.n_time < 2 or solver.n_wealth < 5:
        raise ValueError("Need at least n_time>=2 and n_wealth>=5.")

    t = np.linspace(0.0, T, solver.n_time)
    dt = t[1] - t[0]
    W = np.linspace(solver.W_min, solver.W_max, solver.n_wealth)

    pi_grid = np.linspace(solver.pi_min, solver.pi_max, solver.n_pi)

    V = np.zeros((solver.n_time, solver.n_wealth), dtype=float)
    pi_star = np.zeros_like(V)

    # terminal condition
    V[-1, :] = crra_utility(W, gamma=gamma)

    # backward induction
    for n in range(solver.n_time - 2, -1, -1):
        V_next = V[n + 1, :].copy()

        # spatial derivatives at next time (explicit scheme)
        Vw = _finite_diff_first(W, V_next)
        Vww = _finite_diff_second(W, V_next)

        # compute Hamiltonian for all pi candidates and wealth points
        H = hjb_hamiltonian(W=W, Vw=Vw, Vww=Vww, mu=mu, sigma=sigma, r=r, pi_grid=pi_grid)

        # argmax in pi dimension
        idx = np.argmax(H, axis=0)
        pi_opt = pi_grid[idx]
        H_opt = H[idx, np.arange(H.shape[1])]

        # backward Euler update: V^n = V^{n+1} - dt * H_opt
        V[n, :] = V_next - dt * H_opt
        pi_star[n, :] = pi_opt

    # define policy at terminal time as last computed (not used in simulation)
    pi_star[-1, :] = pi_star[-2, :]
    return t, W, V, pi_star
