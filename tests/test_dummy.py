import secrets
import yaml

from lgca.display import HexagonalGrid
from lgca.automata import FhpOne
from lgca.utils.initial_shape import frame, solid_rectangle, solid_square
from lgca import settings


def test_hex_lattice():
    pattern = "wiki"

    # width, height, tile_size = 100, 70, 8

    colors = [None] * 64
    for key, val in yaml.safe_load((settings.BASE_PATH / "lgca" / "config" / "colors.yaml").open())["fhpi"].items():
        val = val.lstrip('#')
        colors[int(key, 2)] = (int(val[:2], 16), int(val[2:4], 16), int(val[4:], 16))

    match pattern:
        case "wiki":
            width, height, tile_size, fps = 300, 200, 4, -1

            input_grid = [[0 for _ in range(width)] for _ in range(height)]
            solid_square(input_grid, height // 2, 63)

        case "random":
            width, height, tile_size, fps = 400, 300, 2, -1
            input_grid = [[secrets.choice(range(6)) for col in range(width)] for _ in range(height)]

        case "obstacle":
            width, height, tile_size, fps = 400, 300, 2, -1

            input_grid = [
                [secrets.choice(range(64)) if col < width // 2 and secrets.SystemRandom().random() < 0.3 else 0 for col
                 in
                 range(width)]
                for _ in range(height)
            ]

            obstacle_value = len(colors) - 1

            # frame(grid=input_grid, value=obstacle_value, size=1)
            # solid_rectangle(
            #     grid=input_grid, value=obstacle_value, height=height // 3, width=4, left_offset=width // 8 + 2,
            # )

        case "single":
            width, height, tile_size, fps = 15, 14, 64, 4
            input_grid = [[0 for _ in range(width)] for _ in range(height)]
            row, col = height // 2, width // 2

            # input_grid[row][col] = 0b000001
            # input_grid[row][col] = 0b000010
            # input_grid[row][col] = 0b000100
            # input_grid[row][col] = 0b001000
            # input_grid[row][col] = 0b010000
            # input_grid[row][col] = 0b100000

            # input_grid[row][col] = 0b111111

            # input_grid[row - 3][col] = 0b000100  # E
            # input_grid[row + 3][col] = 0b100000  # S

            # input_grid[row + 2][col - 3] = 0b000001  # NE
            # input_grid[row - 1][col + 3] = 0b001000  # SW

            input_grid[row - 1][col - 3] = 0b000010  # SE
            input_grid[row + 2][col + 3] = 0b010000  # NW

            # for x in range(0, 12, 3):
            #     row, col = 1 + x, round(width / 2) + 1
            #     input_grid[row][col] = 1
            #     for (row_off, col_off) in settings.HONEYCOMB[col % 2]:
            #         input_grid[row + row_off][col + col_off] = 3

    automaton = FhpOne(grid=input_grid)
    board = HexagonalGrid(
        title="LGCA FHP I",
        automaton=automaton,
        tile_size=tile_size,
        colors=colors,
        fps=fps,
        run=False,
    )
    assert isinstance(board, HexagonalGrid)

    board.mainloop()
