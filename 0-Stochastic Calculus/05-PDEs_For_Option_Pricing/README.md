# 05 – Option Pricing & PDEs

This chapter contains two components:

## 1. Theory & Practice (folder: Theory/)

Three notebooks covering the full mathematical and numerical pipeline:

- **05.1** — Feynman–Kac, generators, valuation PDEs
- **05.2** — Numerical solution of parabolic PDEs (finite differences, θ-schemes, stability)  
- **05.3** — American options via variational inequalities (Brennan–Schwartz LCP)

They form the theoretical and practical core of PDE-based option pricing.

## 2. P1-Adaptive_PDE_solvers/ (interactive project)

A standalone mini-project I developed: a pricing engine built on top of the algorithms from the Theory notebooks.

**Features:**

- Fully interactive solver (maturity, strike, vol, rate, grid sizes, etc.)
- Numerical BS PDE solver (European call)
- Brennan–Schwartz LCP solver (American put)
- Price curves + full numerical surfaces
- Intuitive, lightweight, easy to experiment with

Designed to explore how PDE pricing reacts when parameters move — just adjust, run, and visualise.

**Alexandre Mathias DONNAT, Sr**
