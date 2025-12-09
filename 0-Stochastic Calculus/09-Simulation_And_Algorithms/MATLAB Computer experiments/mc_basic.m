% mc_basic.m
% Basic Monte Carlo: estimate E[e^G] with G ~ N(0,1)
% and display 95% confidence intervals for different N.

clear all; close all; clc;

% List of sample sizes
Ns = [1e3, 1e4, 1e5];

true_value = exp(0.5);  % E[e^G] = exp(1/2)

fprintf('Estimating E[e^G] with G ~ N(0,1)\n');
fprintf('Theoretical value: %.6f\n\n', true_value);

for k = 1:length(Ns)
    N = Ns(k);
    
    % Draw Gaussian samples
    G = randn(N, 1);
    Y = exp(G);
    
    % Monte Carlo estimator
    est = mean(Y);
    var_est = var(Y);          % empirical variance
    se = sqrt(var_est / N);    % standard error
    
    % 95% confidence interval: est +/- 1.96 * se (approx CLT)
    z = 1.96;
    ci_low  = est - z * se;
    ci_high = est + z * se;
    
    fprintf('N = %8d : est = %.6f, SE = %.6f, CI95 = [%.6f ; %.6f]\n', ...
        N, est, se, ci_low, ci_high);
end

fprintf('\nNote: the width of the confidence interval shrinks like 1/sqrt(N).\n');
