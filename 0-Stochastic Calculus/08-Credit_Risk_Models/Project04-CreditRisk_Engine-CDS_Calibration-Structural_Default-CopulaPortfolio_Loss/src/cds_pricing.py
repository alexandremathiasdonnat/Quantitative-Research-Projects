"""
CDS pricing and hazard-rate calibration.

We work with a *constant* default intensity λ and a flat risk-free rate r.
Premium and protection legs are computed in continuous time with a simple
approximation. The goal is to invert the mapping λ : spread so that
the observed CDS spread implies a hazard rate.

INPUT PROVENANCE
----------------
Typical sources in the notebook:
    - Manual inputs for a single CDS:
        spread (in basis points), maturity T, recovery R, rate r
    - Or a CSV with one row per tenor and spread, loaded via pandas.

This module does not read files: it expects numeric inputs passed by the caller.
"""

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class CDSParams:
    """
    Parameters of a standard CDS under a constant intensity model.

    Attributes
    ----------
    spread_bps : float
        Quoted CDS spread in basis points (e.g. 120 for 120 bps).
    maturity : float
        Contract maturity (years).
    recovery : float
        Recovery rate (e.g. 0.4).
    rate : float
        Flat risk-free rate r for discounting.
    payment_frequency : int
        Number of premium payments per year (e.g. 4 for quarterly).
    """
    spread_bps: float
    maturity: float
    recovery: float
    rate: float
    payment_frequency: int = 4


def survival_prob(t: float, lam: float) -> float:
    """Survival probability under constant intensity: S(t) = exp(-λ t)."""
    return np.exp(-lam * t)


def premium_leg_pv(params: CDSParams, lam: float) -> float:
    """
    Present value of the premium leg for unit notional.

    Approximation:
    PL = s * sum_{i} Δ_i * P(τ > T_i) * exp(-r T_i)

    where s is the spread in *decimal* (not bps).
    """
    s = params.spread_bps / 10_000.0  # convert bps to decimal
    T = params.maturity
    r = params.rate
    freq = params.payment_frequency

    # Regular payment dates
    payment_times = np.linspace(1.0 / freq, T, int(T * freq))
    delta = 1.0 / freq

    surv = survival_prob(payment_times, lam)
    discounts = np.exp(-r * payment_times)

    return s * np.sum(delta * surv * discounts)


def protection_leg_pv(params: CDSParams, lam: float, n_steps: int = 1_000) -> float:
    """
    Present value of the protection leg for unit notional.

    Approximation via numerical integration:
    Prot = (1 - R) * ∫_0^T S(t) λ e^{-r t} dt

    We approximate the integral with a simple Riemann sum.
    """
    T = params.maturity
    r = params.rate
    R = params.recovery

    times = np.linspace(0.0, T, n_steps + 1)[1:]  # exclude 0
    dt = T / n_steps

    S = survival_prob(times, lam)
    density_default = S * lam  # λ S(t)
    discounts = np.exp(-r * times)

    integral = np.sum(density_default * discounts * dt)
    return (1.0 - R) * integral


def cds_pv_difference(lam: float, params: CDSParams) -> float:
    """
    Difference between premium and protection leg PVs (unit notional).

    We seek lam such that PV_premium(lam) - PV_protection(lam) = 0.
    """
    pl = premium_leg_pv(params, lam)
    prot = protection_leg_pv(params, lam)
    return pl - prot


def calibrate_lambda(
    params: CDSParams,
    lam_min: float = 1e-6,
    lam_max: float = 5.0,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> float:
    """
    Calibrate the constant intensity λ from the quoted CDS spread.

    We solve for λ in [lam_min, lam_max] such that
    PV_premium(λ) = PV_protection(λ) using a bisection method.

    Parameters
    ----------
    params : CDSParams
    lam_min, lam_max : float
        Bracketing interval for λ.
    tol : float
        Tolerance on the absolute PV difference.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    float
        Calibrated hazard rate λ*.
    """
    a, b = lam_min, lam_max
    fa = cds_pv_difference(a, params)
    fb = cds_pv_difference(b, params)

    if fa * fb > 0:
        raise ValueError(
            "Bisection failed: PV differences have the same sign on the interval. "
            "Try expanding lam_min/lam_max."
        )

    for _ in range(max_iter):
        mid = 0.5 * (a + b)
        fm = cds_pv_difference(mid, params)

        if abs(fm) < tol:
            return mid

        if fa * fm < 0:
            b, fb = mid, fm
        else:
            a, fa = mid, fm

    # If we reach here, we did not converge within max_iter.
    return 0.5 * (a + b)


def implied_pd_from_lambda(lam: float, T: float) -> float:
    """
    Compute the cumulative default probability under constant intensity.

    PD(T) = 1 - exp(-λ T).
    """
    return 1.0 - np.exp(-lam * T)
