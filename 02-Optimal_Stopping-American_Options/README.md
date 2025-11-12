# 02-Optimal Stopping and American Options  

**Hi there! 👋**

## About

*In many financial problems, the payoff does not only depend on *what* happens, but on *when* we decide to act. Optimal stopping is the mathematics of timing : the bridge between probability, decision, and American-style derivatives.*


## Content  

This section develops the discrete-time theory of **optimal stopping** and applies it to  
the pricing of **American options** in a binomial/CRR framework.

Notebooks combine rigorous probabilistic tools (stopping times, Snell envelope, supermartingales), Markov-chain dynamic programming, and full numerical case studies (American put/call pricing, exercise boundary, early exercise premium).

The true objective is to move from abstract definitions to implementable algorithms that can price and analyse American-style contracts.

## Structure  

| Notebook | Title | Core Idea |
|:--:|:--|:--|
| **02.1** | Stopping Times | Random decision times based only on current and past information. Hitting times and simulated examples. |
| **02.2** | Snell Envelope | Value process of an optimal stopping problem. Backward recursion and first numerical constructions. |
| **02.3** | Supermartingale Decomposition | Doob–Meyer decomposition \(X = M - A\) and its interpretation for Snell envelopes. |
| **02.4** | Snell Envelope & Markov Chains | Dynamic programming on finite-state Markov chains. Stopping vs continuation regions. |
| **02.5** | American Options – Application | Full case study: American put/call pricing in the CRR model, exercise boundary, early exercise premium, convergence vs Black–Scholes. |

## Notes  

Feel free to reuse these notebooks if you are interested in how **optimal stopping and American option pricing work in practice**.

If you are new to the topic, you can focus on the theoretical explanations and visualisations to build intuition step by step.
If you are already familiar with the theory, you can extend the notebooks with your own **numerical experiments**: modify parameters, change payoff structures, test different stopping rules, or benchmark other models.

Make sure the same Python modules are available in your environment  
before running the notebooks (NumPy, Pandas, Matplotlib, math).

## *Alexandre Mathias DONNAT, Sr*