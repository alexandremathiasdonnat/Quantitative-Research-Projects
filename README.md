# Quantitative Research Projects

**Hi there! 👋**

Markets look like noise until we impose structure: information, constraints, and the refusal of arbitrage.  
This repository is my attempt to turn that structure into working research artifacts, not just notes, not just formulas, but models that run, break, and teach.

At its core, this work revolves around one idea:

> **Randomness is not the enemy,  unstructured reasoning is.**

I build from first principles to implementable engines in three complementary directions:

- **Stochastic calculus** to formalize uncertainty, derive prices, and construct numerical methods that match real market mechanics (diffusions, jumps, rates, credit, Monte Carlo, PDE/PIDE).
- **Machine learning** to test what data-driven prediction can and cannot extract from unstable time series, with an emphasis on methodology, baselines, and interpretability rather than “alpha storytelling”.
- **Portfolio optimization** to transform models into decisions, from convex risk-based allocations to dynamic control policies solved through HJB-style PDEs.

A large part of the stochastic calculus references is supported by the Chapman & Hall/CRC Financial Mathematics Series, especially:  
*Lamberton & Lapeyre - Introduction to Stochastic Calculus Applied to Finance (2nd ed.)* used as a rigorous anchor between theory and implementation.

### How to use/read this repo
Each chapter is designed to be read like a research notebook: start with intuition, stress-test the assumptions, then run the code and observe where the model holds — and where reality forces compromises.

If you are a quant-minded reader, the fastest path is:
**read a short theory notebook → run a project engine (usually very intuitive driven by dashboard calling library we developped)→ inspect outputs & failure modes**.

# Core Research Projects (A–G)

Below is a curated list of the main end-to-end research engines developed in this repository.
Each project corresponds to a fully implemented quantitative model, typically exposed through an interactive dashboard and backed by a reusable Python library.

They are ordered to reflect a natural progression:
stochastic modeling → pricing → numerical methods → risk → portfolio decisions.

---
**Project A - Ornstein–Uhlenbeck Process Simulator & MLE Calibration**

`Folder` 0-Stochastic Calculus/03-Brownian_Motion-SDEs/Project A - Ornstein Uhlenbeck Process Simulator & MLE Calibration/  
**Direct access** : [Project A - Ornstein–Uhlenbeck Process Simulator & MLE Calibration](https://github.com/alexandremathiasdonnat/Quantitative-Research-Projects/tree/main/0-Stochastic%20Calculus/03-Brownian_Motion-SDEs/Project%20A%20%20-%20Ornstein%20Uhlenbeck%20Process%20Simulator%20%26%20MLE%20Calibration) 

*A market-facing simulator for mean-reverting processes, combining exact and Euler schemes with maximum-likelihood calibration on real data.
Used as a foundational building block for interest rates, spreads, and stochastic factor modeling.*

---

**Project B - Live Implied Volatility Engine & VIX-Like Index Dashboard**

`Folder` 0-Stochastic Calculus/04-Black_Scholes-Model/Project B - Live Implied Vol Engine & VIX like Index Dashboard/    
**Direct access** : [Project B - Live Implied Volatility Engine & VIX-Like Index Dashboard](https://github.com/alexandremathiasdonnat/Quantitative-Research-Projects/tree/main/0-Stochastic%20Calculus/04-Black_Scholes-Model/Project%20B%20-%20Live%20Implied%20Vol%20Engine%20%26%20VIX%20like%20Index%20Dashboard#live-implied-volatility-engine--vix-like-dashboard)

*A volatility analysis engine turning option prices into implied volatilities, full smiles and surfaces, and a VIX-style aggregate indicator.
Designed to mirror trading-desk workflows for volatility diagnostics and regime analysis.*

---

**Project C - Finite-Difference Black–Scholes PDE Pricer (European & American Options)**

`Folder` 0-Stochastic Calculus/05-PDEs_For_Option_Pricing/Project C - Finite Difference Black–Scholes PDE Pricer for European & American Options with Brennan–Schwartz Projection   
**Direct access** : [Project C - Finite-Difference Black–Scholes PDE Pricer (European & American Options)](https://github.com/alexandremathiasdonnat/Quantitative-Research-Projects/tree/main/0-Stochastic%20Calculus/05-PDEs_For_Option_Pricing/Project%20C%20-%20Finite%20Difference%20Black%E2%80%93Scholes%20PDE%20Pricer%20for%20European%20%26%20American%20Options%20with%20Brennan%E2%80%93Schwartz%20Projection)

*A clean, reusable PDE pricing engine in log-space, solving the Black–Scholes equation via θ-schemes.
European options are priced by backward induction; American options are handled through a free-boundary formulation using Brennan–Schwartz projection.
Designed as a numerical benchmark and research sandbox for stability, convergence, and early-exercise behavior.*

---

**Project D - Term-Structure Modeling & Short-Rate Calibration Engine**

`Folder` 0-Stochastic Calculus/06-Interest_Rate_Models/Project D - Term-Structure Modeling & Short-Rate Calibration Engine/   
**Direct access** : [Project D - Term-Structure Modeling & Short-Rate Calibration Engine](https://github.com/alexandremathiasdonnat/Quantitative-Research-Projects/tree/main/0-Stochastic%20Calculus/06-Interest_Rate_Models/Project%20D%20-%20Term-Structure%20Modeling%20%26%20Short-Rate%20Calibration%20Engine)


*An interest-rate engine that calibrates Vasicek or CIR short-rate models to market zero-coupon curves, reconstructs the full term structure, prices basic IR products (ZC, FRA, swaps), and simulates rate dynamics using the calibrated SDE.
A compact, industry-style implementation of fixed-income modeling fundamentals.*

---

**Project E - Jump–Diffusion Option Pricing Engine (PIDE-Based)**

`Folder` 0-Stochastic Calculus/07-Asset_Models_With_Jumps/Project E - Jump–Diffusion PIDE Solving Engine for Option Pricing/   
**Direct access** : [Project E - Jump–Diffusion Option Pricing Engine (PIDE-Based)](https://github.com/alexandremathiasdonnat/Quantitative-Research-Projects/tree/main/0-Stochastic%20Calculus/07-Asset_Models_With_Jumps/Project%20E%20-%20Jump%E2%80%93Diffusion%20PIDE%20Solving%20Engine%20for%20Option%20Pricing
)

*A full jump–diffusion pricing framework supporting Black–Scholes, Merton, and Kou models.
European option prices are obtained by solving the pricing PIDE; the engine also generates jump-induced implied-volatility smiles and simulates discontinuous asset paths via Monte Carlo.
Used to study skew, tail risk, and the structural impact of jumps on option prices.*

---
**Project F - Credit Risk Engine: Structural Default, CDS Calibration & Copula Portfolio Loss**

`Folder` 0-Stochastic Calculus/08-Credit_Risk_Models/Project F - Credit Risk Engine - Structural Default, CDS Calibration & Copula-Based Portfolio Loss/   
**Direct access** : [Project F — Credit Risk Engine: Structural Default, CDS Calibration & Copula Portfolio Loss](https://github.com/alexandremathiasdonnat/Quantitative-Research-Projects/tree/main/0-Stochastic%20Calculus/08-Credit_Risk_Models/Project%20F%20-%20Credit%20Risk%20Engine%20-%20%20Structural%20Default%2C%20CDS%20Calibration%20%26%20Copula-Based%20Portfolio%20Loss
)

*A comprehensive credit-risk engine combining Merton structural models, CDS-implied intensity calibration, and copula-based portfolio default simulation.
Produces default probabilities, loss distributions, VaR / Expected Shortfall, and sensitivity diagnostics, closely reflecting workflows used in credit, CVA, and systemic risk analysis.*

---

**Project G — Optimal Portfolio Allocation via HJB (Stochastic Control, PDE-Based)**

`Folder` 2-Portfolio Optimization/Projet G - Optimal Portfolio Allocation Engine via Hamilton–Jacobi–Bellman (Stochastic Control, PDE-based)/   
**Direct access** : [Project G — Optimal Portfolio Allocation via HJB (Stochastic Control, PDE-Based)](https://github.com/alexandremathiasdonnat/Quantitative-Research-Projects/tree/main/2-Portfolio%20Optimization/Projet%20G%20-%20Optimal%20Portfolio%20Allocation%20Engine%20via%20Hamilton%E2%80%93Jacobi%E2%80%93Bellman%20(Stochastic%20Control%2C%20PDE-based)
)

*A research-oriented portfolio allocation engine formulated as a continuous-time stochastic control problem.
The optimal allocation policy is obtained by solving the Hamilton–Jacobi–Bellman equation and then implemented under realistic trading constraints.
Strategies are evaluated net of transaction costs using expected utility, highlighting the gap between theoretical optimality and practical buy-side robustness.*


---

**Alexandre Mathias Donnat**
