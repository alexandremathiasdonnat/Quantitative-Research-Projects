# Credit Risk Engine : Structural Default, CDS Calibration, Copula Portfolio Loss

Merton Structural Model • CDS Calibration • Copula Portfolio Simulation • VaR & ES • Sensitivity Analysis

## About

This project delivers a complete and customisable credit-risk engine for quant-credit / xVA-risk desks, that combines structural modelling (Merton), reduced-form CDS calibration, and copula-based portfolio simulation : from user-defined firm data and portfolio inputs, it computes default probabilities and distance-to-default, calibrates hazard rates from CDS spreads, simulates correlated default times through Gaussian and t-copulas, generates full loss distributions with VaR/Expected Shortfall, and evaluates systemic risk through sensitivity analysis and marginal risk contributions.

**Ready to use tool : engine packaged in a compact library I developed, easily driven through a simple pipeline:**

*inputs → run (backend engine) → calibrated PDs & intensities → portfolio default simulation → outputs (PD curves, λ, loss distribution, VaR/ES, sensitivities, MCR) (directly from the Jupyter dashboard)*


## What the Engine Does

### 1. Single-name credit (Structural + CDS)

Given firm-level parameters:

- Compute Merton structural PD (closed form + Monte Carlo)
- Compute Distance-to-Default
- Calibrate CDS-implied hazard rate λ*
- Compare structural vs reduced-form PD curves
- Visualize asset value distributions and stochastic paths

This answers:

- "What is the probability that this firm defaults within 1–10 years?"
- "What risk does the balance-sheet imply vs CDS markets?"

### 2. Portfolio credit risk (Gaussian & t-Copula)

From portfolio exposures, recoveries, maturities, and correlation:

- Simulate massive vectors of correlated default times
- Construct full loss distribution
- Compute VaR 99% and ES 97.5%
- Detect multi-default stress scenarios
- Compare Gaussian vs t-copula tail behaviour
- Highlight fat-tail amplification under low degrees of freedom

This replicates the logic used in credit portfolio risk desks, tranche pricing models, systemic stress-testing, and xVA/CVA analytics.

### 3. Sensitivities & Marginal Contribution to Risk

The notebook re-runs Monte-Carlo simulations under modified assumptions to quantify risk drivers:

- **ρ-sweep**: VaR sensitivity to correlation
- **df-sweep**: tail dependence under t-copula
- **λ-shock**: systemic intensity stress (+20%)
- **MCR**: name-level contribution to portfolio VaR (1% EAD bump)

This reveals:

- Which parameters drive tail risk the most?
- Which names contribute most to portfolio losses?
- How does systemic stress propagate through the portfolio?

## Mathematical Foundations

### Structural Model (Merton)

Equity = call option on firm assets:

$$dV_t = \mu V_t dt + \sigma_A V_t dW_t$$

Default at maturity if $V_T < D$.

Closed-form PD:

$$PD = \Phi(-DD), \quad DD = \frac{\ln(V_0/D) + (\mu - \sigma_A^2/2)T}{\sigma_A\sqrt{T}}$$

Also simulated with Monte-Carlo to validate behaviour.

### CDS Calibration (Reduced-Form)

Premium leg:

$$PL = s \sum_i \Delta_i P(\tau > T_i)$$

Protection leg:

$$\text{Prot} = (1-R) \int_0^T P(\tau > t) \lambda e^{-rt} dt$$

Solve for $\lambda$ such that $PL = \text{Prot}$.

Implied survival:

$$P(\tau > T) = e^{-\lambda T}$$

### Copula Default Simulation

Gaussian copula:

$$U = \Phi(ZL), \quad Z \sim N(0, I)$$

t-copula:

$$U = t_\nu(ZL)$$

Map uniforms to exponential times:

$$\tau_i = -\frac{1}{\lambda_i} \ln(1 - U_i)$$

Captures dependence of defaults and fat-tail clustering.

### Portfolio Loss & Risk Metrics

For each scenario:

$$L = \sum_i EAD_i (1 - R_i) \mathbb{1}_{\{\tau_i < T\}}$$

Compute:

- VaR 99%
- Expected Shortfall
- Stress clusters (≥3 defaults)
- Tail amplification (Gaussian vs t-copula)

## Project Architecture

```
src/
├── structural_model.py      # Merton structural PD, distance-to-default, MC simulation
├── cds_calibration.py       # Premium/protection legs, closed-form CDS calibration, λ-solver
├── hazard_models.py         # Exponential default-time model τ ~ Exp(λ)
├── copula_simulation.py     # Gaussian & t-copula correlated default generator
├── portfolio_losses.py      # Portfolio loss computation + VaR/ES + extreme scenario stats
├── credit_api.py            # High-level unified interface for dashboard calls
└── plotting.py              # All plots: PD curves, V_T histograms, loss distributions, etc.

data/
├── company_inputs.csv       # Firm-level inputs for Part 1 (Merton + CDS)
└── portfolio_inputs.csv     # Portfolio-level inputs for Part 2 & 3 (copulas + VaR/ES)

dashboard.ipynb              # Interactive end-to-end credit risk analysis tool
```
*The CSV files included in data/ are only templates, fully replaceable by a user own datasets, as long as they keep the same column structure (`company_inputs.csv` and `portfolio_inputs.csv`).*

## How to Use the Engine

Open the main dashboard: `dashboard.ipynb`

### 1. Set input parameters

```python
COMPANY_CSV = "./data/company_inputs.csv"
PORTFOLIO_CSV = "./data/portfolio_inputs.csv"

FIRM_NAME = "FirmA"

BASE_RHO = 0.3
N_SCENARIOS_PORTFOLIO = 20_000
N_SCENARIOS_COPULA_COMPARE = 20_000
N_SCENARIOS_SENSI = 10_000

RANDOM_STATE = 42
```

### 2. Run the notebook top-to-bottom

- **Part. 1**: compute PDs, lambdas, structural vs CDS curves
- **Part. 2**: simulate portfolio losses & obtain VaR/ES
- **Part. 3**: run sensitivities & MCR

### 3. Interpret the results

The dashboard automatically generates:

- company-level diagnostics
- portfolio loss histograms
- Gaussian vs t-copula comparisons
- correlation & tail-risk sensitivities
- name-level VaR contributions

## In short : generate all outputs at once

The dashboard produces three main outputs:

**Output 1 – Single-Name Credit Metrics**: Structural PD, CDS-implied intensity, distance-to-default, PD curves

**Output 2 – Portfolio Loss Distribution**: Gaussian vs t-copula, tail risk, multi-default clustering, VaR & ES

**Output 3 – Sensitivities & MCR**: Correlation sweep, df sweep, λ-shock, incremental VaR contributions

---
**Alexandre Mathias DONNAT, Sr**