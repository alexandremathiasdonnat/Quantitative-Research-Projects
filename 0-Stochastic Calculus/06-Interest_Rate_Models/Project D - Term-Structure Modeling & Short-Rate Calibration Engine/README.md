# Project D - Term-Structure Modeling & Short-Rate Calibration Engine

**Vasicek & Cox-Ingersoll-Ross Models | Yield-Curve Fitting | IR Product Pricing | SDE Simulation**

## About

*A powerful and fully replicable engine that, from any zero-coupon curve, calibrates a chosen short-rate model (Vasicek or CIR), reconstructs the full term structure (closed-form ZC formulas, parameter estimation, loss minimisation), and delivers model-consistent pricing and rate dynamics through an interactive dashboard : a practical tool for IR desks, where understanding and modelling the short rate 𝑟(𝑡) is central since it directly influences the valuation of fixed-income instruments while evolving over time.*

Starting from a market zero-coupon yield curve (CSV input), the engine:
- Converts yields into zero-coupon prices
- Calibrates a one-factor short-rate model: (Vasicek or CIR : choice possibilty)
- Reconstructs the model-implied term structure
- Compares model vs market (errors, plots, diagnostics)
- Prices basic fixed-income products: (Zero-coupon bonds, FRAs, Plain-vanilla swaps)
- Simulates short-rate paths using exactly the calibrated SDE parameters
    (simulation & distribution shown only for Vasicek choice in the notebook for clarity and lightness)

**Key idea 1:** the calibration output $(κ^*, θ^*, σ^*, r_0^*)$ are exactly the parameters of the SDE.

**Key idea 2:** the simulation of $r_t$ uses these same calibrated parameters, ensuring full model consistency.

It is a compact, industry-style implementation of the core IR modelling concepts: short-rate dynamics, bond pricing under $\mathbb{Q}$, calibration, and term-structure analysis.

## Mathematical Foundations

### 1. Short-rate dynamics

**Vasicek (Gaussian)**

$$dr_t = κ(θ - r_t)dt + σdW_t$$

Closed-form ZC price:

$$P(0,T) = A(0,T)e^{-B(0,T)r_0}$$

with

$$B(0,T) = \frac{1-e^{-κT}}{κ}$$

**CIR (square-root)**

$$dr_t = κ(θ - r_t)dt + σ\sqrt{r_t}dW_t$$

Closed-form ZC price:

$$P(0,T) = A(0,T)e^{-B(0,T)r_0}$$

with

$$γ = \sqrt{κ^2 + 2σ^2}$$

### 2. Calibration objective

Given market ZC prices $P^{mkt}(0,T_i)$:

$$\text{Loss}(κ,θ,σ,r_0) = \sum_i \left(P^{model}(0,T_i) - P^{mkt}(0,T_i)\right)^2$$

The engine minimizes this loss (L-BFGS-B) to obtain calibrated SDE parameters $(κ^*, θ^*, σ^*, r_0^*)$.

### 3. IR product pricing (using ZC curve)

**Forward rate**

$$1 + F(T_1,T_2)(T_2-T_1) = \frac{P(0,T_1)}{P(0,T_2)}$$

**FRA payoff**

$$\text{PV} = P(0,T_2)(F-K)(T_2-T_1) \cdot \text{Notional}$$

**Swap fixed leg**

$$\text{PV}_{fixed} = K\sum_i Δ_i P(0,T_i)$$

**Floating leg**

$$\text{PV}_{float} = 1 - P(0,T_n)$$

### 4. Short-rate simulation

Using the calibrated SDE parameters:

$$dr_t = κ(θ - r_t)dt + σdW_t$$

Euler discretization generates:
- future rate distributions
- risk & stress scenarios
- Monte Carlo validation of ZC pricing

## Project Architecture

```
data/
└── eur_zc_curve.csv     # Any curve with same structure will work

src/
│
├── market_data.py        # Load & clean market ZC curves
├── zc_curve.py           # Yield↔Price conversions, curve interpolation
├── ir_models.py          # Vasicek & CIR closed-form formulas
├── calibration.py        # Optimization routines, loss functions
├── pricing.py            # ZCB, FRA, swap pricing tools
├── plotting.py           # Term-structure & error plots
└── ir_api.py             # High-level calibrate() & analyze() interfaces

dashboard.ipynb   # Dashboard notebook
```

##  Input

Any CSV with the following structure works with my engine :

```csv
maturity_years,zc_yield
0.5,0.015
1.0,0.017
2.0,0.019
5.0,0.021
10.0,0.023
20.0,0.024
```

**Requirements:** maturities in years, yields in decimal (0.02 = 2%)

The dashboard automatically adapts to any other curve with this schema.

With real-time market data feeds, this engine could be used to continuously recalibrate Vasicek/CIR parameters and update all interest-rate-dependent product prices in real time.

Similar engines could be built for HJM models (direct modelling of the entire forward-rate curve under no-arbitrage) and LIBOR Market Models (multi-factor GBM dynamics for forward LIBORs). These frameworks offer greater realism but require substantially more mathematical and numerical complexity.

## How to Use the Engine

### 1. Load the curve (trough any .csv)
```python
from src.market_data import load_zc_curve
zc_df = load_zc_curve("data/my_curve.csv")
```

### 2. Calibrate Vasicek or CIR (can be chosen)
```python
from src.ir_api import calibrate_short_rate_model

calibrated_model, info, curve_used = calibrate_short_rate_model(
     zc_curve_df = zc_df,
     model_type = "vasicek",   # or "cir"
)
```

**Outputs:**
- calibrated SDE parameters
- optimization diagnostics
- cleaned curve used in calibration

### 3. Analyze the term structure
```python
from src.ir_api import analyze_term_structure
analysis = analyze_term_structure(zc_df, calibrated_model)
```

It get:
- model vs market yields
- model vs market ZC prices
- RMSE diagnostics

### 4. Price products
```python
from src.ir_api import price_benchmark_products
bench = price_benchmark_products(calibrated_model, zc_df)
print(bench)
```

### 5. Simulate short-rate paths (Vasicek only in notebook)
```python
t_grid, r_paths = simulate_vasicek_paths(
     calibrated_model.params,
     T=10,
     n_steps=250,
     n_paths=2000
)
```

## Outputs

- Calibrated parameters (kappa, theta, sigma, r0)
- Model-implied yield curve
- Market vs model comparison plots
- Zero-coupon, FRA, swap pricing
- Short-rate path simulations (Vasicek)
- Distribution of future rates (histograms)

**Examples:**
- FRA ATM → PV ≈ 0
- Par swap rate recovered automatically
- Paths mean-revert toward the calibrated long-term mean θ*

**Alexandre Mathias DONNAT, Sr**
