# 09 - Simulation & Algorithms for Financial Models

This chapter consolidates the numerical foundations of simulation-based pricing in quantitative finance.
It shows how to turn stochastic models into working algorithms, how to measure statistical uncertainty, and how to accelerate Monte Carlo estimators using classical variance reduction techniques.

It contains two components

## 09.1 - Monte Carlo Simulation & Variance Reduction (Notebook)

A structured lab that follows the standard quant pipeline:

### Part 1 — Monte Carlo Basics

- Simulation of Gaussian noise
- Estimation of expectations (LLN, CLT)
- 95% confidence intervals
- Convergence analysis and computational cost

### Part 2 — European Call Pricing

- Exact simulation of Black–Scholes
- Crude Monte Carlo pricer
- Comparison with analytical Black–Scholes formula
- Impact of payoff tail behaviour on variance

### Part 3 — Variance Reduction Techniques

- Antithetic variates (negative correlation trick)
- Control variates (L² projection, dramatic variance reduction)
- Importance sampling for rare events (deep OTM calls)
- CPU Timing vs variance analysis

### Part 4 — Hedging Error Under Discrete Rebalancing

- Delta-hedging simulation across thousands of paths
- Monthly / weekly / daily hedging
- Distribution of replication errors
- Gamma cost and structural limits of discrete hedging

This notebook provides a realistic introduction to simulation-based pricing,
and highlights the gap between continuous-time mathematics and real-world trading constraints.

## 2. MATLAB Computer Experiments (Folder)

A collection of compact MATLAB/Octave scripts illustrating the core ideas of the chapter:

- Basic Monte Carlo estimation
- Lognormal asset simulation
- Black–Scholes call pricing
- Antithetic sampling
- Control variates
- Histograms and simple plots

These scripts mirror historical teaching workflows in quantitative finance and complement the Jupyter notebook (Python chunks) with lightweight numerical experiments.

---

***Alexandre Mathias DONNAT, Sr***


