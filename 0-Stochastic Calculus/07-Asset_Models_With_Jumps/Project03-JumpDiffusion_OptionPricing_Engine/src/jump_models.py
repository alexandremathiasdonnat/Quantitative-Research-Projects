"""
jump_models.py

Jump size distributions and drift adjustment for jump–diffusion models.

All inputs are plain Python floats provided by the user in the notebook.
There is NO file I/O here: the notebook is responsible for creating
the parameter values and passing them to these functions/classes.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Protocol


class JumpModel(Protocol):
    """Protocol for jump size distributions Y.

    A jump model provides:
    - pdf(y): probability density of Y at y
    - expected_exp_jump(): E[e^Y], needed for risk-neutral drift adjustment.
    """

    def pdf(self, y: np.ndarray) -> np.ndarray:
        ...

    def expected_exp_jump(self) -> float:
        ...


@dataclass
class MertonJumpModel:
    """Merton jump model: Y ~ Normal(mu_J, sigma_J^2)."""

    mu_J: float
    sigma_J: float

    def pdf(self, y: np.ndarray) -> np.ndarray:
        """Normal density of the jump size at y."""
        var = self.sigma_J ** 2
        norm_const = 1.0 / np.sqrt(2.0 * np.pi * var)
        return norm_const * np.exp(-(y - self.mu_J) ** 2 / (2.0 * var))

    def expected_exp_jump(self) -> float:
        """E[e^Y] for Y ~ N(mu_J, sigma_J^2) = exp(mu_J + 0.5 sigma_J^2)."""
        return float(np.exp(self.mu_J + 0.5 * self.sigma_J ** 2))


@dataclass
class KouJumpModel:
    """Kou jump model: double exponential asymmetric distribution.

    P(Y > 0) = p, density on y>0: p * eta1 * exp(-eta1 * y)
    P(Y < 0) = 1-p, density on y<0: (1-p) * eta2 * exp(eta2 * y)
    Parameters must satisfy: eta1 > 1, eta2 > 0 for E[e^Y] to be finite.
    """

    p: float
    eta1: float
    eta2: float

    def pdf(self, y: np.ndarray) -> np.ndarray:
        """Double-exponential density evaluated elementwise."""
        y = np.asarray(y)
        res = np.zeros_like(y, dtype=float)

        pos_mask = y > 0
        neg_mask = y < 0

        res[pos_mask] = self.p * self.eta1 * np.exp(-self.eta1 * y[pos_mask])
        res[neg_mask] = (1.0 - self.p) * self.eta2 * np.exp(self.eta2 * y[neg_mask])
        # y == 0 has probability 0 in continuous distribution => we keep 0
        return res

    def expected_exp_jump(self) -> float:
        """E[e^Y] for Kou model.

        E[e^Y] = p * eta1 / (eta1 - 1) + (1-p) * eta2 / (eta2 + 1),
        provided eta1 > 1.
        """
        if self.eta1 <= 1.0:
            raise ValueError("Kou model requires eta1 > 1 for E[e^Y] to be finite.")
        term_up = self.p * self.eta1 / (self.eta1 - 1.0)
        term_down = (1.0 - self.p) * self.eta2 / (self.eta2 + 1.0)
        return float(term_up + term_down)


def adjusted_risk_neutral_drift(
    r: float,
    q: float,
    lam: float,
    jump_model: JumpModel,
) -> float:
    """Compute risk-neutral drift μ̃ for S_t under the jump–diffusion.

    Risk-neutral condition:
        E[dS_t / S_{t-}] = (r - q) dt
        = μ̃ dt + λ (E[e^Y - 1]) dt

    => μ̃ = r - q - λ (E[e^Y] - 1).

    Parameters
    ----------
    r : float
        Risk-free rate.
    q : float
        Continuous dividend yield.
    lam : float
        Jump intensity λ.
    jump_model : JumpModel
        MertonJumpModel or KouJumpModel instance.

    Returns
    -------
    mu_tilde : float
        Risk-neutral drift of the diffusion part.
    """
    exp_jump = jump_model.expected_exp_jump()
    return float(r - q - lam * (exp_jump - 1.0))
