# Projet G - Optimal Portfolio Allocation Engine via Hamilton–Jacobi–Bellman (Stochastic Control, PDE-based)

Stochastic Control • HJB Equation • CRRA Utility • Transaction Costs • Buy-Side Strategy Comparison

## About

This project delivers a research-oriented portfolio allocation engine designed to study dynamic asset allocation under uncertainty using stochastic control techniques.

Starting from a single set of user-defined inputs (market assumptions, investor preferences, and implementation constraints), the engine computes the theoretically optimal allocation policy via solving the HJB equation, implements this policy in a realistic trading environment, and benchmarks it against standard buy-side allocation strategies. The objective is allocation interpretation: understanding how different portfolio rules perform net of transaction costs, when evaluated through an investor's expected utility. This tool can serve as a foundational building block for portfolio research, systematic asset management, and quantitative hedge fund applications. A dedicated `constraints.txt` file is included to provide some classical predefined parameter configurations (market regimes, investor profiles, and implementation constraints) that can be directly applied to the dashboard input section.

**Ready to use research tool : engine is packaged as a clean, modular library, fully driven through a single interactive Jupyter dashboard:**

*inputs (market & investor assumptions) → HJB resolution (theoretical benchmark) → strategy implementation & simulation → risk, performance & utility comparison across strategies*


All strategies are evaluated on the same simulated market scenarios, ensuring full statistical fairness.

## What the Engine Does

### Market & Investor Modeling

Continuous-time market with:

- one risky asset (GBM with constant drift and volatility),
- one risk-free asset.

Investor preferences modeled via CRRA utility.

Configurable:

- risk aversion,
- investment horizon,
- leverage / short-selling constraints,
- transaction costs.

### HJB Optimal Allocation (Theoretical Benchmark)

Solves the Hamilton–Jacobi–Bellman equation backward in time.

Computes:

- the value function $V(t,W)$,
- the optimal policy $\pi^*(t,W)$.

Produces a state-dependent allocation rule as a function of time and wealth.

This policy represents the theoretical optimum in a frictionless setting and serves as a benchmark, not a production strategy.

### Strategy Implementation & Simulation

All strategies are implemented on the same Monte Carlo paths:

- Buy & Hold
- Constant Mix
- Volatility Targeting
- Mean-Variance (static)
- Merton closed-form solution
- HJB optimal policy (implemented discretely)

Transaction costs are applied at the implementation stage, allowing a clear comparison between theory and practice.

### Buy-Side Evaluation Metrics

Each strategy is evaluated using:

- terminal wealth statistics,
- Sharpe ratio,
- maximum drawdown,
- quantiles (downside / upside),
- expected utility (decision criterion).

The dashboard also reports turnover diagnostics, revealing trading intensity and explaining sensitivity to transaction costs.

## Mathematical Foundations

### Stochastic Control & HJB

The portfolio optimization problem is formulated as a continuous-time stochastic control problem.
The value function satisfies the HJB equation:

$$0 = V_t + \max_{\pi} \left[(\pi\mu + (1-\pi)r)WV_W + \frac{1}{2}\pi^2\sigma^2W^2V_{WW}\right]$$

with terminal condition:

$$V(T,W) = U(W)$$

### Utility-Based Decision Making

The final decision criterion is expected utility, not raw return:

$$E[U(W_T)]$$

This ensures:

- full distributional comparison,
- consistency with investor risk preferences,
- alignment with buy-side decision frameworks.

## Project Architecture

```
root/
    src/
    ├── market_models.py     # Market dynamics (GBM, wealth evolution)
    ├── utility.py           # CRRA utility and derivatives
    ├── hjb_equation.py      # Formal HJB construction
    ├── hjb_solver.py        # Finite-difference HJB solver
    ├── policies.py          # Buy-side benchmark strategies
    ├── simulation.py        # Monte Carlo wealth simulation
    ├── evaluation.py        # Risk, performance & utility metrics
    ├── portfolio_api.py     # Unified high-level engine interface
    └── plotting.py          # All visualization utilities

└── constraints.txt          # Suggested market, investor, and constraint configurations

└── dashboard.ipynb          # Interactive end-to-end dashboard
```

## How to Use the Dashboard

1. Open `dashboard.ipynb`.

2. Modify only the Input Parameters section:
    - market assumptions,
    - investor risk aversion,
    - constraints and costs,
    - numerical resolution.

3. Run the notebook top-to-bottom.

Each execution:

- resolves the HJB equation,
- simulates all strategies,
- updates plots and metrics automatically.

## In short : generate all outputs at once

The dashboard produces three main outputs:

**Output 1 — HJB Optimal Policy**
Theoretical optimal allocation $\pi^*(t,W)$.

**Output 2 — Strategy Simulation & Diagnostics**
Wealth trajectories, terminal distributions, and turnover diagnostics.

**Output 3 — Strategy Comparison Table**
Final buy-side metrics with expected utility as the decision criterion.

## Observations

Across multiple runs and parameter configurations, the results consistently show that highly adaptive allocation rules, such as the HJB policy, tend to generate significant trading intensity and are therefore strongly penalized once transaction costs are introduced.
In contrast, simpler strategies with stable allocations (e.g. Merton or volatility targeting) exhibit much greater robustness and often dominate in terms of expected utility.

These observations highlight the gap between theoretical optimality and practical implementability, and emphasize that, in the current engine setup, turnover control is a key driver of performance

## Going Further

In its current version, the engine is intentionally designed to study portfolio allocation under uncertainty with fixed market assumptions, using the HJB solution as a theoretical benchmark rather than a production-ready strategy.

In a more advanced research setting, this same pipeline could be extended to test more elaborate allocation mechanisms, for example by introducing stochastic volatility (making volatility-targeting strategies dynamic), rolling or adaptive parameter estimation, multi-asset portfolios with time-varying covariance structures, or time-varying alpha signals driving risk allocation decisions.

In practice, the HJB framework typically remains a conceptual reference point, while implementable strategies are built as constrained, regularized, or approximated versions that explicitly control turnover, risk budgets, and trading frictions.
These extensions are deliberately outside the scope of this project, whose objective is to provide a clean, interpretable foundation for portfolio research, not a fully industrialized trading system.

---
**Alexandre Mathias DONNAT**
