from lgca import settings
from lgca.automata import Lgca


class FhpOne(Lgca):
    name: str = "fhpi"
    masks: tuple[int] = (
        0b001000,
        0b010000,
        0b100000,
        0b000001,
        0b000010,
        0b000100,
    )

    def free_translation(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                new_val = self.temp_grid[row][col] & 0b1000_0000

                for idx, (row_off, col_off) in enumerate(settings.HONEYCOMB[col % 2]):
                    # torus mode:
                    n_row = (row + row_off + self.height) % self.height
                    n_col = (col + col_off + self.width) % self.width

                    new_val |= self.temp_grid[n_row][n_col] & self.masks[idx]

                self.grid[row][col] = new_val
