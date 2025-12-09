% plot_hist.m
% Histogram of N(0,1) samples to check Gaussian sampling.

clear all; close all; clc;

N = 10000;
G = randn(N, 1);

figure;
hist(G, 50);  % 50 bins
title('Histogram of N(0,1) samples');
xlabel('Value');
ylabel('Frequency');
grid on;
