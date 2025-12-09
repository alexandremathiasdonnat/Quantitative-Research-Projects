% mc_call_antithetic.m
% Monte Carlo pricing of a European call with and without antithetic variates.
% The goal is to compare the empirical variance of both estimators.

clear all; close all; clc;

% Parameters
S0    = 100;
K     = 100;
r     = 0.05;
sigma = 0.2;
T     = 1.0;

N = 50000;  % base number of draws

% ---- Crude Monte Carlo ----
G = randn(N, 1);
ST = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T).*G);
payoff = exp(-r*T) * max(ST - K, 0);

price_mc = mean(payoff);
var_mc   = var(payoff);
se_mc    = sqrt(var_mc / N);

% ---- Antithetic variates ----
G_anti = -G;  % antithetic counterpart
ST1 = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T).*G);
ST2 = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T).*G_anti);

payoff1 = exp(-r*T) * max(ST1 - K, 0);
payoff2 = exp(-r*T) * max(ST2 - K, 0);

payoff_antithetic = 0.5 * (payoff1 + payoff2);

price_antithetic = mean(payoff_antithetic);
var_antithetic   = var(payoff_antithetic);
se_antithetic    = sqrt(var_antithetic / N);

fprintf('European call, N = %d base draws\n', N);
fprintf('Crude MC:          price = %.6f, Var = %.6f, SE = %.6f\n', ...
    price_mc, var_mc, se_mc);
fprintf('Antithetic MC:     price = %.6f, Var = %.6f, SE = %.6f\n', ...
    price_antithetic, var_antithetic, se_antithetic);
fprintf('Variance reduction factor ~ %.3f\n', var_mc / var_antithetic);
