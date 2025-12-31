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

---

**Alexandre Mathias Donnat**
