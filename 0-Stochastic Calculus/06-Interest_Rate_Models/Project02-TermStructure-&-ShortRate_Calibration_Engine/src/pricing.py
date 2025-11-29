# src/pricing.py

"""
Pricing of simple interest-rate products from a zero-coupon curve
and calibrated short-rate models.

We provide:
    - pricing of zero-coupon bonds for arbitrary maturities,
    - pricing of simple FRAs,
    - pricing of plain-vanilla interest-rate swaps.
"""

from dataclasses import dataclass
from typing import Literal, Iterable

import numpy as np

from .ir_models import VasicekParams, CIRParams, zcb_price


@dataclass
class CalibratedModel:
    """
    Container for a calibrated short-rate model.

    Attributes
    ----------
    model_type : {'vasicek', 'cir'}
        Which model is used.
    params : VasicekParams or CIRParams
        Calibrated parameters.
    """
    model_type: Literal["vasicek", "cir"]
    params: VasicekParams | CIRParams


def price_zcb_from_model(
    maturities: Iterable[float],
    calibrated_model: CalibratedModel,
) -> np.ndarray:
    """
    Price zero-coupon bonds P(0, T) from a calibrated model.

    Parameters
    ----------
    maturities : iterable of float
        Maturities T_i (in years).
    calibrated_model : CalibratedModel
        Calibrated short-rate model.

    Returns
    -------
    prices : ndarray
        Zero-coupon prices P_model(0, T_i).
    """
    maturities = np.asarray(maturities, dtype=float)
    params = calibrated_model.params

    prices = np.array(
        [
            zcb_price(
                t=0.0,
                T=float(T),
                r_t=params.r0,
                params=params,
                model_type=calibrated_model.model_type,
            )
            for T in maturities
        ],
        dtype=float,
    )
    return prices


def forward_rate_from_zc(
    T1: float,
    T2: float,
    zc_price_T1: float,
    zc_price_T2: float,
) -> float:
    """
    Compute the simple forward rate F(T1, T2) implied by zero-coupon prices.

        1 + F * (T2 - T1) = P(0, T1) / P(0, T2)

    So:

        F = (P(0, T1) / P(0, T2) - 1) / (T2 - T1)

    Parameters
    ----------
    T1, T2 : float
        Start and end of the period, with T2 > T1.
    zc_price_T1, zc_price_T2 : float
        Zero-coupon prices P(0, T1) and P(0, T2).

    Returns
    -------
    float
        Forward rate F(T1, T2).
    """
    if T2 <= T1:
        raise ValueError("T2 must be > T1 for a forward rate.")

    delta = T2 - T1
    return (zc_price_T1 / zc_price_T2 - 1.0) / delta


def price_fra(
    T1: float,
    T2: float,
    K: float,
    notional: float,
    zc_price_T1: float,
    zc_price_T2: float,
) -> float:
    """
    Price a simple FRA (Forward Rate Agreement).

    We assume:
        - The underlying rate is the simple forward F(T1, T2).
        - The payoff is settled at T2 and equal to:
              notional * (F - K) * (T2 - T1)

    The present value under risk-neutral measure is:

        PV = P(0, T2) * notional * (F(T1, T2) - K) * (T2 - T1)

    Parameters
    ----------
    T1, T2 : float
        Start and end of the accrual period.
    K : float
        FRA fixed rate (strike).
    notional : float
        Notional amount.
    zc_price_T1, zc_price_T2 : float
        Zero-coupon prices P(0, T1), P(0, T2).

    Returns
    -------
    float
        Present value of the FRA (for the fixed-rate payer).
    """
    delta = T2 - T1
    F = forward_rate_from_zc(T1, T2, zc_price_T1, zc_price_T2)
    payoff_at_T2 = notional * (F - K) * delta
    pv = zc_price_T2 * payoff_at_T2
    return pv


def price_swap_vanilla(
    payment_times: np.ndarray,
    fixed_rate: float,
    notional: float,
    zc_prices: np.ndarray,
    T0: float = 0.0,
    payer: bool = True,
) -> float:
    """
    Price a plain vanilla interest-rate swap (fixed vs floating)
    using a zero-coupon curve.

    We assume:
        - payment_times = [T1, T2, ..., Tn], with T0 <= T1 < ... < Tn
        - accrual fractions are delta_i = T_i - T_{i-1} (simple year fraction)
        - floating leg is equivalent to:
              notional * (1 - P(0, Tn))  if starting at T0 = 0
          or, more generally, notional * (P(0, T0) - P(0, Tn))
        - fixed leg PV:
              notional * fixed_rate * sum_i delta_i P(0, T_i)

    For a payer swap (pay fixed, receive float), the value is:

        V_swap = PV_float - PV_fixed

    Parameters
    ----------
    payment_times : ndarray
        Payment dates [T1, ..., Tn].
    fixed_rate : float
        Fixed swap rate K.
    notional : float
        Notional amount.
    zc_prices : ndarray
        Zero-coupon prices P(0, T_i) for all payment_times.
    T0 : float, optional
        Start time of the swap. Default is 0.0.
    payer : bool, optional
        If True, value of a payer swap (pay fixed, receive float).
        If False, receiver swap (receive fixed, pay float).

    Returns
    -------
    float
        Present value of the swap.
    """
    payment_times = np.asarray(payment_times, dtype=float)
    zc_prices = np.asarray(zc_prices, dtype=float)

    if payment_times.shape != zc_prices.shape:
        raise ValueError("payment_times and zc_prices must have the same shape.")

    # Accrual factors (simple year fractions)
    times_full = np.concatenate([[T0], payment_times])
    deltas = np.diff(times_full)

    # Fixed leg PV
    pv_fixed = notional * fixed_rate * np.sum(deltas * zc_prices)

    # Float leg PV (standard approximation)
    P0_T0 = 1.0 if T0 == 0.0 else np.interp(T0, payment_times, zc_prices)
    P0_Tn = zc_prices[-1]
    pv_float = notional * (P0_T0 - P0_Tn)

    # Payer swap: receive float, pay fixed
    payer_value = pv_float - pv_fixed

    return payer_value if payer else -payer_value
