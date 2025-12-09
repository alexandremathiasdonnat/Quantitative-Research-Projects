% mc_call_control_variate.m
% Monte Carlo pricing of a European call using S_T as a control variate.
% We compare the crude variance vs the variance with the control variate.

clear all; close all; clc;

% Parameters
S0    = 100;
K     = 120;    % slightly OTM to make variance reduction more visible
r     = 0.05;
sigma = 0.2;
T     = 1.0;
N     = 50000;

% Draw Gaussian and simulate S_T
G = randn(N, 1);
ST = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T).*G);

% Discounted payoff Y = e^{-rT} (S_T - K)+
Y = exp(-r*T) * max(ST - K, 0);   % target: E[Y]

% ---- Crude estimator ----
price_mc = mean(Y);
var_mc   = var(Y);
se_mc    = sqrt(var_mc / N);

% ---- Control variate with Z = S_T (not discounted) ----
Z  = ST;
EZ = S0 * exp(r*T);   % E[S_T] under risk-neutral measure

% Estimate beta* = Cov(Y, Z) / Var(Z) from the sample
cov_YZ  = mean((Y - mean(Y)) .* (Z - mean(Z)));
var_Z   = var(Z);
beta    = cov_YZ / var_Z;

% Adjusted payoff
Y_tilde = Y - beta * (Z - EZ);

price_cv = mean(Y_tilde);
var_cv   = var(Y_tilde);
se_cv    = sqrt(var_cv / N);

fprintf('European call (K=%.2f), N = %d\n', K, N);
fprintf('Without control variate: price = %.6f, Var = %.6f, SE = %.6f\n', ...
    price_mc, var_mc, se_mc);
fprintf('With control variate:    price = %.6f, Var = %.6f, SE = %.6f\n', ...
    price_cv, var_cv, se_cv);
fprintf('Variance reduction factor ~ %.3f\n', var_mc / var_cv);
