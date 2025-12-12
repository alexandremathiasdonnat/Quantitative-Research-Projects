# Portfolio Optimization 

**Hi there! 👋**

*Portfolio construction is fundamentally a decision problem under uncertainty, where estimation error, regime shifts, and extreme events dominate theoretical optimality. While expected returns are highly unstable and difficult to exploit, risk measures such as volatility, correlations, and downside losses exhibit stronger persistence and structure. This module therefore focuses on robust, risk-aware allocation frameworks rather than return forecasting.*

This folder contains a set of research-oriented notebooks exploring portfolio optimization from a quantitative risk management perspective, combining convex optimization, risk budgeting, and tail-risk control under realistic constraints.

The objective here is to understand how portfolio allocations emerge from different risk objectives, how sensitive they are to estimation noise, and how they behave once embedded in a dynamic rebalancing process.This section complements both the stochastic calculus and machine learning components of the repository by translating model outputs into portfolio-level decisions.

## Practical

Portfolios are constructed using a consistent universe of liquid ETFs (e.g. SPY, TLT, GLD, QQQ, EFA, EEM, HYG), with allocations recomputed through rolling estimation windows. Static optimization methods (Mean–Variance, Risk Parity, CVaR) are subsequently embedded into a time-consistent backtesting framework, accounting for rebalancing frequency, turnover, and transaction costs.

## Content

| Notebook | Title | Core idea |
|----------|-------|-----------|
| 01 | Markowitz Mean–Variance Optimization | Classical portfolio theory: efficient frontier, minimum variance and tangency portfolios under convex constraints. |
| 02 | Risk Parity & Factor-Based Allocation | Risk budgeting approaches that avoid return forecasts, with asset- and factor-level risk contributions. |
| 03 | CVaR Optimization | Tail-risk–aware portfolio construction using scenario-based Expected Shortfall minimization. |
| 04 | Backtesting Strategies & Allocation Dynamics | Rolling allocation, transaction costs, turnover, and comparative performance analysis. |

## What is demonstrated

- Formulate portfolio allocation as convex optimization problems
- Understand the limits of mean–variance optimality under estimation noise
- Implement risk-based and tail-risk objectives
- Decompose portfolio risk at the asset and factor levels
- Embed static allocation rules into dynamic, realistic backtests
- Evaluate robustness through drawdowns, turnover, and transaction costs

---

**Alexandre Mathias DONNAT, Sr**