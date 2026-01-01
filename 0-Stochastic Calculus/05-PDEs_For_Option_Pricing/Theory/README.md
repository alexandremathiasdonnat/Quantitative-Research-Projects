# 05 - Option Pricing & Partial Differential Equations

**Hi there! 👋**

## About

*In this 5th chapter, we step inside the pricing engine that powers modern quantitative finance: where stochastic calculus meets PDEs, where expectations become equations, and where the mathematics of diffusion models transforms directly into the surfaces traders use every day.*

*From Feynman–Kac to finite differences, from European PDEs to American variational inequalities, and from localisation tricks to exercise boundaries, this section shows how the pricing engine actually works under the hood.*

If Chapter 4 built the probabilistic backbone of Black–Scholes,
Chapter 5 turns it into a complete analytical + numerical pipeline.

## Content

This chapter is split into three notebooks, each one building directly on the previous.

| Notebook | Title | Core Idea |
|----------|-------|-----------|
| 05.1 | European Option Pricing & Diffusions | Feynman–Kac, infinitesimal generators, valuation PDEs. Link between probabilistic expectations and analytical PDE solutions. |
| 05.2 | Solving Parabolic PDEs Numerically | Finite difference discretisation, θ-schemes, stability, tridiagonal solvers, Black–Scholes PDE in log-space. |
| 05.3 | American Options & Variational Inequalities | Snell envelope → LCP formulation → Brennan–Schwartz method. Optimal exercise boundary and comparison with CRR. |

Across these notebooks, we unify:

- stochastic calculus (Itô, generators, martingales),
- PDE theory (parabolic equations, boundary conditions, variational inequalities),
- numerical methods (finite differences, localisation, tridiagonal solvers),
- practical pricing tools (American puts, exercise boundaries, European benchmarks).

## Interactive Pricing Engine (custom quantitative library)

In addition to the three notebooks, this chapter includes a small pricing engine I developed myself:

- fully interactive,
- parametric inputs for maturity, strike, volatility, rates, grid sizes,
- numerical solver built on top of the algorithms from 05.2 and 05.3,
- outputs both prices and full numerical surfaces.

For now, the engine supports:

- European call (vanilla) via the BS PDE,
- American put (vanilla) via the Brennan–Schwartz LCP solver.

It is intuitive, lightweight, and easy to play with if you want to explore how numerical pricing behaves when parameters move.

## Why this chapter matters

Modern desks rely heavily on numerical PDEs:

- whenever implied volatility surfaces must be transformed into local volatility dynamics,
- whenever a payoff has early exercise, barriers, constraints, path-dependence, or no closed form,
- whenever calibration requires fast computation of full price grids,
- whenever Greeks must be computed consistently with the model dynamics.

## Notes to viewers

Feel free to adapt these notebooks depending on your background.

If you're new to PDEs, take your time: localisation, stability constraints, and discretisation choices take a bit of practice. But seeing the price surface evolve through time makes everything click.

If you already know the theory, challenge the notebooks:
try different schemes, stress the stability limits, or increase space/time resolution to see convergence and failures.

All notebooks use only standard Python tools (NumPy, Matplotlib, SciPy), so you can experiment freely or extend them with your own pricing routines (e.g., barriers, rebates, local vol, Heston PDE).

---

***Alexandre Mathias DONNAT, Sr***
