# src/ir_api.py

"""
API for the term-structure & short-rate calibration engine.

This is the entry point that a notebook or a simple dashboard would use.

Typical usage:
    - load a ZC curve from CSV,
    - convert yields to prices,
    - calibrate a Vasicek (or CIR) model,
    - generate model-implied term structure,
    - price simple FRAs and swaps for illustration.
"""

from typing import Literal

import numpy as np
import pandas as pd

from .market_data import load_zc_curve, clean_zc_curve
from .zc_curve import yields_to_prices, prices_to_yields
from .calibration import calibrate_vasicek, calibrate_cir
from .pricing import CalibratedModel, price_zcb_from_model, price_fra, price_swap_vanilla


def calibrate_short_rate_model(
    zc_curve_df: pd.DataFrame,
    model_type: Literal["vasicek", "cir"] = "vasicek",
    use_cleaned_curve: bool = True,
    **calib_kwargs,
):
    """
    Calibrate a short-rate model to a given zero-coupon yield curve.

    Parameters
    ----------
    zc_curve_df : DataFrame
        Must contain columns ['maturity_years', 'zc_yield'].
    model_type : {'vasicek', 'cir'}
        Which model to calibrate.
    use_cleaned_curve : bool, optional
        Whether to apply basic cleaning before calibration.
    **calib_kwargs :
        Extra keyword arguments forwarded to the calibration function
        (e.g. initial_guess, bounds).

    Returns
    -------
    calibrated_model : CalibratedModel
        Calibrated short-rate model.
    calib_info : dict
        Calibration diagnostics (final loss, success flag, etc.).
    curve_used : DataFrame
        The curve actually used in calibration (raw or cleaned).
    """
    if use_cleaned_curve:
        curve_used, clean_info = clean_zc_curve(zc_curve_df)
    else:
        curve_used = zc_curve_df.copy()
        clean_info = {"n_original": len(zc_curve_df), "n_clean": len(zc_curve_df)}

    maturities = curve_used["maturity_years"].to_numpy()
    yields = curve_used["zc_yield"].to_numpy()
    market_prices = yields_to_prices(maturities, yields)

    if model_type == "vasicek":
        params_hat, info = calibrate_vasicek(
            maturities=maturities,
            market_prices=market_prices,
            **calib_kwargs,
        )
    elif model_type == "cir":
        params_hat, info = calibrate_cir(
            maturities=maturities,
            market_prices=market_prices,
            **calib_kwargs,
        )
    else:
        raise ValueError("model_type must be 'vasicek' or 'cir'.")

    calibrated_model = CalibratedModel(model_type=model_type, params=params_hat)

    info["clean_info"] = clean_info

    return calibrated_model, info, curve_used


def analyze_term_structure(
    zc_curve_df: pd.DataFrame,
    calibrated_model: CalibratedModel,
):
    """
    Given a calibrated model and an input ZC curve, compute:

        - market ZC prices and yields,
        - model-implied ZC prices and yields (at same maturities),
        - simple diagnostics (RMSE on yields and prices).

    Parameters
    ----------
    zc_curve_df : DataFrame
        Curve with columns ['maturity_years', 'zc_yield'].
    calibrated_model : CalibratedModel
        Calibrated short-rate model.

    Returns
    -------
    result : dict
        Contains maturities, market/model prices and yields, and RMSE metrics.
    """
    curve = zc_curve_df.copy().sort_values("maturity_years")
    maturities = curve["maturity_years"].to_numpy()
    mkt_yields = curve["zc_yield"].to_numpy()

    # Market prices from yields
    mkt_prices = yields_to_prices(maturities, mkt_yields)

    # Model prices from calibrated model
    model_prices = price_zcb_from_model(maturities, calibrated_model)

    # Model yields inferred from model prices
    model_yields = prices_to_yields(maturities, model_prices)

    # Simple RMSE metrics
    rmse_prices = float(np.sqrt(np.mean((model_prices - mkt_prices) ** 2)))
    rmse_yields = float(np.sqrt(np.mean((model_yields - mkt_yields) ** 2)))

    result = {
        "maturities": maturities,
        "market_yields": mkt_yields,
        "market_prices": mkt_prices,
        "model_yields": model_yields,
        "model_prices": model_prices,
        "rmse_prices": rmse_prices,
        "rmse_yields": rmse_yields,
    }
    return result


def price_benchmark_products(
    calibrated_model: CalibratedModel,
    zc_curve_df: pd.DataFrame,
    notional: float = 1_000_000.0,
):
    """
    Price a few benchmark products using the model-implied term structure:

        - 5Y and 10Y zero-coupon bonds,
        - a simple FRA,
        - a 2Y vs 10Y plain vanilla swap.

    This is intentionally simple: the goal is to show that once you have
    a calibrated model, you can reconstruct a full curve and price things.
    """
    # Use maturities present in the DataFrame for ZC pricing
    curve = zc_curve_df.sort_values("maturity_years")
    maturities = curve["maturity_years"].to_numpy()

    # Model prices on these maturities
    model_prices = price_zcb_from_model(maturities, calibrated_model)

    # Helper to get P(0, T) at arbitrary T using interpolation
    def P_model(T: float) -> float:
        return float(np.interp(T, maturities, model_prices))

    # Example: 5Y and 10Y ZCB prices
    P_5Y = P_model(5.0)
    P_10Y = P_model(10.0)

    # Example FRA: from 1Y to 2Y
    T1, T2 = 1.0, 2.0
    P_T1 = P_model(T1)
    P_T2 = P_model(T2)
    # Suppose K is the market-implied forward (at-the-money FRA)
    F_12 = (P_T1 / P_T2 - 1.0) / (T2 - T1)
    fra_price = price_fra(T1, T2, K=F_12, notional=notional, zc_price_T1=P_T1, zc_price_T2=P_T2)

    # Plain vanilla swap 2Y vs 10Y with annual payments
    pay_times = np.arange(2.0, 10.0 + 1e-8, 1.0)  # 2,3,...,10
    zc_for_swap = np.array([P_model(T) for T in pay_times])
    # Set fixed rate = par swap rate (so PV ~ 0)
    deltas = np.diff(np.concatenate([[0.0], pay_times]))
    par_swap_rate = (1.0 - zc_for_swap[-1]) / np.sum(deltas * zc_for_swap)

    swap_value_payer = price_swap_vanilla(
        payment_times=pay_times,
        fixed_rate=par_swap_rate,
        notional=notional,
        zc_prices=zc_for_swap,
        T0=0.0,
        payer=True,
    )

    return {
        "P_5Y": P_5Y,
        "P_10Y": P_10Y,
        "FRA_1Y_2Y_ATM_price": fra_price,
        "par_swap_rate_2Y_10Y": par_swap_rate,
        "swap_value_payer_2Y_10Y": swap_value_payer,
    }
