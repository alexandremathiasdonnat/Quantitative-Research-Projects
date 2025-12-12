# src/data_fetcher_yf.py
"""
Utilities to fetch and clean option chains from Yahoo Finance,
and convert them into a snapshot compatible with the IV dashboard.

Output format:
    K, T, option_type, market_price
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Tuple, List

import numpy as np
import pandas as pd
import yfinance as yf


def _get_spot_from_yf(ticker: str) -> float:
    """Fetch current spot price for the underlying."""
    tk = yf.Ticker(ticker)
    hist = tk.history(period="1d")
    if hist.empty:
        raise ValueError(f"No historical data for ticker {ticker}")
    return float(hist["Close"].iloc[-1])


def _process_chain(
    df: pd.DataFrame,
    option_type: str,
    expiry_str: str,
    today_utc: datetime,
) -> pd.DataFrame:
    """Convert a raw yahoo option chain (calls or puts) into a clean DF."""
    df = df.copy()
    df["option_type"] = option_type

    # Strike
    df["K"] = df["strike"]

    # Time to maturity (same expiry for the whole chain)
    expiry_dt = pd.to_datetime(expiry_str).tz_localize("UTC")
    T = (expiry_dt - today_utc).total_seconds() / (365 * 24 * 3600)
    df["T"] = T

    # Market price: mid of bid/ask, fallback lastPrice
    mid = (df["bid"] + df["ask"]) / 2
    df["market_price"] = mid.where(mid > 0, df["lastPrice"])

    # Basic cleaning: drop missing/zero prices
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["market_price"])
    df = df[df["market_price"] > 0.01]

    return df[["K", "T", "option_type", "market_price"]]


def fetch_options_snapshot(
    ticker: str,
    n_expiries: int = 8,              # plus de maturités → surface moins dégénérée
    min_T_days: int = 10,             # évite l'ultra short term (0–7 jours)
    max_T_days: int = 270,            # garde ~10 jours à 9 mois
    moneyness_band: Tuple[float, float] = (0.7, 1.3),  # vire les extrêmes
) -> Tuple[pd.DataFrame, float]:
    """
    Build a clean options snapshot for the given ticker.

    - Fetches up to n_expiries maturities
    - Keeps options with  min_T_days <= T <= max_T_days
    - Filters strikes by moneyness_band relative to spot
    - Returns (options_df, S0)

    options_df columns: K, T, option_type, market_price
    """
    today_utc = datetime.now(timezone.utc)
    tk = yf.Ticker(ticker)

    # 1) Spot
    S0 = _get_spot_from_yf(ticker)

    # 2) Available expiries
    expiries: List[str] = tk.options
    if not expiries:
        raise ValueError(f"No listed options for ticker {ticker}")

    # 3) Loop over first n_expiries, build chains
    all_rows = []
    for expiry in expiries[:n_expiries]:
        chain = tk.option_chain(expiry)
        calls = chain.calls
        puts = chain.puts

        if calls.empty and puts.empty:
            continue

        calls_df = _process_chain(calls, "call", expiry, today_utc)
        puts_df  = _process_chain(puts,  "put",  expiry, today_utc)

        all_rows.append(calls_df)
        all_rows.append(puts_df)

    if not all_rows:
        raise ValueError(f"No non-empty chains for ticker {ticker}")

    options_df = pd.concat(all_rows, ignore_index=True)

    # 4) Filter by time-to-maturity window
    options_df = options_df[
        (options_df["T"] * 365 >= min_T_days)
        & (options_df["T"] * 365 <= max_T_days)
    ]

    # 5) Filter by moneyness (relative to spot)
    options_df["moneyness"] = options_df["K"] / S0
    lo, hi = moneyness_band
    options_df = options_df[
        (options_df["moneyness"] >= lo) & (options_df["moneyness"] <= hi)
    ].copy()
    options_df = options_df.drop(columns=["moneyness"])

    # 6) Final sanity check
    if options_df.empty:
        raise ValueError(
            "No options left after cleaning. "
            "Try widening moneyness_band or T window."
        )

    return options_df, S0
