# 06 – Interest Rate Models

Hi there! 👋

## About

*To price anything in fixed income, we must understand how the entire yield curve moves. A shift in the short rate instantly changes every bond price, reshapes portfolio values, and ripples across maturities. Forward rates and LIBORs matter just as much: they are quoted directly in markets, used as benchmarks, and often act as the underlying of options such as caps, floors, and swaptions. Since these rates reflect many interacting risk factors, modelling their joint dynamics is essential.*

Interest-rate models provide exactly that: a coherent description of how all points on the curve evolve together.
In this chapter, we start from short-rate models (Vasicek, CIR) and progress to forward-rate models (HJM, BGM), revealing how bond prices, forward rates and LIBORs are generated and stitched together by no-arbitrage.*


![Historical Yield Curves](https://at.scalable.capital/images/kcbf79ije7q7/5irxgO0jfVhwjbR4YFgzCs/4970a56f5d3f9ec4e81bb70da937683f/yc1_changing_curve_and_prices.png)


Behind all of this lies one unifying mechanism: choose a numéraire, change measure, enforce martingale dynamics.

This simple structure is what makes the whole world of fixed-income modelling work, 
from affine closed-form bond prices to the Black formulas used every day to price interest-rate options.

## Content

- Yield curves in deterministic & stochastic settings
- Risk-neutral measure, discounted bonds as martingales
- Numéraire changes & forward measures
- Black pricing for bond options
- Short-rate models: Vasicek, CIR
- Forward-rate models: HJM, BGM (caplets, swaptions)

## Structure

| Notebook | Title | Core idea |
|----------|-------|-----------|
| 06.1 | Modelling Principles | Yield curves, short-rate dynamics, martingale pricing, forward measures. |
| 06.2 | Some Classical Models | Vasicek, CIR, HJM, BGM + affine formulas & Black pricing. |

## Notes to viewers

Feel free to move through these notebooks at your own pace, interest-rate modelling is conceptually dense, and the connections between short rates, forward rates, measures and numéraires take time to internalise.
If you are new to fixed-income modelling, take it slow: understanding the role of the numéraire, how discounted assets become martingales, and how this pins down drifts is key. These structural ideas matter more than the algebra.
If you already know the probabilistic framework(Girsanov, martingale pricing, affine diffusions): use the notebooks to deepen your intuition: compare short-rate vs forward-rate approaches, visualise the affine bond-price shapes, or experiment with how volatility choices propagate into HJM/BGM drifts.

The code cells are lightweight and can be extended:
you can add calibration examples, simulate short-rate paths (Euler), or test Black's caplet formula versus Monte Carlo in a few lines. Warnings are disabled at the top of the notebooks for cleaner output.

**Alexandre Mathias DONNAT, Sr**