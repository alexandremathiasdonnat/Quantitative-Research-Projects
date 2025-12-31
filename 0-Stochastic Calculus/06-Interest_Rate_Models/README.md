# 06 - Interest Rate Models

This chapter contains two complementary components:

## 1. Theory & Practice
Folder: `Theory/`

Two notebooks covering the theoretical foundations and practical mechanics of modern interest-rate modeling:

### 06.1 - Modelling Principles
Yield curves, discount factors, zero-coupon pricing, martingale measures, forward measures, and the conceptual bridge between short-rate models and the term structure.

### 06.2 - Some Classical Models
The core short-rate and forward-rate models used in practice: Vasicek, CIR, affine bond-pricing formulas, and an introduction to HJM/BGM frameworks.

These notebooks provide the mathematical and conceptual toolkit required to understand yield-curve construction, no-arbitrage constraints, and the dynamics of fixed-income markets.

## 2. Project D - Term-Structure Modeling & Short-Rate Calibration Engine/
Interactive calibration & pricing project

A standalone, fully replicable project: a Term-Structure & Short-Rate Calibration Engine built directly on top of the ideas from the Theory notebooks.

### Features
- Calibration of Vasicek or CIR to any market zero-coupon curve (CSV input).
- Estimation of parameters \((\kappa, \theta, \sigma, r_0)\) via loss minimization.
- Reconstruction of the model-implied term structure (ZC prices, yields, forwards).
- Comparison vs market (errors, diagnostics, plots).

### Pricing tools
- Zero-coupon bonds
- FRAs
- Plain-vanilla swaps (par rate, PV)
- Short-rate path simulation (Vasicek) and distribution plots
- Interactive dashboard notebook for immediate testing with any curve

### Purpose
A clean, practical environment to explore how short-rate models reproduce market yield curves, how calibration behaves, and how model-consistent pricing emerges from the underlying dynamics \(r(t)\).

**Alexandre Mathias DONNAT, Sr**
