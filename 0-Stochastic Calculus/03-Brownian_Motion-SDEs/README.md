# 03 - Brownian Motion & SDEs

This chapter contains two complementary components:

## 1. Theory & Practice

**Folder:** `Theory/`

Five notebooks forming the mathematical and numerical foundations of continuous-time stochastic modelling.
This sequence builds everything needed to understand Brownian motion, Itô calculus, and SDEs — the pillars of all modern quantitative finance models.

### 03.1 – Continuous-Time Processes

Filtrations, adapted processes, stopping times.
First visual and conceptual intuition of randomness evolving in continuous time.

### 03.2 – Brownian Motion

Construction of $W_t$, Gaussian increments, scaling laws, quadratic variation.
Rigorous empirical tests and simulations validating theoretical properties.

### 03.3 – Continuous-Time Martingales

Martingale behaviour of key processes such as $W_t$, $W_t^2 - t$, and exponential martingales.
Optional stopping and martingale intuition in continuous time.

### 03.4 – Itô Integral & Itô Calculus

From simple processes to the full Itô integral.
Itô isometry, Itô's formula (1D and multi-dimensional), and applications to diffusions.

### 03.5 – SDEs & Numerical Schemes

Euler–Maruyama discretisation, strong/weak convergence, OU and GBM simulations.
Monte Carlo pricing under GBM and first contact with diffusion-based financial models.

These notebooks together form the theoretical toolkit that underpins Black–Scholes, Heston, OU models, term-structure models, stochastic volatility, and modern derivatives pricing.

## 2. Project A – Ornstein–Uhlenbeck Process Simulator & MLE Calibration

**Folder:** `Project A  - Ornstein Uhlenbeck Process Simulator & MLE Calibration/`

A standalone, interactive simulation project applying SDE theory to the Ornstein–Uhlenbeck mean-reverting process:

$$dX_t = \theta(\mu - X_t)\,dt + \sigma dW_t$$

This project transforms OU theory into a calibrated, real-time simulation tool directly driven by live financial data.

### Features

- **Exact & Euler simulation** of OU paths
- **Maximum Likelihood Estimation** of $(\theta, \mu, \sigma)$
- **Real-time calibration** from freshly downloaded market data (S&P 500 realized volatility, EUR/USD FX)
- **Exact transition-density sampling** for future forecasting
- **Real vs simulated path comparison**
- **Scenario extension:** historical series + OU-simulated future
- **Fully interactive simulator:** every run produces different future paths and distributions

### Outputs

- Calibrated OU parameters (mean-reversion speed, long-run level, diffusion)
- Predictive distribution of $X_T$ via exact OU transition density
- Overlay plots comparing true market behaviour vs OU dynamics
- Long-horizon scenarios illustrating drift, reversion, or instability
- Full extended time series combining history and simulated future

### Purpose

This project offers a clean, practical environment to understand, calibrate, and exploit mean-reverting processes — central to:

- volatility modelling
- interest-rate term-structure (Vasicek, CIR)
- FX macro modelling
- spreads & statistical arbitrage
- Monte Carlo risk simulations

It bridges:
**theory** (Brownian motion, Itô calculus, SDEs) TO **numerics** (Euler, MLE, Monte Carlo) TO **real market application** (calibration, forecasting, scenario generation).

---

*Alexandre Mathias DONNAT, Sr*

