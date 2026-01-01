# Project E - Jump–Diffusion PIDE Solving Engine for Option Pricing

*Merton & Kou Models | PIDE Solver | Volatility Smile Generation | Monte-Carlo Jump Simulation*

## About

*This project delivers a full, customisable jump–diffusion option pricing engine for equity/FX desks: from user-defined market/model parameters, it solves the PIDE, produces European option prices, generates jump-induced implied-volatility smiles, simulates discontinuous asset paths, and compares BS/Merton/Kou prices across multiple strikes and maturities.*

**Ready to use tool : engine packaged in a compact library, easily driven through a simple pipeline:**

*inputs → run (backend engine) → outputs (directly from the Jupyter dashboard).*

The engine supports three models:

- **Black–Scholes** (pure diffusion baseline)
- **Merton Jump–Diffusion** (Gaussian jumps)
- **Kou Double-Exponential Jump Model** (asymmetric, fat-tailed jumps)

It includes:

- a PIDE solver (finite-difference + integral jump terms),
- European call pricing surfaces,
- implied-volatility smiles under jump models,
- Monte-Carlo simulation of jump paths,
- pricing comparison tables across maturities and strikes.

This is the exact workflow used on equity/FX derivative desks to study jumps, skew, tail risk, and the structure of implied volatility.

## What the Engine Does

Given user-defined market and model parameters:

**Solve the PIDE**
- Crank–Nicolson scheme
- Fully explicit jump integral
- Boundary & terminal conditions for European calls

**Generate model price surfaces**
- 3D visualization of price vs time-to-maturity vs spot
- For BS, Merton, and Kou

**Compute implied-volatility smiles**
- Model IVs for a range of strikes
- Comparison against a reference flat BS vol
- Joint plot: BS vs Merton vs Kou

**Simulate jump–diffusion paths**
- Compound Poisson + diffusion
- 200 Monte-Carlo scenarios by default
- Side-by-side Merton vs Kou comparison

**Produce comparison tables**
- Price for multiple (T, K) pairs
- Shows how jumps reshape option values
- Very useful for understanding skew asymmetry & tail behaviour

## Mathematical Foundations

### 1. Models

**Black–Scholes**

$$dS_t = (r - q)S_t \, dt + \sigma S_t \, dW_t$$

**Merton Jump–Diffusion**

$$dS_t = (r - q - \lambda \mathbb{E}[e^Y - 1])S_{t-} dt + \sigma S_{t-} dW_t + S_{t-} dZ_t$$

with $Y \sim \mathcal{N}(\mu_J, \sigma_J^2)$

**Kou Double-Exponential Model**

$$Y \sim p \, \eta_1 e^{-\eta_1 y} \mathbf{1}_{y > 0} + (1 - p) \, \eta_2 e^{\eta_2 y} \mathbf{1}_{y < 0}$$

Allows large upward and downward jumps with different decay rates → realistic skew.

### 2. PIDE (pricing equation)

For a European call:

$$\frac{\partial U}{\partial t} + \mathcal{L}_{\text{diff}}[U] + \lambda \int_{\mathbb{R}} \left( U(Se^y, t) - U(S, t) \right) f_Y(y) \, dy = 0$$

Finite-difference + trapezoidal integration on $[y_{\min}, y_{\max}]$.

### 3. Simulation

For Merton:

$$\log S_T = \log S_0 + \left(r - q - \lambda \mathbb{E}[e^Y - 1] - \frac{1}{2}\sigma^2\right)T + \sigma W_T + \sum_{i=1}^{N_T} Y_i$$

For Kou: same structure but $Y \sim$ double-exponential.

## Project Architecture

```
src/
│
├── jump_models.py      # Merton & Kou characteristic functions, densities
├── integral_terms.py   # Discretised jump integrals for the PIDE
├── pide_operator.py    # Spatial finite-difference operators
├── pide_solver.py      # Crank–Nicolson time stepping + jumps
├── simulation.py       # Monte Carlo jump–diffusion paths
├── plotting.py         # Surfaces, smiles, path plots
└── pricing_api.py      # High-level pricing & smile generation interface

dashboard.ipynb         # Intuitive ready to use notebook
```

## How to Use the Engine

**Open the main dashboard:**
`dashboard.ipynb`

### 1. Set market & model parameters

```python
S0 = 100.0
r = 0.02
sigma_bs = 0.20
lam_merton = 1.0
lam_kou = 1.0
# etc.
```

### 2. Run Output 1 :  Price a call

```python
from src.pricing_api import price_option

res = price_option(
    model="Merton",
    S0=S0, K=100, T=1.0,
    r=r, q=0.0,
    sigma=sigma_bs,
    lam=lam_merton,
    mu_J=mu_J_merton,
    sigma_J=sigma_J_merton,
    **grid_kwargs
)

print(res["price_S0"])
```

### 2. Run Output 2 : Generate a volatility smile

```python
smile = generate_smile(
    model="Kou",
    S0=S0, strikes=[60,80,100,120,140],
    T=1.0, r=r, q=0.0,
    sigma=sigma_bs,
    lam=lam_kou,
    p=p_kou, eta1=eta1_kou, eta2=eta2_kou,
    grid_kwargs=grid_kwargs,
    plot=True
)
```

### 3. Run Output 3 : Simulate asset paths

```python
paths = simulate_jump_paths(
    model="Merton",
    S0=S0, T=1.0,
    r=r, q=0.0,
    sigma=sigma_bs,
    lam=lam_merton,
    mu_J=mu_J_merton,
    sigma_J=sigma_J_merton,
    n_paths=200, n_steps=252
)
```

###  In short : generate all outputs at once

The dashboard produces four outputs:

**Output 1 – Price & Surfaces** (3D surfaces for BS, Merton, and Kou.)

**Output 2 – Implied Vol Smiles** (BS (flat) vs Merton vs Kou.)

**Output 3 – Path Simulations** (Merton vs Kou, side-by-side.)

**Output 4 – Pricing Table** (Comparisons across (T, K).)

---

***Alexandre Mathias DONNAT, Sr***
