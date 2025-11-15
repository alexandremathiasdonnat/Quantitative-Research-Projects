# 02-Optimal Stopping and American Options  

**Hi there! 👋**

## About

*Sometimes, the hardest question in financial problems isn’t what to do, it’s when to do it. This section explores that razor’s edge between patience and action: when waiting has value, and when it silently destroys it. From martingale theory to the Snell envelope, we learn how time itself becomes a tradable asset,
and how American options transform this invisible timing game into real monetary worth.*


## Content  

This section develops the discrete-time theory of **optimal stopping** and applies it to the pricing of **American options** in a binomial/CRR framework.

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

If you’re just discovering this topic, take your time — quite literally. Each notebook shows how the abstract notion of “optimal timing” unfolds into code, figures, and meaning. Follow the random walks, the stopping times, and the envelopes: they’ll teach you intuition better than formulas alone.

If you are already familiar with the theory, you can extend the notebooks with your own **numerical experiments**: modify parameters, push to higher 
𝑁, change payoff structures (test exotic for instance), test different stopping rules, or benchmark other models.

Make sure the same Python modules are available in your environment before running the notebooks (NumPy, Pandas, Matplotlib, math).

## *Alexandre Mathias DONNAT, Sr*