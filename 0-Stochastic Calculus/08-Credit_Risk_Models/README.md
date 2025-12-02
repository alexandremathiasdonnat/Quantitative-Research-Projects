# 08 - Credit Risk Models

Hi there! 👋

## About

*Credit risk modelling revolves around a deceptively simple question: when does a firm default, and how does that single event reshape the value of every liability it has issued?
Behind this question lies the entire architecture of modern credit theory — the timing of failure, the uncertainty around it, and the transmission of that uncertainty into bond prices, CDS spreads, and portfolio losses. What looks like a binary event becomes a continuous, probabilistic object that markets must price, hedge, and anticipate.*
This 8th chapter develops all three foundational approaches used in modern quantitative credit:

**Structural models (Merton, Black–Cox):**  
default arises from the firm's balance sheet and asset dynamics.

**Reduced-form / intensity models (hazard rates):**  
default is a surprise event governed by a stochastic intensity calibrated directly to CDS curves.

**Copula models for multi-name credit:**  
provide a dependence structure between several default times, essential for baskets, CDO tranches, and index products.

Each framework reflects a different market philosophy:

- **Structural** : economic story, equity/credit linkage, firm-value modelling.
- **Intensity** : market-implied survival probabilities, fast calibration, CDS-driven.
- **Copulas** : modelling joint defaults and tail dependence for portfolio credit products.

Together, they form the backbone of the pricing and risk analytics used in credit desks worldwide.

## Content

### Structural Credit Models (Merton & Black–Cox)
- GBM firm-value dynamics under the risk-neutral measure
- Equity as a call option; debt as risk-free bond minus put
- Closed-form default probabilities
- First-passage default with barriers (covenants)
- Survival via reflection principles
- Heatmaps and sensitivity analysis (V₀, σ)

### Intensity-Based Models (Reduced-Form)
- Hazard rates and survival probabilities
- Defaultable zero-coupon pricing
- CDS premium vs protection legs
- Piecewise-constant hazard calibration
- Cox-process simulation (CIR intensity + inverse integrated hazard)
- Numerical illustrations of survival curves, spreads, and defaultable ZC prices

### Copula Models for Multi-Name Credit
- Sklar's theorem and the separation of marginals vs dependence
- Gaussian copula and its limitations (no tail dependence)
- t-copula and fat-tailed joint defaults
- Archimedean copulas (Clayton, Gumbel, Frank)
- Tail dependence and systemic risk
- Simulation and visual comparison of dependence structures

## Structure

| Notebook | Title | Core idea |
|----------|-------|-----------|
| 08.1 | Structural Models – Merton & Black–Cox | Default arises from firm-value dynamics; equity = option, debt = contingent claim; first-passage vs terminal default. |
| 08.2 | Intensity-Based Credit Models | Default is a surprise event with a hazard rate λ(t); survival, CDS pricing, and stochastic intensity simulation. |
| 08.3 | Copulas for Multi-Name Credit | Construct joint laws of default times from market-calibrated marginals; Gaussian/t/Archimedean copulas and tail dependence. |

## Notes to viewers

Structural, reduced-form, and copula models respond to different modelling needs. Structural models provide intuition and explicit formulas, but are difficult to calibrate to market spreads. Reduced-form models sacrifice economic interpretation in favor of calibration speed and market consistency. Copulas complete the picture by allowing joint modelling of many obligors, critical for CDOs, baskets, and index tranches.

If you are discovering these ideas: move slowly between frameworks. Structural vs intensity vs copulas is not a continuum but three distinct modelling philosophies.

If you already know credit modelling: use this chapter to deepen intuition on tail dependence, first-passage vs terminal default, and the meaning of market-implied survival curves. Try stress-testing λ(t), simulating correlated defaults, or modifying the copula to explore systemic scenarios.

The code cells are light, practical, and extendable. You can add calibration routines, simulate large credit portfolios, compare tranche losses, or experiment with different copulas. The notebooks aim to bridge theory and practice in a concise, production-oriented format.

---

**Alexandre Mathias DONNAT, Sr**
