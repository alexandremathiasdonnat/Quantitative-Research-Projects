# Live Implied Volatility Engine & VIX-like Dashboard

Live Market Data • Black–Scholes Inversion • Volatility Smiles • IV Surface • VIX-like Index 

## About

This project delivers a complete implied volatility analysis engine designed for volatility trading, equity derivatives, or any risk management workflows. Starting from a single user-input underlying ticker, the engine fetches live listed option prices, computes implied volatilities via Black–Scholes inversion, reconstructs volatility smiles and surfaces, and produces a VIX-like internal volatility index summarizing market-implied risk.

The dashboard operates on a live market snapshot: every execution re-extracts option chains and automatically recomputes all quantities updated, ensuring that outputs always reflect current market conditions.

**Ready to use tool : engine packaged in a compact library I developed, easily driven through a simple pipeline:**

The engine is packaged as a clean and modular library, driven through a simple interactive pipeline:

*inputs (ticker & market assumptions) → run (volatility engine) → implied volatility extraction → outputs (IV table, smiles, surface, VIX-like index)
(directly from the Jupyter dashboard)*

## What the Engine Does

1. **Live Option Data Extraction**  
    From a user-selected underlying ticker:  
    - Fetches live call and put option chains  
    - Computes spot price and time-to-maturity  
    - Filters illiquid, unstable, or unusable contracts  
    - Produces a clean cross-sectional option snapshot  
    This replicates the first step of professional volatility desk workflows.

2. **Implied Volatility Computation**  
    For each option contract:  
    - Inverts the Black–Scholes formula to recover implied volatility  
    - Handles numerical edge cases and theoretical inconsistencies  
    - Automatically discards contracts with invalid or non-invertible IVs  
    This yields a clean implied volatility table indexed by strike and maturity.

3. **Smiles & Term Structures**  
    The dashboard explores the cross-sectional structure of implied volatility:  
    - Volatility smiles: IV as a function of strike at a representative maturity  
    - Term structures: IV as a function of maturity at an at-the-money strike  
    - Call vs put IV comparisons to detect skew and directional asymmetries  
    When exact reference points are not available, the closest tradable contracts in the market snapshot are used.

4. **Implied Volatility Surface & Distribution**  
    Market-implied volatilities are interpolated onto a regular (strike, maturity) grid to reconstruct the full implied volatility surface. The dashboard visualizes:  
    - A 3D volatility surface  
    - A 2D heatmap  
    - The distribution of implied volatilities  
    These views highlight global structure, regime differences, and localized volatility spikes driven by market stress or limited liquidity.

5. **VIX-like Internal Volatility Index**  
    The entire volatility surface is compressed into a single VIX-like annualized volatility level, computed around a target maturity (e.g., 30 days). This index acts as an internal market fear gauge, summarizing the volatility expectations priced by options at the observation date.

## Mathematical Foundations

### Black–Scholes Implied Volatility

Option prices are inverted by solving
$$
C_{\text{market}} = BS(S_0, K, T, r, q, \sigma)
$$
for the implied volatility $\sigma$, using robust numerical root-finding methods with theoretical bounds. Contracts violating arbitrage bounds or suffering from microstructure noise are excluded.

### Volatility Surface Reconstruction

Given implied volatilities $(\sigma(K, T))$ observed on an irregular grid, the surface is reconstructed through interpolation on a regular grid:
$$
(K_i, T_j) \mapsto \sigma_{\text{interp}}(K_i, T_j)
$$
This provides a continuous representation suitable for visualization and aggregation.

### VIX-like Index (Simplified)

The VIX-like index aggregates near-the-money implied volatilities around a target maturity:
$$
\text{VIX}_{\text{int}} = \left(\sum_i w_i\,\sigma_i^2\right)^{1/2}
$$

where weights emphasize ATM options and contracts close to the target maturity.

## Project Architecture

```
src/
├── data_fetcher_yf.py     # Live option chain extraction & cleaning (Yahoo Finance)
├── implied_vol.py         # Black–Scholes pricing & implied volatility inversion
├── surface_builder.py     # IV surface interpolation & grid construction
├── vix_engine.py          # VIX-like volatility aggregation logic
├── plotting.py            # All visualization utilities
└── iv_api.py              # Unified high-level interface for the dashboard

dashboard.ipynb            # Interactive end-to-end volatility dashboard
```

## How to Use the Engine
1. Open `dashboard.ipynb`.
2. Set dashboard inputs (Section A):
    ```python
    ticker = "AAPL"
    preset = "robust"
    r = 0.02
    q = 0.00
    ```
3. Run the notebook top-to-bottom. Each execution:
    - Fetches live option data,
    - Recomputes implied volatilities,
    - Updates smiles, surfaces, and the VIX-like index.

4. Interpret output for any analysis

## In short : generate all outputs at once
The dashboard produces four main outputs:
- **Output 1 – Implied Volatility Table**: Clean IV snapshot across strikes and maturities  
- **Output 2 – Smiles & Term Structures**: Cross-sectional volatility diagnostics  
- **Output 3 – Distribution Diagnostics**: IV dispersion and outlier detection  
- **Output 4 – IV Surface & Heatmap**: Global volatility structure visualization  
- **Output 5 – VIX-like Index**: Single-number volatility stress indicator

---
**Alexandre Mathias DONNAT, Sr**

