from abc import ABC
import numpy as np
from lgca.utils.config_loader import get_config

DTYPE = np.ubyte


class LgcaFaster(ABC):
    name: str = "LGCA"
    masks: tuple = tuple()
    neighborhood: tuple = tuple()
    OBSTACLE_BIT: int = 0b1000_0000
    REST_PARTICLE_BIT: int = 0b0100_0000
    MODE_TORUS: str = "torus"
    MODE_DIE: str = "die"

    def __init__(self, grid, mode: str = MODE_TORUS) -> None:
        self.grid = np.array(grid, dtype=DTYPE)
        self.height = len(grid)
        self.width = len(grid[0])
        self.step = 0
        self.mode = mode
        self.neighborhood_indices = []
        self.neighborhood_masks = []
        self.prepare()

    def __next__(self):
        self.step += 1
        self.collision()
        self.free_translation()

    def prepare(self):
        self.temp_grid = np.zeros((self.height, self.width), dtype=DTYPE)
        self.lookup_table = get_config(self.name.replace(" ", "_").lower())

        # Pre-compute neighborhood indices and masks
        self.neighborhood_indices = []
        self.neighborhood_masks = []

        # Create lookup arrays for even and odd columns
        for parity in [0, 1]:  # 0 for even, 1 for odd
            cols = range(parity, self.width, 2)
            for col in cols:
                for row in range(self.height):
                    for idx, (row_off, col_off) in enumerate(self.neighborhood[parity]):
                        n_row, n_col = row + row_off, col + col_off

                        if self.mode == self.MODE_DIE:
                            if not (0 <= n_row < self.height and 0 <= n_col < self.width):
                                continue
                        else:  # MODE_TORUS
                            n_row = (n_row + self.height) % self.height
                            n_col = (n_col + self.width) % self.width

                        # print((row, col, n_row, n_col))
                        self.neighborhood_indices.append((row, col, n_row, n_col))
                        self.neighborhood_masks.append(self.masks[idx])

        # Convert to numpy arrays for faster access
        self.neighborhood_indices = np.array(self.neighborhood_indices, dtype=np.int32)
        self.neighborhood_masks = np.array(self.neighborhood_masks, dtype=DTYPE)

    def collision(self):
        # Vectorized collision step
        for state in np.unique(self.grid):
            mask = self.grid == state
            result = self.lookup_table[state]
            self.temp_grid[mask] = np.random.choice(result, size=np.sum(mask)) if len(result) > 1 else result[0]

    def free_translation(self) -> None:
        # Apply basic masks using vectorized operations
        self.grid[:] = (self.temp_grid & self.OBSTACLE_BIT) | (self.temp_grid & self.REST_PARTICLE_BIT)

        # Use pre-computed indices for neighborhood operations
        src_rows = self.neighborhood_indices[:, 2]  # n_row
        src_cols = self.neighborhood_indices[:, 3]  # n_col
        dst_rows = self.neighborhood_indices[:, 0]  # row
        dst_cols = self.neighborhood_indices[:, 1]  # col

        # Filter out empty cells
        mask = self.temp_grid[src_rows, src_cols] != 0

        # Apply masks in one operation
        np.bitwise_or.at(
            self.grid,
            (dst_rows[mask], dst_cols[mask]),
            self.temp_grid[src_rows[mask], src_cols[mask]] & self.neighborhood_masks[mask],
        )
