# 07 – Asset Models with Jumps

This chapter contains two complementary components:

## 1. Theory & Practice

**Folder:** `Theory/`

Four notebooks introducing the full mathematical framework of jump–diffusion models, from Poisson mechanics to incomplete-market pricing.

### 07.1 – Poisson & Compound Poisson

Builds the jump structure itself: exponential waiting times, Poisson counts, jump amplitudes, and the compound Poisson process

$$Z_t = \sum_{j=1}^{N_t} U_j.$$

### 07.2 – Jump–Diffusion Dynamics

Introduces Merton's model and its explicit solution

$$S_t = S_0 \exp\left[(\mu - \lambda\kappa)t + \sigma W_t\right] \prod_{j=1}^{N_t} e^{Y_j},$$

and explains how diffusion × jumps interact.

### 07.3 – Martingales in Jump–Diffusion

Derives risk-neutral drift corrections

$$\tilde{\mu} = r - q - \lambda\left(\mathbb{E}[e^Y] - 1\right),$$

introduces compensated Poisson integrals, and explains why markets with jumps are incomplete.

### 07.4 – Pricing & Hedging in Jump–Diffusion

Pricing via expectations (Merton mixture formula), change of measure, and computation of quadratic-risk–minimising hedges when perfect replication is impossible.

**These notebooks provide the full conceptual and mathematical toolkit behind jump processes, incomplete markets, and the pricing mechanics of Merton/Kou-style models.**

---

## 2. Project03 – JumpDiffusion_OptionPricing_Engine/

**Interactive PIDE Pricing Engine**

A standalone, fully replicable project: a **Jump–Diffusion Option Pricing Engine** that solves the PIDE for European options under Merton and Kou models, compares with Black–Scholes, generates implied-volatility smiles, and simulates jump–diffusion paths.

### Features

- Fully customisable market & model inputs (spot, rates, vol, jump intensity, jump distribution).
- Solves the PIDE numerically (Crank–Nicolson scheme).
- Pricing under three models:
    - **Black–Scholes** (no jumps)
    - **Merton** (Gaussian jumps)
    - **Kou** (double-exponential jumps)
- Outputs:
    - PIDE price surfaces for each model
    - European call prices (at-the-money or any strike)
    - Implied-volatility smiles (BS vs Merton vs Kou)
    - Side-by-side simulation of Merton and Kou jump–diffusion paths
    - Model comparison table across strikes and maturities

### Purpose

A clean, practical environment to explore how jumps reshape option prices, fatten return tails, generate natural volatility smiles, and break perfect hedging.

This project mirrors real sell-side workflows: PIDE pricing, smile generation, model comparison, and stochastic scenario simulation.

## Why this Chapter Matters

Jump–diffusion models solve the biggest weakness of Black–Scholes: **markets jump**.

Earnings gaps, macro shocks, flash crashes, all introduce discontinuities that pure Brownian diffusions cannot represent.

This chapter develops both:

- **the theory** (Poisson processes, SDEs with jumps, martingale corrections, incomplete markets),
- **and the application** (PIDE engines, numerical schemes, implied smiles, Monte Carlo simulation).

It is a complete and industry-aligned introduction to modern models of market discontinuities.

---

**Alexandre Mathias DONNAT, Sr**
