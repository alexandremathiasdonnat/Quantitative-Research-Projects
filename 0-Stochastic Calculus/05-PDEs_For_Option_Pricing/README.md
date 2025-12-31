# 05 - Option Pricing & PDEs

This chapter contains two components:

## 1. Theory & Practice (folder: Theory/)

Three notebooks covering the full mathematical and numerical pipeline:

- **05.1** — Feynman–Kac, generators, valuation PDEs
- **05.2** — Numerical solution of parabolic PDEs (finite differences, θ-schemes, stability)  
- **05.3** — American options via variational inequalities (Brennan–Schwartz LCP)

They form the theoretical and practical core of PDE-based option pricing.

## 2. Project C - Black–Scholes Log-Space Finite-Difference PDE Pricer for European and American Options (Free-Boundary via Brennan–Schwartz Projection)/ (interactive project)

A standalone mini-project I developed: a pricing engine built on top of the algorithms from the Theory notebooks.

**Features:**

- Notebook-driven pricing dashboards (maturity, strike, volatility, rate, grid resolution)
- Finite-difference Black–Scholes PDE solver for European options
- American option pricing via Brennan–Schwartz projection
- Price curves and full numerical solution surfaces
- Lightweight, modular, and easy to experiment with

Designed to explore how PDE pricing reacts when parameters move — just adjust, run, and visualise.

**Alexandre Mathias DONNAT, Sr**
