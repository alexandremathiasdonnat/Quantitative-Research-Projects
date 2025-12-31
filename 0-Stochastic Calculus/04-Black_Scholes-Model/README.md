# 04 – Black–Scholes Model, Volatility & Implied Dynamics

This chapter contains two complementary components:

## 1. Theory & Practice

**Folder:** `Theory/`

Five notebooks developing the Black–Scholes framework from first principles, combining rigorous mathematics, numerical methods, and market-oriented interpretations.
Together, they explain how diffusion models, martingales, PDEs, and hedging arguments produce arbitrage-free option prices and volatility surfaces observed in real markets.

### Structure

| Notebook | Title | Core Idea |
|----------|-------|-----------|
| 04.1 | The Black–Scholes Model | Define GBM, solve the SDE explicitly, introduce risk-neutral measure, and show discounted asset prices are martingales. |
| 04.2 | Martingale Representation & Market Completeness | Any payoff can be replicated via stochastic integrals. Dynamic hedging and why Black–Scholes is a complete market. |
| 04.3 | European Options – PDE, Pricing, Greeks | Derive the BS PDE, solve it, obtain closed-form call/put prices, compute Greeks, and validate results via Monte Carlo. |
| 04.4 | American Options – Optimal Stopping | Early exercise logic, Snell envelope, backward induction, numerical free-boundary approximation. |
| 04.5 | Implied & Local Volatility | Invert BS to implied vol, construct smiles and surfaces, introduce local volatility (Dupire), and connect to VIX-like quantities. |

## 2. Project B – Live Implied Volatility Engine & VIX-like Index Dashboard

**Folder:** `Project B - Live Implied Vol Engine & VIX like Index Dashboard/`

A standalone, market-facing project that transforms Black–Scholes theory into a live implied volatility analysis engine.

The engine takes live real option market data as input and reconstructs the implied volatility structure used daily on trading desks.

### Core Features

- Numerical inversion of Black–Scholes prices to implied volatility
- Robust arbitrage filtering and sanity checks
- Construction of volatility smiles and full IV surfaces
- 3D surface and 2D heatmap visualisation
- Aggregation into a simplified VIX-like volatility index
- Distributional analysis of implied volatility regimes

### Outputs

- Implied volatility smiles across strikes and maturities
- Continuous IV(K, T) surface
- Heatmaps revealing regime shifts and term-structure effects
- Histogram diagnostics for outliers and volatility clustering
- Time-consistent, market-ready volatility snapshots

### Purpose

This project bridges:
**theory → numerics → market practice application and tool development**

It shows how Black–Scholes is used in reverse in practice, with implied volatility emerging as the true state variable and volatility surfaces feeding risk management, hedging, and local volatility models used on trading desks.
As the keystone of the framework, Chapter 04 connects stochastic calculus to real option prices, transforming abstract diffusion models into observable and tradable market objects.

---
**Alexandre Mathias DONNAT**
