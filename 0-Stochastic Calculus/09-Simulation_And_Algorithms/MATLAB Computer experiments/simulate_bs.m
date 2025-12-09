% simulate_bs.m
% Simulates sample paths of the Black–Scholes model
% dS_t = S_t (r dt + sigma dW_t)
% and plots the trajectories.

clear all; close all; clc;

% Model parameters
S0    = 100;
r     = 0.05;   % risk-free rate
sigma = 0.2;    % volatility
T     = 1.0;    % maturity (in years)
Nsteps = 250;   % number of time steps (e.g. ~250 trading days)
Npaths = 5;     % number of paths to plot

dt = T / Nsteps;
t  = linspace(0, T, Nsteps+1);

% Matrix to store paths
S = zeros(Nsteps+1, Npaths);
S(1, :) = S0;

for j = 1:Npaths
    % Brownian increments: sqrt(dt) * N(0,1)
    dW = sqrt(dt) * randn(Nsteps, 1);
    W  = [0; cumsum(dW)];
    
    % Exact GBM solution
    S(:, j) = S0 * exp( (r - 0.5 * sigma^2) * t' + sigma * W );
end

figure;
plot(t, S, 'LineWidth', 1.2);
xlabel('Time t');
ylabel('S_t');
title('Sample paths of the Black–Scholes model');
grid on;
