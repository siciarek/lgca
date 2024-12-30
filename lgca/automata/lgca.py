from abc import ABC
import secrets


from lgca.utils.config_loader import get_config


class Lgca(ABC):
    name: str = "LGCA"
    masks: tuple = tuple()
    neighborhood: tuple = tuple()
    OBSTACLE_BIT: int = 0b1000_0000
    REST_PARTICLE_BIT: int = 0b0100_0000
    MODE_TORUS: str = "torus"
    MODE_DIE: str = "die"

    def __init__(self, grid, mode: str = MODE_TORUS) -> None:
        self.grid: list[list[int]] = grid
        self.height: int = len(self.grid)
        self.width: int = len(self.grid[0])
        self.step: int = 0
        self.mode = mode
        self.prepare()

    def __next__(self):
        self.step += 1
        self.collision()
        self.free_translation()

    def prepare(self):
        self.temp_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.lookup_table = get_config(self.name.replace(" ", "_").lower())

    def collision(self):
        for row in range(self.height):
            for col in range(self.width):
                result = self.lookup_table[self.grid[row][col]]
                if isinstance(result, list):
                    result = secrets.choice(result)

                self.temp_grid[row][col] = result

    def free_translation(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = self.temp_grid[row][col] & self.OBSTACLE_BIT
                self.grid[row][col] |= self.temp_grid[row][col] & self.REST_PARTICLE_BIT

                for idx, (row_off, col_off) in enumerate(self.neighborhood[col % 2]):
                    n_row, n_col = row + row_off, col + col_off

                    # work in "die" mode
                    if self.mode == self.MODE_DIE and not (0 <= n_row < self.height and 0 <= n_col < self.width):
                        continue

                    # performance trick
                    if (0 <= n_row < self.height and 0 <= n_col < self.width) and not self.temp_grid[n_row][n_col]:
                        continue

                    # work in "torus" mode
                    n_row, n_col = (n_row + self.height) % self.height, (n_col + self.width) % self.width

                    self.grid[row][col] |= self.temp_grid[n_row][n_col] & self.masks[idx]
