# src/market_data.py

"""
Utilities to load and clean market zero-coupon yield curves.

The engine expects a CSV file with at least the following columns:
    - maturity_years: time to maturity in years (float)
    - zc_yield: annualized zero-coupon yield (in decimal, e.g. 0.02 for 2%)

The CSV can come from:
    - a simulated curve (for educational purposes),
    - a bootstrapped curve built from OAT / ESTR / swap quotes,
    - any other source, as long as the format is respected.

This module is deliberately simple: it does minimal cleaning
and basic sanity checks, and returns a tidy DataFrame that
other modules can consume.
"""

from typing import Tuple

import numpy as np
import pandas as pd


def load_zc_curve(path: str) -> pd.DataFrame:
    """
    Load a zero-coupon yield curve from a CSV file.

    Parameters
    ----------
    path : str
        Path to the CSV file with columns:
        - 'maturity_years'
        - 'zc_yield'

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with columns ['maturity_years', 'zc_yield'],
        sorted by maturity and with duplicated maturities removed.
    """
    df = pd.read_csv(path)

    required_cols = {"maturity_years", "zc_yield"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"CSV must contain columns {required_cols}, got {set(df.columns)}"
        )

    # Keep only the required columns and drop obvious garbage
    df = df[["maturity_years", "zc_yield"]].copy()
    df = df.dropna()
    df = df.drop_duplicates(subset="maturity_years")

    # Sort by maturity
    df = df.sort_values("maturity_years").reset_index(drop=True)

    return df


def clean_zc_curve(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """
    Apply simple cleaning rules to a zero-coupon yield curve.

    The goal is NOT to build a full professional bootstrapping
    pipeline, but to:
        - ensure maturities are strictly increasing,
        - optionally remove extreme outliers in yields.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with columns ['maturity_years', 'zc_yield'].

    Returns
    -------
    df_clean : pandas.DataFrame
        Cleaned curve.
    info : dict
        Metadata about cleaning operations (e.g. number of rows removed).
    """
    df = df.copy()

    if not {"maturity_years", "zc_yield"}.issubset(df.columns):
        raise ValueError("DataFrame must contain columns 'maturity_years', 'zc_yield'.")

    n_original = len(df)

    # Ensure maturities are > 0 and finite
    df = df[np.isfinite(df["maturity_years"]) & (df["maturity_years"] > 0)]

    # Remove extreme yield outliers using a simple IQR rule
    q1 = df["zc_yield"].quantile(0.25)
    q3 = df["zc_yield"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 3 * iqr
    upper = q3 + 3 * iqr
    df = df[(df["zc_yield"] >= lower) & (df["zc_yield"] <= upper)]

    # Sort again and drop duplicates just in case
    df = df.sort_values("maturity_years").drop_duplicates("maturity_years")
    df = df.reset_index(drop=True)

    n_clean = len(df)

    info = {
        "n_original": n_original,
        "n_clean": n_clean,
        "n_removed": n_original - n_clean,
        "outlier_yield_bounds": (float(lower), float(upper)),
    }

    return df, info
