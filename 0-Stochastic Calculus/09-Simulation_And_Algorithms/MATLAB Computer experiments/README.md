# Chapter 09 – Monte Carlo (MATLAB / Octave)

This folder contains a small collection of MATLAB/Octave scripts illustrating the core ideas of Chapter 9: simulation and Monte Carlo methods for financial models.

The objective is to show clean minimal use-cases of:

- Monte Carlo estimation and confidence intervals,
- Simulation of Black–Scholes paths,
- Option pricing by Monte Carlo,
- Basic variance reduction techniques (antithetic variates, control variates).

## Files

- `mc_basic.m`  
    Estimates $\mathbb{E}[e^G]$ with $G \sim \mathcal{N}(0,1)$ using Monte Carlo.
    Prints the estimate, empirical variance, and 95% confidence intervals for different sample sizes $N$, illustrating the $1/\sqrt{N}$ convergence rate.

- `simulate_bs.m`  
    Simulates and plots several sample paths of a Black–Scholes asset
    $$
    dS_t = S_t (r\,dt + \sigma\,dW_t).
    $$
    Uses the exact geometric Brownian motion solution.

- `mc_call.m`  
    Prices a European call option by Monte Carlo under the Black–Scholes model and compares the result to the analytical Black–Scholes formula.

- `mc_call_antithetic.m`  
    Reprices the same call using **antithetic variates** (pairing $G$ with $-G$) and compares the empirical variance and standard error with the crude Monte Carlo estimator.

- `mc_call_control_variate.m`  
    Uses the terminal underlying price $S_T$ as a **control variate**, exploiting the fact that
    $$
    \mathbb{E}[S_T] = S_0 e^{rT}
    $$
    under the risk-neutral measure. Demonstrates how the optimal control variate coefficient can be estimated from the sample and how much the variance is reduced.

- `plot_hist.m`  
    Plots a histogram of draws from $\mathcal{N}(0,1)$ as a basic sanity check of the Gaussian sampling.

All scripts have been written to be compatible with both MATLAB and GNU Octave.
They are  short and self-contained, making them easy to read and to adapt.

