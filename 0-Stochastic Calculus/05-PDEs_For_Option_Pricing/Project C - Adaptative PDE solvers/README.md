# Adaptive PDE solvers for European & American options (free-boundary) under Black–Scholes (log-space)

This project provides a compact and fully reusable **PDE engine** as a quantitative library for pricing
**European and American Vanilla options** under the **Black–Scholes model**, implemented
in **log-price** and solved using **finite differences** with a θ-scheme.

The goal is to offer a clean, well-structured codebase that can be used as:

- a **numerical benchmark** against closed-form formulas or binomial trees,
- a **research sandbox** to experiment with stability, convergence, and
    free-boundary behaviour,
- a **building block** for more advanced models (local vol, jumps, stochastic
    control).

## What the engine does

- Builds a **time–space grid** on $(t,x) \in [0,T] \times [-L, L]$ where $x=\log S$.
- Constructs the **Black–Scholes log-space operator** as a **tridiagonal matrix**.
- Solves the pricing PDE using a **θ-scheme** (explicit, implicit, Crank–Nicolson).
- Uses a custom **Thomas algorithm** for fast tridiagonal solves in $O(N)$.
- Prices **European options** by backward time stepping.
- Prices **American puts** via a simple **free-boundary LCP projection step**:
    $$u^{n}_i = \max(\tilde u^{n}_i,\, \text{payoff}_i).$$

The implementation is intentionally minimal, transparent, and stable — suitable
for teaching, research, or interview-level quantitative work.


## Repository structure

```text
src/
        grid.py           // time–space grid definition
        payoffs.py        // call/put payoffs in log-space
        operators.py      // tridiagonal BS log-operator coefficients
        tridiagonal.py    // Thomas algorithm
        theta_schema.py   // European PDE θ-scheme solver
        american_pde.py   // American PDE solver (θ-scheme + projection)

solvers/
        european_call_solver.ipynb     // PDE price vs closed-form (call)
        american_put_solver.ipynb // PDE price + exercise boundary (put)
```

Each notebook imports the functions from `src/` and demonstrates how to run a
full pricing loop with a few lines of code.

## How to use it (conceptual tutorial to viewers)

Each solver-notebook works like a mini-dashboard:
- you choose the option you want to price (here only european or american),
- you open the corresponding notebook-solver,
- you fill in the input parameters,
- the engine computes everything automatically.

Only two notebooks exist for now (European call / American put),
but they are fully modular, the solver adapts to any inputs.

**1. EuropeanCall Solver Notebook : simple PDE call pricer**

This notebook lets you price a European call option with a PDE solver.

**Step 1 : Choose your inputs**
- $S_0$, $K$, $T$
- volatility $\sigma$
- interest rate $r$
- grid parameters: $L$ (log-domain), $N$ (space steps), $M$ (time steps)
- $\theta$-scheme parameter: $0$, $0.5$ or $1$

**Step 2 : Run the notebook**

It automatically:
- builds the time–space grid,
- constructs the BS operator coefficients $(a,b,c)$,
- applies the $\theta$-scheme PDE solver,
- interpolates the price at $\log S_0$.

**Step 3 : Read the outputs**

You get:
- the PDE price at $t=0$,
- the Black–Scholes closed-form price,
- the absolute error between both,
- a plot of $u(0,x)$ vs $S=e^x$.

This notebook acts as a numerical dashboard:
change the inputs, re-run, instantly see how the PDE price reacts.

---

**2. AmericanPut Solver Notebook : free-boundary solver**

This notebook is a full American put pricer.

**Inputs**

Same as the European pricer, plus:
- the American payoff $(K - e^x)_+$

**Internal steps (automatic)**

The notebook:
- solves the PDE in log-space with the $\theta$-scheme,
- applies the American projection step at each time,
- reconstructs the exercise/continuation region.

**Outputs**

You obtain:
- the American price at $S_0$,
- a heatmap showing exercise vs continuation,
- the optimal exercise boundary as a function of time,
- a comparison with a CRR binomial tree.

This notebook acts as a free-boundary visualizer for American options.



## Extending the solver

The engine is modular: we can easily build more dashboards on top of it.

Possible extensions:
- barrier options
- dividends
- local volatility σ(t,x)
- jump-diffusion PIDEs
- stochastic volatility
- optimal stopping / control

All follow the same workflow:

Inputs → PDE solver → Price surface + plots

