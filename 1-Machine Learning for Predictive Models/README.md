# Machine Learning for Predictive Models

**Hi there!👋**

*Financial markets are dominated by noise, non-stationarity, and shifting regimes, where exploitable signals are weak and often ephemeral. As a consequence, direct return prediction is structurally fragile, while risk dynamics exhibit stronger persistence and more stable patterns. This module therefore prioritizes methodological rigor, time-consistent evaluation, explicit baselines, and interpretability, over raw model complexity or headline performance.*

This folder contains a set of research-oriented notebooks exploring how machine learning can be applied to financial prediction problems, with a strong emphasis on methodology, realism, and interpretability.

The objective here is not to build trading strategies or claim alpha, but to understand what machine learning can and cannot do when applied to noisy financial time series.

This block complements the stochastic calculus core of the repository by providing a data-driven and empirical perspective on quantitative finance.

## Practical 

Features are engineered from SPY price data (returns, volatility, momentum, and structural measures), saved as .parquet files in Notebook 01, and then reused in different ways across subsequent notebooks: as tabular inputs for classical supervised models, as temporal sequences for LSTM architectures, and as explanatory variables for interpretable risk-focused machine learning models.

## Content

| Notebook | Title | Core idea |
|----------|-------|------------|
| 01 | Feature Engineering for Market Data | Transform raw price series into meaningful predictive features (returns, volatility, momentum, structure). |
| 02 | Supervised Models for Return Prediction | Evaluate linear and tree-based models for return and direction prediction, with proper baselines and diagnostics. |
| 03 | LSTM & Deep Forecasting for Financial Time Series | Test whether sequence-aware deep models capture temporal dependencies beyond standard ML methods. |
| 04 | ML Risk Models & Explainability | Forecast risk measures (volatility) using ML and interpret predictions via feature importance and SHAP values. |

## What is demonstrated

- engineer features tailored to financial time series
- design robust ML evaluation pipelines under temporal constraints
- compare models against naïve and structural baselines
- diagnose overfitting and noise-driven results
- apply deep learning cautiously in a financial context
- model risk instead of returns, which is the dominant real-world use case
- interpret ML models using explainability tools

---
***Alexandre Mathias DONNAT, Sr***