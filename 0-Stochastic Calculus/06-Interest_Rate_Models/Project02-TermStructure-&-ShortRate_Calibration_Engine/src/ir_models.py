# src/ir_models.py

"""
Closed-form formulas for short-rate term-structure models.

We implement:
    - Vasicek model
    - CIR model (bonus)

All formulas are written under the risk-neutral measure,
and we only use them to compute zero-coupon bond prices.
"""

from dataclasses import dataclass
from typing import Literal

import numpy as np


@dataclass
class VasicekParams:
    """
    Parameters for the Vasicek short-rate model:

        dr_t = kappa (theta - r_t) dt + sigma dW_t

    We interpret kappa, theta, sigma under the risk-neutral measure.
    """

    kappa: float
    theta: float
    sigma: float
    r0: float  # short rate at t = 0


@dataclass
class CIRParams:
    """
    Parameters for the CIR short-rate model:

        dr_t = kappa (theta - r_t) dt + sigma * sqrt(r_t) dW_t

    Feller condition (not enforced here, but often desired in practice):
        2 kappa theta >= sigma^2
    """

    kappa: float
    theta: float
    sigma: float
    r0: float


def vasicek_B(t: float, T: float, kappa: float) -> float:
    """
    Vasicek B(t, T) function:

        B(t, T) = (1 - exp(-kappa (T - t))) / kappa
    """
    tau = T - t
    if tau < 0:
        raise ValueError("T must be >= t.")
    if tau == 0:
        return 0.0
    return (1.0 - np.exp(-kappa * tau)) / kappa


def vasicek_A(t: float, T: float, params: VasicekParams) -> float:
    """
    Vasicek A(t, T) function (for P(t, T) = A(t, T) * exp(-B(t, T) * r_t)).

    Under the risk-neutral Vasicek model, the closed form is:

        B = (1 - e^{-kappa * tau}) / kappa
        A = exp(
                (theta - sigma^2 / (2 kappa^2)) * (B - tau)
                - (sigma^2 / (4 kappa)) * B^2
            )

    where tau = T - t.
    """
    kappa = params.kappa
    theta = params.theta
    sigma = params.sigma

    tau = T - t
    if tau < 0:
        raise ValueError("T must be >= t.")

    B = vasicek_B(t, T, kappa)

    term1 = (theta - (sigma**2) / (2.0 * kappa**2)) * (B - tau)
    term2 = (sigma**2 / (4.0 * kappa)) * (B**2)

    A = np.exp(term1 - term2)
    return A


def vasicek_zcb_price(t: float, T: float, r_t: float, params: VasicekParams) -> float:
    """
    Zero-coupon bond price P(t, T) in the Vasicek model.

        P(t, T) = A(t, T) * exp(-B(t, T) * r_t)

    Parameters
    ----------
    t : float
        Current time.
    T : float
        Maturity time (T >= t).
    r_t : float
        Short rate at time t.
    params : VasicekParams
        Model parameters.

    Returns
    -------
    float
        Zero-coupon bond price P(t, T).
    """
    B = vasicek_B(t, T, params.kappa)
    A = vasicek_A(t, T, params)
    return A * np.exp(-B * r_t)


def cir_A_B(t: float, T: float, params: CIRParams) -> tuple[float, float]:
    """
    CIR A(t, T) and B(t, T) functions for P(t, T) = A * exp(-B r_t).

    Closed-form solution under risk-neutral CIR:

        gamma = sqrt(kappa^2 + 2 sigma^2)
        B(t,T) = 2 (e^{gamma tau} - 1) / ((gamma + kappa)(e^{gamma tau} - 1) + 2 gamma)
        A(t,T) = [ 2 gamma * exp((kappa + gamma) tau / 2)
                   / ((gamma + kappa)(e^{gamma tau} - 1) + 2 gamma)
                 ]^{ 2 kappa theta / sigma^2 }

    where tau = T - t.
    """
    kappa = params.kappa
    theta = params.theta
    sigma = params.sigma

    tau = T - t
    if tau < 0:
        raise ValueError("T must be >= t.")

    if tau == 0:
        return 1.0, 0.0

    gamma = np.sqrt(kappa**2 + 2.0 * sigma**2)
    exp_gamma_tau = np.exp(gamma * tau)

    denom = (gamma + kappa) * (exp_gamma_tau - 1.0) + 2.0 * gamma
    B = 2.0 * (exp_gamma_tau - 1.0) / denom

    A_factor = (2.0 * gamma * np.exp((kappa + gamma) * tau / 2.0)) / denom
    power = 2.0 * kappa * theta / (sigma**2)

    A = A_factor**power
    return A, B


def cir_zcb_price(t: float, T: float, r_t: float, params: CIRParams) -> float:
    """
    Zero-coupon bond price P(t, T) in the CIR model.

        P(t, T) = A(t, T) * exp(-B(t, T) * r_t)
    """
    A, B = cir_A_B(t, T, params)
    return A * np.exp(-B * r_t)


def zcb_price(
    t: float,
    T: float,
    r_t: float,
    params,
    model_type: Literal["vasicek", "cir"] = "vasicek",
) -> float:
    """
    Generic wrapper: compute P(t, T) for a given model type.

    Parameters
    ----------
    t : float
        Current time.
    T : float
        Maturity time (T >= t).
    r_t : float
        Short rate at time t.
    params : VasicekParams or CIRParams
        Model parameters.
    model_type : {'vasicek', 'cir'}
        Which model to use.

    Returns
    -------
    float
        Zero-coupon price.
    """
    if model_type == "vasicek":
        return vasicek_zcb_price(t, T, r_t, params)
    elif model_type == "cir":
        return cir_zcb_price(t, T, r_t, params)
    else:
        raise ValueError("model_type must be 'vasicek' or 'cir'.")
