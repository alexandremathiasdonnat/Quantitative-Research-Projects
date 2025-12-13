# Portfolio Optimization & Dynamic Allocation

**Hi there! 👋**

*Portfolio optimization lies at the intersection of financial theory, numerical optimization, and decision-making under uncertainty. 
In practice, portfolio construction is less about predicting returns than about controlling risk, managing estimation error, and ensuring robustness under changing market conditions.*

This chapter explores portfolio allocation from two complementary perspectives:

1. **Static, risk-based portfolio construction**, grounded in convex optimization and risk budgeting techniques.
2. **Dynamic, continuous-time optimal control**, formulated as a Hamilton–Jacobi–Bellman (HJB) partial differential equation.

Together, these approaches illustrate how portfolio decisions emerge from different modeling assumptions, risk preferences, and time representations, and how theoretical optima behave once embedded into realistic investment processes.

This chapter is organized into two main components:

## 1. Theory & Practice 
**Folder:** `Theory/`

This section focuses on classical and modern portfolio optimization methods formulated as **static convex optimization problems**, evaluated under realistic constraints and estimation uncertainty.

The emphasis is deliberately placed on **risk control rather than return forecasting**, reflecting the empirical instability of expected returns and the stronger persistence of risk-related quantities.
Topics Covered : Mean–Variance optimization under convex constraints, Risk Parity and factor-based risk budgeting, CVaR / Expected Shortfall optimization for tail-risk control, Risk decomposition at the asset and factor levels, Sensitivity of allocations to estimation noise, embedding static allocations into rolling backtests

### Structure
| Notebook | Title | Core Idea |
|--------|------|-----------|
| 01 | Markowitz Mean–Variance Optimization | Efficient frontier, minimum variance and tangency portfolios under realistic constraints |
| 02 | Risk Parity & Factor-Based Allocation | Allocation via equal risk contributions without return forecasts |
| 03 | CVaR Optimization | Tail-risk–aware portfolio construction using scenario-based Expected Shortfall |
| 04 | Backtesting Strategies & Allocation Dynamics | Rolling rebalancing, transaction costs, turnover, and comparative evaluation |

## 2. ProjectHJB — Dynamic Portfolio Allocation via HJB  
**Folder:** `Projet-HJB_Optimal_Portfolio_Allocation_Engine-Hamilton–Jacobi–Bellman-(PDE-based)/`

This standalone project reframes portfolio optimization as a **continuous-time stochastic control problem**.

Instead of selecting a static allocation vector, the investor dynamically adjusts exposure over time as a function of wealth and market parameters. The optimal policy is obtained by solving the **Hamilton–Jacobi–Bellman (HJB) equation**, a nonlinear partial differential equation governing optimal decision-making under uncertainty.

This component bridges stochastic calculus, optimal control, and portfolio choice theory.

### Core Concepts

- Continuous-time portfolio choice under stochastic dynamics  
- Utility-based decision making and risk aversion (CRRA framework)  
- Hamilton–Jacobi–Bellman equation as a dynamic decision PDE  
- Feedback control interpretation of optimal allocation policies  
- Numerical stability and discretization issues in nonlinear PDEs  
- Linking theoretical optimal control to simulated investment outcomes

### What is demonstrated
- How portfolio allocation emerges from optimal control principles
- The equivalence between HJB and closed-form Merton solutions in simple settings
- The impact of leverage, constraints, and risk aversion on optimal policies
- The numerical challenges of solving nonlinear PDEs in finance
- The gap between theoretical optimality and implementable strategies

### Outputs
- Optimal allocation policy $$(\pi(t, W))$$ across time and wealth levels  
- Wealth-dependent exposure surfaces under leverage and constraint regimes  
- Simulated wealth distributions under optimal and benchmark strategies  
- Drawdown, tail-risk, and risk-adjusted performance diagnostics  
- Time-consistent, strategy-level allocation and performance snapshots

## Purpose 

Portfolio optimization is not a single problem, but a family of decision frameworks, whose solutions depend critically on modeling assumptions, risk preferences, and time representation.

By combining static convex optimization with dynamic HJB-based control, this block connects:
- **risk modeling → optimization → implementation**,  
- **stochastic calculus → numerical methods → portfolio decisions**,   and complements both the stochastic calculus and machine learning components of the repository.

---

**Alexandre Mathias DONNAT**
