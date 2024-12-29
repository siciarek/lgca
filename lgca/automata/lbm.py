
import numpy as np
import math


class Lbm:
    """Lattice Boltzmann Method."""

    name: str = "LBM"

    def __init__(self, grid: list, mode: str):
        self.step = 0

        self.mode = mode
        self.height = len(grid)
        self.width = len(grid[0])

        self.ny = self.height
        self.nx = self.width

        self.tau = 0.53
        self.cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
        self.cys = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])
        self.weights = np.array([4 / 9, 1 / 9, 1 / 36, 1 / 9, 1 / 36, 1 / 9, 1 / 36, 1 / 9, 1 / 36])  # sums to 1
        self.nl = len(self.cxs.tolist())

        # Initial conditions
        flow_shape = (self.height, self.width, self.nl)
        self.flow = np.ones(flow_shape)
        self.flow += 0.01 * np.random.randn(*flow_shape)
        self.flow[:, :, 3] = 2.3

        cylinder = []
        for row in range(self.height):
            cylinder.append([False] * self.width)
            for col in range(self.width):
                cylinder[row][col] = math.dist((self.height // 2, self.width // 4), (row, col)) < 13

        self.cylinder = np.array(cylinder)

        self.grid: list = [[0 for _ in range(self.width)] for _ in range(self.height)]
        ux, uy, rho = self.update_fluid_variables()

        self.temp_grid = np.sqrt(ux**2 + uy**2).tolist()

        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = round(0xFF * self.temp_grid[row][col])

    def update_fluid_variables(self):
        boundary_f = self.flow[self.cylinder, :]
        boundary_f = boundary_f[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]

        rho = np.sum(self.flow, 2)
        ux = np.sum(self.flow * self.cxs, 2) / rho
        uy = np.sum(self.flow * self.cys, 2) / rho

        self.flow[self.cylinder, :] = boundary_f
        ux[self.cylinder] = uy[self.cylinder] = 0

        return ux, uy, rho

    def __next__(self):

        for i, cy, cx in zip(range(self.nl), self.cxs, self.cys):
            self.flow[:, :, i] = np.roll(self.flow[:, :, i], cx, axis=0)
            self.flow[:, :, i] = np.roll(self.flow[:, :, i], cy, axis=1)

        ux, uy, rho = self.update_fluid_variables()

        # collision

        flow_equilibrium = np.zeros(self.flow.shape)
        for i, cx, cy, w in zip(range(self.nl), self.cxs, self.cys, self.weights):
            flow_equilibrium[:, :, i] = (
                rho * w * (1 + 3 * (cx * ux + cy * uy) + 9 * (cx * ux + cy * uy) ** 2 / 2 - 3 * (ux**2 + uy**2) / 2)
            )

        self.flow -= (1.0 / self.tau) * (self.flow - flow_equilibrium)

        self.temp_grid = np.sqrt(ux**2 + uy**2).tolist()
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = round(0xFF * self.temp_grid[row][col])

        self.step += 1
