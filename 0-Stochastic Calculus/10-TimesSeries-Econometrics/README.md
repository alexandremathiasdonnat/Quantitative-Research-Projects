# 10 - Time Series (Structural & Dynamic Modeling of FX)

Hi there ! 👋

## About

*FX markets look chaotic at first glance : noisy, fast-moving, and seemingly unpredictable.
But beneath this turbulence lies a slow-moving macro structure that classical models fail to capture.*

This chapter is a two-notebook case study on USD/JPY, designed to bridge:

- what we see (noisy daily FX prices),
- what actually drives it (hidden economic trends),
- and what models can or cannot extract.

We combine classical time-series tools with state-space modeling and Kalman filtering to reveal both the limits of traditional methods and the strength of latent-state approaches.

## Content

The research motivation lean on two questions :

**What structure exists in FX price dynamics?**
: decomposition, seasonality, stationarity, ARIMA behavior, spectral signatures.

**Is there a hidden macro trend beneath the noise?**
: local level / local trend models, Kalman filtering & smoothing, regime interpretation, forecasting tests.

The two notebooks work together:

- **Notebook 10.1** diagnoses the observable data.
- **Notebook 10.2** uncovers the unobservable structure.

## Structure

| Notebook | Title | Core Idea |
|----------|-------|-----------|
| 10.1 | Structural Analysis of USD/JPY | A full structural diagnostics pipeline of the FX series. We perform STL decomposition, test stationarity using ADF and KPSS, inspect linear dependence via ACF/PACF, and follow the Box–Jenkins methodology: identification → estimation (via Maximum Likelihood) → residual diagnostics. We fit AR/MA/ARIMA models and analyze the spectral structure through periodogram and Fast Fourier Transform (FFT). We apply linear filters (moving averages, exponential smoothing) and illustrate the Slutzky–Yule effect. |
| 10.2 | Dynamic Modeling with State-Space & Kalman Filtering | Introduces a state-space formulation of FX dynamics with latent variables. We build local level and local linear trend models, define the transition and observation equations, and estimate hidden states using Kalman filtering and smoothing. We analyse process vs observation noise variances (Q and R), interpret them economically, and compare filtered vs smoothed states to detect structural regimes. ARIMA is re-expressed as a state-space benchmark, enabling direct comparison. Forecasting performance is evaluated through a train/test split, with 1-step-ahead predictions, RMSE/MAE metrics, and an empirical demonstration that models with latent trends outperform classical ARIMA.  |

## What we observe

### From Notebook 10.1

- FX prices drift with long macro cycles → non-stationary
- Returns behave almost like white noise
- ARIMA captures almost nothing beyond microstructure
- No meaningful seasonal or frequency components
- Smoothing can create spurious patterns

### From Notebook 10.2

- A clean latent level (structural FX value) emerges from Kalman filtering
- A stable macro trend governs long-term evolution
- Observation noise is small vs structural drift
- The local trend model outperforms ARIMA in forecasting
- Filtering ≈ smoothing, because the true signal is highly persistent

---

***Alexandre Mathias DONNAT, Sr***
