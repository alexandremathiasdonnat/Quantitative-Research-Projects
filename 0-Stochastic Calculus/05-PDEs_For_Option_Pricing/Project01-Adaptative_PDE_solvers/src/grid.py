# src/grid.py
import numpy as np


class TimeSpaceGrid:
    """
    Simple container for time/space discretisation.

    Space: x_i = -L + i*h, i = 0..N+1  (N interior points)
    Time : t_n = n*k,     n = 0..M
    """

    def __init__(self, T: float, L: float, N: int, M: int):
        self.T = T
        self.L = L
        self.N = N       # number of interior points
        self.M = M       # number of time steps

        self.k = T / M                   # time step
        self.h = 2 * L / (N + 1)         # space step

        self.x = np.linspace(-L, L, N + 2)  # incl. boundaries
        self.t = np.linspace(0.0, T, M + 1)
