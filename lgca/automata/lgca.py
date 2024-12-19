import random
from lgca.utils.config_loader import get_config


class Lgca:

    def __init__(self, grid):
        self.grid: list[list[int]] = grid
        self.height: int = len(self.grid)
        self.width: int = len(self.grid[0])
        self.step: int = 0
        self.temp_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.collision_table = get_config(self.name)

    def __next__(self):
        self.collision()
        self.free_translation()
        self.step += 1

        return self.grid

    def collision(self):
        for row in range(self.height):
            for col in range(self.width):
                result = self.collision_table[self.grid[row][col]]
                if isinstance(result, list):
                    result = random.choice(result)

                self.temp_grid[row][col] = result
