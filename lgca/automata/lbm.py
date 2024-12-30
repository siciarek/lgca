import numpy as np
from lgca.automata import Lgca


class Lbm(Lgca):
    """Lattice Boltzmann Method."""

    name: str = "LBM"

    def prepare(self):

        self.tau = 0.53
        self.cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
        self.cys = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])
        weights = np.array([4 / 9, 1 / 9, 1 / 36, 1 / 9, 1 / 36, 1 / 9, 1 / 36, 1 / 9, 1 / 36])  # sums to 1
        nl = len(self.cxs.tolist())

        self.neigh = list(zip(range(nl), self.cxs, self.cys, weights))

        # Initial conditions
        flow_shape = (self.height, self.width, nl)
        self.flow = np.ones(flow_shape)
        self.flow += 0.01 * np.random.randn(*flow_shape)
        self.flow[:, :, 3] = 2.3

        # create obstacle
        obstacle = [[self.grid[row][col] != 0 for col in range(self.width)] for row in range(self.height)]
        self.cylinder = np.array(obstacle)

        ux, uy, _ = self.update_fluid_variables()
        self.update_grid(ux=ux, uy=uy)

    def update_grid(self, ux, uy):
        temp_grid = np.sqrt(ux**2 + uy**2).tolist()
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = round(0xFF * temp_grid[row][col])

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
        self.step += 1

        for i, cx, cy, _ in self.neigh:
            self.flow[:, :, i] = np.roll(self.flow[:, :, i], cy, axis=0)
            self.flow[:, :, i] = np.roll(self.flow[:, :, i], cx, axis=1)

        ux, uy, rho = self.update_fluid_variables()

        # collision

        flow_equilibrium = np.zeros(self.flow.shape)
        for i, cx, cy, w in self.neigh:
            flow_equilibrium[:, :, i] = (
                rho * w * (1 + 3 * (cx * ux + cy * uy) + 9 * (cx * ux + cy * uy) ** 2 / 2 - 3 * (ux**2 + uy**2) / 2)
            )

        self.flow -= (1.0 / self.tau) * (self.flow - flow_equilibrium)

        self.update_grid(ux=ux, uy=uy)
