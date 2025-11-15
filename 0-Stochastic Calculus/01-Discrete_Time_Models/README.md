# 01-Discrete-Time Models  

**Hi there! 👋**

## About

*Behind every sophisticated trading algorithm lies a discrete model :
a clean mathematical playground where randomness meets reason.
Everything begins here: a world where prices evolve step by step, and where arbitrage disappears under the right probability measure to keep markets fair.*

## Content

This section introduces the **foundations of discrete-time financial models**, combining both **rigorous theory** and **numerical applications in Python**.  

It covers the core ideas of modern asset pricing:  
How to model financial markets over discrete time, define arbitrage-free dynamics, and derive fair prices for options through replication and risk-neutral valuation.  

The notebooks mix **mathematical structure** and **computational practice**, progressively building from theoretical definitions to fully coded examples.  

## Structure  

| Notebook | Title | Core Idea |
|:--:|:--|:--|
| **01.1** | Discrete-Time Formalism | Market setup, self-financing strategies, admissibility and arbitrage. |
| **01.2** | Martingales and Arbitrage | No-arbitrage ⇔ existence of a risk-neutral measure (Fundamental Theorem). |
| **01.3** | Complete Markets & Pricing | Replication, fair pricing and expectation under the risk-neutral measure. |
| **01.4** | Cox–Ross–Rubinstein (CRR) Model | Binomial tree model and convergence to the Black–Scholes limit. |

---

## Notes  

Feel free to reuse these notebooks if you're interested in understanding  
**how discrete-time pricing mechanisms work in practice**.  

If you’re discovering this field, take the time to focus on the theoretical explanations (they’ll help you grasp the logic behind the models).  

If you’re already familiar with these concepts, you can extend the notebooks by developing your own **numerical experiments**, testing **hedging conditions**, or comparing **model accuracy** across different parameters.  

Make sure the same Python modules are installed in your environment  before running the notebooks (NumPy, Matplotlib, Pandas, math).  

<h3><span style="color:#800000;"><strong> </strong> <em>Alexandre Mathias DONNAT, Sr</em></span></h3>

