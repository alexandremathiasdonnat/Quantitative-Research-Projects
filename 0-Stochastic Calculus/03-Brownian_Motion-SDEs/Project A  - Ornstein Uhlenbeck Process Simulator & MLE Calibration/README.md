# Ornstein–Uhlenbeck Process Simulator, Maximum Likelihood Calibration & Real-Market Applications

Mean-Reversion Dynamics • Exact Transition Density • MLE Estimation • Volatility Modeling • FX Analysis • Scenario Generation

## About

This project takes the Ornstein–Uhlenbeck (OU) process from theory to practice, following the ready-to-use pipeline:

**SDE → Simulation → Transition Density → MLE Calibration → Real Data Fitting → Scenario Generation**

It implements the mathematical foundations of the OU process, builds a robust maximum-likelihood estimator, and applies the calibrated model to live financial time series.

*The simulator is fully interactive:
each execution generates new OU paths, new future scenarios, and new distribution forecasts, allowing hands-on exploration of mean-reversion strength, equilibrium levels, and uncertainty propagation under the current market regime.*

**All parameters (θ, μ, σ) are calibrated in real time from freshly downloaded market data (S&P 500 realized volatility and EUR/USD FX), ensuring that every run reflects the most recent market conditions.**



## What this project covers

### OU Dynamics & Simulation

- Reminder of OU stochastic differential equation
- Euler–Maruyama discretization
- Multi-path simulation engine (`simulate_ou_process`)
- Visual inspection of sample trajectories

**Output:**  
A large set of OU sample paths + diagnostic plot to validate mean-reversion visually.

### Maximum Likelihood Estimation (MLE)

- Warm-up on Gaussian MLE
- Derivation of OU transition density
- Exact conditional mean/variance:

$$\mu_{t+\Delta t} = x e^{-\theta \Delta t} + \mu (1 - e^{-\theta \Delta t})$$

$$\sigma_{t+\Delta t}^2 = \frac{\sigma^2}{2\theta} (1 - e^{-2\theta \Delta t})$$

- Numerical log-likelihood
- L-BFGS-B optimization with positivity constraints
- Clean output formatting with LaTeX rendering

**Output:**  
Estimated parameters $\hat{\theta}, \hat{\mu}, \hat{\sigma}$ for any univariate time series.

## What the Simulator Does ? 

### 1. Application 1 — S&P 500 Realized Volatility

We compute rolling realized volatility from S&P returns, then estimate an OU model.

**Deliverables:**

- Historical volatility plot
- OU parameters (`theta_sp`, `mu_sp`, `sigma_sp`)
- Exact-distribution simulation at horizon T (PDF/KDE)
- Real vs OU Monte-Carlo path comparison
- Statistical match report (mean, std, skew, kurtosis)

**Output:**  
A validation that S&P 500 volatility exhibits mean-reversion and is reasonably captured by an OU model. (Excepting the 2008 and 2020 jumps but consistent)

### 2. Application 2 — EUR/USD FX Rate

Same full pipeline applied to FX spot levels (not returns).

**Deliverables:**

- EUR/USD historical plot
- Calibrated OU parameters
- Simulated future distribution
- Real vs OU path comparison
- Statistical fitting diagnostics

**Output:**  
A test showing that FX levels are weakly mean-reverting, with parameters reflecting slow decay and narrow stationary variance.

### 3. Scenario Generation & Time-Series Extension

A practical tool to extend any financial series into the future:

`simulate_and_concatenate_data(data, theta, mu, sigma)`

**Produces:**

- Historical data
- Simulated OU continuation
- Clean date index
- Vertical marker showing the transition point
- Highlighted simulation region

**Output:**  
An extended time series for what-if analyses, risk engines, and Monte-Carlo scenario generation.

## Main reusable functions of the tool

| Function | Purpose |
|----------|---------|
| `simulate_ou_process` | Euler discretization of OU paths |
| `simulate_continuous_ou_process` | Exact distribution at horizon T |
| `optimize_ou_parameters` | MLE via L-BFGS-B |
| `estimate_ou_parameters` | Clean wrapper returning LaTeX results |
| `simulate_and_compare_data` | Quantitative fit diagnostics (stats + plots) |
| `simulate_and_concatenate_data` | Extend real series with OU predictions |
| `plot_kde` | KDE + mode visualization for simulated distributions |

All functions are modular and ready for reuse on any others data (mean-reversion models, interest-rate modeling, factor models, etc.).

## Insights

- OU captures the mean-reverting nature of volatility very well.
- OU fits FX levels only partially, slow reversion and narrow dispersion.
- MLE on the exact transition density is fast, robust, and model-consistent.
- The scenario generator provides an easy way to run forward-looking stress tests.

---
**Alexandre Mathias DONNAT, Sr**
