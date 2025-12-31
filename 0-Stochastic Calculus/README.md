# Stochastic Calculus for Quantitative Finance

This chapter forms the mathematical and numerical backbone of the entire repository.  
It develops stochastic calculus from first principles to market-grade applications, following a coherent progression from discrete-time models to continuous-time dynamics, option pricing, credit risk, and portfolio-level simulations.

My objective is  to turn probabilistic models into working pricing, risk, and simulation engines, aligned with how quantitative finance is practiced in industry.

## Scope & Philosophy

Modern quantitative finance rests on a simple but powerful idea:  
prices evolve randomly, but not arbitrarily.

Here we explores how randomness, information, and no-arbitrage constraints interact to produce:
- fair prices,
- hedging strategies,
- risk measures,
- and structural market insights.

The content systematically bridges:
> **probability → stochastic processes → martingales → pricing → numerics → market applications**

Each section combines:
- rigorous mathematical foundations,
- explicit probabilistic intuition,
- and fully implemented numerical experiments in Python (and some MATLAB).

##  Topics & Structure

### 01 - Discrete-Time Models
Foundations of arbitrage-free pricing in discrete time:
- market formalism and self-financing strategies,
- martingales and risk-neutral measures,
- market completeness and replication,
- Cox–Ross–Rubinstein binomial model and convergence to Black–Scholes.

This section provides the cleanest environment to understand *why* pricing by expectation works.

### 02 - Optimal Stopping & American Options
When *timing* becomes the decision variable:
- stopping times and information flow,
- Snell envelope and optimal stopping theory,
- Doob–Meyer decomposition,
- dynamic programming on Markov chains,
- full American option pricing in CRR models.

The notebooks show how abstract stopping problems become executable pricing algorithms.

### 03 - Brownian Motion & Stochastic Differential Equations
The continuous-time foundation of quantitative finance:
- filtrations and adapted processes,
- Brownian motion and quadratic variation,
- continuous-time martingales,
- Itô integral and Itô calculus,
- SDEs and numerical schemes (Euler–Maruyama).

**Project A - Ornstein–Uhlenbeck Simulator**  
A standalone, market-facing simulator with:
- exact and Euler simulation,
- maximum likelihood calibration,
- real market data ingestion,
- scenario generation and forecasting.

### 04 - Black–Scholes, Volatility & Implied Dynamics
From diffusion models to observable market objects:
- GBM and risk-neutral dynamics,
- market completeness and replication,
- PDE formulation and Greeks,
- implied and local volatility,
- American exercise logic.

**Project B - Live Implied Volatility & VIX-like Engine**  
A practical volatility analysis engine:
- BS inversion to implied volatility,
- smile and surface construction,
- regime diagnostics,
- aggregation into a VIX-style index.

This chapter connects stochastic calculus directly to trading-desk workflows.

### 05 - Option Pricing & PDE Methods
Pricing as a boundary-value problem:
- Feynman–Kac representation,
- parabolic PDEs and generators,
- finite-difference schemes and stability,
- variational inequalities for American options.

**Project C -  Adaptive PDE Pricing Engine**  
An interactive solver for European and American options, designed to explore numerical behaviour and parameter sensitivity.

### 06 - Interest Rate Models
The quantitative structure of fixed income:
- yield curves and discounting,
- short-rate vs term-structure logic,
- Vasicek, CIR, affine pricing,
- introduction to HJM/BGM ideas.

**Project D - Term Structure & Short-Rate Calibration Engine**  
Calibration to real curves, pricing of ZC bonds, FRAs, swaps, and short-rate simulations.

### 07 - Asset Models with Jumps
Beyond continuous diffusion:
- Poisson and compound Poisson processes,
- jump–diffusion dynamics (Merton, Kou),
- martingale corrections and incompleteness,
- pricing and hedging under jumps.

**Project E - Jump–Diffusion Option Pricing Engine**  
Numerical PIDE solver, implied-volatility smiles, and model comparison across BS, Merton, and Kou frameworks.

### 08 - Credit Risk Models
From firm value to portfolio losses:
- structural default models (Merton, Black–Cox),
- intensity-based models and CDS calibration,
- copulas and default dependence.

**Project F - Credit Risk Engine**  
A full structural + reduced-form + copula-based framework producing:
PDs, CDS-implied intensities, correlated default simulations, VaR / ES, and systemic stress scenarios.

### 09 - Simulation & Algorithms
Monte Carlo as a pricing and risk engine:
- statistical convergence and confidence intervals,
- variance reduction techniques,
- hedging error under discrete rebalancing.

Includes both Python notebooks and MATLAB numerical experiments.

### 10 - Time Series & State-Space Models (FX Case Study)
A structural view of FX dynamics:
- ARIMA diagnostics and limitations,
- spectral and stationarity analysis,
- state-space models and Kalman filtering,
- latent macro trends vs observable noise.

A two-notebook case study on USD/JPY illustrating why latent-state models outperform classical time-series tools.

## References & Methodological Support

The theoretical development throughout this chapter is strongly inspired by:

**Damien Lamberton & Bernard Lapeyre**  
*Introduction to Stochastic Calculus Applied to Finance (2nd ed.)*  
Chapman & Hall / CRC Financial Mathematics Series

This reference provides exersices and the unifying framework linking probability, martingales, stochastic calculus, and financial applications, and serves me as a constant anchor between theory and implementation.

## Final Remark

This chapter is designed as a quantitative research purpose, not a collection of isolated notebooks.  
Each section prepares the ground for the next, and every project translates mathematics into executable models that reflect real market mechanisms.

If you as a reader, you understand this chapter, you understand why and how modern quantitative finance works, and where it breaks.

---

**Alexandre Mathias DONNAT, Sr**
