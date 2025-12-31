# 08 - Credit Risk Models

This chapter contains two complementary components:

## 1. Theory & Practice

**Folder:** `Theory/`

Three notebooks introducing the full mathematical framework of modern credit risk modelling, from firm-value dynamics (structural), to hazard-rate calibration (intensity), to dependence structures for multi-name portfolios (copulas).

### 08.1 – Structural Models (Merton & Black–Cox)

Builds the micro-economic foundations of default: the firm value follows a GBM under the risk-neutral measure, equity appears as a call option on the firm's assets, and debt becomes a contingent claim.
Default occurs when $V_T < D$ (terminal case) or when $V_t$ touches a safety barrier (first-passage).
Outputs include closed-form structural PDs, distance-to-default, barrier-based survival via reflection arguments, and sensitivity heatmaps to initial firm value and volatility.

### 08.2 – Intensity-Based Credit Models (Reduced Form)

Default becomes a surprise event governed by a hazard rate $\lambda(t)$, producing survival:

$$S(t) = \exp\left(-\int_0^t \lambda(s) \, ds\right)$$

This framework yields defaultable zero-coupon pricing and the CDS premium–protection balance used to infer the market-implied intensity $\lambda^*$.
Illustrations include flat and piecewise-constant intensity curves, defaultable discount factors, and Monte-Carlo sampling of exponential default times.

### 08.3 – Copulas for Multi-Name Credit

Separates marginal PDs from their dependence using Sklar's theorem.
The Gaussian copula provides a baseline but no tail dependence; the t-copula introduces fat-tailed joint defaults; Archimedean copulas (Clayton, Gumbel, Frank) capture asymmetric dependence patterns.
Simulations highlight clustering, systemic behaviour, and why joint defaults cannot be inferred from marginals alone.

These notebooks together form the conceptual toolkit behind credit pricing, CDS calibration, and portfolio default modelling used by credit-quants, xVA teams, and systemic-risk supervisors.

## 2. Project F - Credit Risk Engine -  Structural Default, CDS Calibration & Copula-Based Portfolio Loss/

**Interactive structural + CDS calibration + copula simulation engine**

A standalone, ready-to-use project: a full credit risk engine through a library I developed that computes structural PDs, calibrates CDS-implied intensities, simulates correlated portfolio defaults, and estimates tail-risk metrics (VaR / ES) under Gaussian and t-copulas.

### Features

- Structural default modelling (Merton)
- CDS hazard-rate calibration (reduced form)
- Correlated default simulation via Gaussian & t-copulas
- Portfolio loss distribution, VaR 99%, ES 97.5%
- Extreme-scenario detection (multi-default events)

**Sensitivities:**
- Correlation sweep ($\rho \to$ VaR)
- t-copula tail-heaviness sweep (df $\to$ VaR)
- Systemic intensity shock (+20%)
- Marginal contribution to VaR (MCR)

### Outputs

- Per-firm structural PDs, distance-to-default, CDS-implied $\lambda^*$
- Structural vs CDS survival curves
- Portfolio loss histogram (Gaussian / t-copula)
- VaR & ES comparison across copulas
- Extreme-scenario statistics (≥3 defaults)
- Sensitivity tables ($\rho$-sweep, df-sweep)
- Name-level marginal risk contributions

### Purpose

This chapter provides a clean and practical environment to understand how firms default, how markets price this risk, and how default correlations generate fat-tailed portfolio losses.

It bridges : Theory (Merton, hazard rates, copulas), Numerics (Monte-Carlo simulation, calibration, dependence modelling), Industry practice (CDS calibration, portfolio VaR/ES, systemic risk stress-testing)

---

**Alexandre Mathias Donnat, Sr**
