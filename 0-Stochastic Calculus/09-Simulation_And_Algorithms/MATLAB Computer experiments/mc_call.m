% mc_call.m
% Monte Carlo pricing of a European call under Black–Scholes
% and comparison with the closed-form Black–Scholes formula.

clear all; close all; clc;

% Parameters
S0    = 100;
K     = 100;
r     = 0.05;
sigma = 0.2;
T     = 1.0;
N     = 100000;  % number of simulations

% Draw G ~ N(0,1)
G = randn(N, 1);

% Simulate S_T
ST = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T).*G);

% Discounted payoff
payoff = exp(-r*T) * max(ST - K, 0);
price_mc = mean(payoff);
var_est  = var(payoff);
se       = sqrt(var_est / N);

% 95% confidence interval
z = 1.96;
ci_low  = price_mc - z * se;
ci_high = price_mc + z * se;

fprintf('European call (Monte Carlo):\n');
fprintf('MC price = %.6f, SE = %.6f, CI95 = [%.6f ; %.6f]\n', ...
    price_mc, se, ci_low, ci_high);

% Black–Scholes analytic formula
d1 = (log(S0/K) + (r + 0.5*sigma^2)*T) / (sigma*sqrt(T));
d2 = d1 - sigma*sqrt(T);

% Normal CDF
N_cdf = @(x) 0.5 * (1 + erf(x / sqrt(2)));

price_bs = S0 * N_cdf(d1) - K * exp(-r*T) * N_cdf(d2);

fprintf('Black–Scholes closed-form price = %.6f\n', price_bs);
fprintf('Absolute error (MC vs BS) = %.6f\n', abs(price_mc - price_bs));
