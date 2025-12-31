# src/calibration.py

"""
Calibration routines for short-rate models.

We fit model parameters so that model zero-coupon prices
match market zero-coupon prices as closely as possible.

The default loss is a weighted L2 loss on prices:

    Loss(params) = sum_i w_i (P_model(0, T_i) - P_mkt(0, T_i))^2
"""

from dataclasses import asdict
from typing import Literal, Callable

import numpy as np
from scipy.optimize import minimize

from .ir_models import VasicekParams, CIRParams, zcb_price


def _compute_model_prices(
    maturities: np.ndarray,
    params,
    model_type: Literal["vasicek", "cir"],
) -> np.ndarray:
    """
    Compute model zero-coupon prices P(0, T_i) for a given set of parameters.
    """
    prices = np.array(
        [
            zcb_price(
                t=0.0,
                T=float(T),
                r_t=params.r0,
                params=params,
                model_type=model_type,
            )
            for T in maturities
        ],
        dtype=float,
    )
    return prices


def vasicek_loss_on_prices(
    x: np.ndarray,
    maturities: np.ndarray,
    market_prices: np.ndarray,
    weights: np.ndarray | None = None,
) -> float:
    """
    L2 loss between Vasicek model prices and market prices.

    Parameters
    ----------
    x : ndarray
        Parameter vector [kappa, theta, sigma, r0].
    maturities : ndarray
        Market maturities (T_i).
    market_prices : ndarray
        Market zero-coupon prices P_mkt(0, T_i).
    weights : ndarray, optional
        Optional weights w_i for each maturity.

    Returns
    -------
    float
        Loss value.
    """
    kappa, theta, sigma, r0 = x
    params = VasicekParams(kappa=kappa, theta=theta, sigma=sigma, r0=r0)

    model_prices = _compute_model_prices(maturities, params, model_type="vasicek")

    if weights is None:
        weights = np.ones_like(model_prices)

    diff = model_prices - market_prices
    return float(np.sum(weights * diff**2))


def calibrate_vasicek(
    maturities: np.ndarray,
    market_prices: np.ndarray,
    initial_guess: np.ndarray | None = None,
    bounds: list[tuple[float, float]] | None = None,
    weights: np.ndarray | None = None,
) -> tuple[VasicekParams, dict]:
    """
    Calibrate Vasicek parameters to market zero-coupon prices.

    Parameters
    ----------
    maturities : ndarray
        Maturities T_i.
    market_prices : ndarray
        Market zero-coupon prices P_mkt(0, T_i).
    initial_guess : ndarray, optional
        Initial guess [kappa, theta, sigma, r0].
        If None, a simple heuristic is used.
    bounds : list of tuple(float, float), optional
        Bounds for each parameter.
    weights : ndarray, optional
        Optional weights for each maturity.

    Returns
    -------
    params_hat : VasicekParams
        Calibrated parameters.
    info : dict
        Optimization diagnostics: success flag, message, final loss, etc.
    """
    maturities = np.asarray(maturities, dtype=float)
    market_prices = np.asarray(market_prices, dtype=float)

    if initial_guess is None:
        # Very rough heuristics:
        kappa0 = 0.5
        theta0 = -np.log(market_prices[-1]) / maturities[-1]
        sigma0 = 0.01
        r0_0 = theta0
        initial_guess = np.array([kappa0, theta0, sigma0, r0_0])

    if bounds is None:
        # Reasonable positivity constraints for kappa, sigma
        bounds = [
            (1e-4, 5.0),   # kappa
            (-0.05, 0.10), # theta (can be negative)
            (1e-4, 0.5),   # sigma
            (-0.05, 0.10), # r0
        ]

    obj = lambda x: vasicek_loss_on_prices(x, maturities, market_prices, weights)

    res = minimize(
        obj,
        x0=initial_guess,
        bounds=bounds,
        method="L-BFGS-B",
    )

    kappa_hat, theta_hat, sigma_hat, r0_hat = res.x
    params_hat = VasicekParams(
        kappa=float(kappa_hat),
        theta=float(theta_hat),
        sigma=float(sigma_hat),
        r0=float(r0_hat),
    )

    info = {
        "success": bool(res.success),
        "message": res.message,
        "n_iter": res.nit,
        "final_loss": float(res.fun),
        "params_hat": asdict(params_hat),
    }
    return params_hat, info


# Optional: similar calibration for CIR (bonus)

def cir_loss_on_prices(
    x: np.ndarray,
    maturities: np.ndarray,
    market_prices: np.ndarray,
    weights: np.ndarray | None = None,
) -> float:
    """
    L2 loss between CIR model prices and market prices.
    """
    kappa, theta, sigma, r0 = x
    params = CIRParams(kappa=kappa, theta=theta, sigma=sigma, r0=r0)

    model_prices = _compute_model_prices(maturities, params, model_type="cir")

    if weights is None:
        weights = np.ones_like(model_prices)

    diff = model_prices - market_prices
    return float(np.sum(weights * diff**2))


def calibrate_cir(
    maturities: np.ndarray,
    market_prices: np.ndarray,
    initial_guess: np.ndarray | None = None,
    bounds: list[tuple[float, float]] | None = None,
    weights: np.ndarray | None = None,
) -> tuple[CIRParams, dict]:
    """
    Calibrate CIR parameters to market zero-coupon prices.
    """
    maturities = np.asarray(maturities, dtype=float)
    market_prices = np.asarray(market_prices, dtype=float)

    if initial_guess is None:
        kappa0 = 0.5
        theta0 = -np.log(market_prices[-1]) / maturities[-1]
        sigma0 = 0.05
        r0_0 = max(theta0, 1e-4)
        initial_guess = np.array([kappa0, theta0, sigma0, r0_0])

    if bounds is None:
        bounds = [
            (1e-4, 5.0),   # kappa
            (1e-4, 0.10),  # theta must be positive in CIR
            (1e-4, 1.0),   # sigma
            (1e-6, 0.10),  # r0 positive
        ]

    obj = lambda x: cir_loss_on_prices(x, maturities, market_prices, weights)

    res = minimize(
        obj,
        x0=initial_guess,
        bounds=bounds,
        method="L-BFGS-B",
    )

    kappa_hat, theta_hat, sigma_hat, r0_hat = res.x
    params_hat = CIRParams(
        kappa=float(kappa_hat),
        theta=float(theta_hat),
        sigma=float(sigma_hat),
        r0=float(r0_hat),
    )

    info = {
        "success": bool(res.success),
        "message": res.message,
        "n_iter": res.nit,
        "final_loss": float(res.fun),
        "params_hat": asdict(params_hat),
    }
    return params_hat, info
