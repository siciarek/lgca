from lgca import settings
from lgca.automata import Lgca


class Hpp(Lgca):
    name: str = "hpp"
    masks = (
        0b0001,
        0b1000,
        0b0010,
        0b0100,
    )

    def free_translation(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                new_val = self.temp_grid[row][col] & 0b1000_0000

                for idx, (row_off, col_off) in enumerate(settings.VON_NEUMANN_NEIGHBORHOOD.values()):
                    # Torus mode:
                    n_row = (row + row_off + self.height) % self.height
                    n_col = (col + col_off + self.width) % self.width

                    new_val |= self.temp_grid[n_row][n_col] & self.masks[idx]

                self.grid[row][col] = new_val
