# 07 – Asset Models with Jumps

**Hi there! 👋**
## About
*Real markets don’t move smoothly. Prices gap on earnings releases, crash on unexpected news, and react instantly to macro events. These discontinuities break the continuous geometry of Brownian diffusions, and that’s where jump–diffusion models enter.*

*In this chapter, we enrich the classic Black–Scholes world by superimposing Poisson jumps on the diffusion dynamics. The consequences are fundamental: replication stops working, the market becomes incomplete, and pricing no longer relies on perfect hedging but on choosing an equivalent martingale measure. Jump sizes, jump intensities, and compensated Poisson integrals become part of the modelling toolkit.*

What emerges is the full structure behind Merton-style models: explicit SDE solutions mixing diffusion and multiplicative jumps, martingale drift corrections, mixture formulas for European options, and hedging strategies that minimise quadratic risk in markets where perfect hedging is impossible.

Jump models are the natural first step toward more realistic return distributions, volatility skews, and fat tails (all core features of equity markets).

## Content
- Poisson processes and compound Poisson constructions
- Jump–diffusion SDEs and the Merton model
- Explicit asset-price solutions: diffusion × jump multipliers
- Martingale conditions and compensated Poisson integrals
- Girsanov for the diffusion part; incomplete-market pricing
- Mixture formulas for European options (Merton series)
- Risk-minimising hedging and comparison to Black–Scholes delta
- Monte Carlo simulations and hedging-error illustrations

## Structure
| Notebook | Title                          | Core idea                                                                 |
|----------|--------------------------------|---------------------------------------------------------------------------|
| 07.1     | Poisson & Compound Poisson     | Build the jump mechanism: exponential waiting times, Poisson counts, random jump amplitudes. |
| 07.2     | Jump–Diffusion Dynamics        | Define Merton’s model, derive explicit solutions, understand diffusion × jump decomposition. |
| 07.3     | Martingales in Jump–Diffusion  | Compute the drift ensuring discounted prices are martingales; introduce compensated Poisson integrals. |
| 07.4     | Pricing & Hedging              | Change measure, price via expectations, derive the Merton mixture formula, and compute quadratic-risk optimal hedges. |

## Notes to viewers
Feel free to navigate the notebooks at your own pace. Jump models introduce concepts that differ sharply from pure diffusions: paths become discontinuous, markets become incomplete, and martingale conditions involve both drift and jump compensators. If you are discovering these ideas, take it slow, intuition grows quickly once you see simulations of jump paths and how they impact pricing.

If you already know diffusion models well, use this chapter to deepen your understanding of incompleteness: compare Black–Scholes delta vs jump-aware hedging, experiment with how jump intensity affects implied-volatility skews, or implement the full Merton series numerically.

The code cells are light and extendable. You can add Monte Carlo calibrations, compute hedging P&L distributions, or modify the jump-size distribution to test how pricing reacts. Warnings are disabled at the top of the notebooks for cleaner output.

**Alexandre Mathias DONNAT, Sr**
