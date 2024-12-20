import secrets
import click
import yaml
from lgca.automata import Hpp, FhpOne
from lgca.display import SquareGrid, HexagonalGrid
from lgca.utils.initial_shape import solid_square, frame, solid_rectangle
from lgca import settings


@click.command()
@click.option("-v", "--value", type=click.IntRange(0, 255), default=15, help="Content value.")
@click.option(
    "-n",
    "--model-name",
    type=click.Choice(["HPP", "FHPI", "FHPII", "FHPIII", "hpp", "fhpi", "fhpii", "fhpiii"]),
    default="HPP",
)
@click.option("-w", "--width", default=300, show_default=True, help="Lattice window width.")
@click.option("-h", "--height", default=200, show_default=True, help="Lattice window height.")
@click.option("-s", "--steps", default=-1, show_default=True, help="Number of steps.")
@click.option("-r", "--run", is_flag=True, default=False, show_default=True, help="Run immediately.")
@click.option(
    "-p",
    "--pattern",
    default="wiki",
    type=click.Choice(["wiki", "random", "alt", "single", "obstacle", "test"]),
    show_default=True,
    help="Select initial state pattern.",
)
def main(width: int, height: int, model_name: str, steps: int, run: bool, pattern: str, value: int):
    """
    Lattice Gas Cellular Automata
    [X] HPP
    [X] FHP I
    [ ] FHP II
    [ ] FHP III
    """

    match model_name.upper():
        case "FHPI":
            match pattern:
                case "wiki":
                    width, height, tile_size, fps = 300, 200, 2, -1
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    solid_square(input_grid, height // 2, 0b111111)
                case "random":
                    width, height, tile_size, fps = 400, 300, 2, -1
                    input_grid = [[secrets.choice(range(64)) for _ in range(width)] for _ in range(height)]
                case "single":
                    width, height, tile_size, fps = 17, 18, 64, 4
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    row, col = height // 2, width // 2

                    input_grid[row][col] = value
                case "test":
                    width, height, tile_size, fps = 18, 17, 64, 4
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    row, col = height // 2, width // 2

                    offsets = (
                        (0b000100, -3, 0),
                        (0b100000, 3, 0),
                        (0b000001, 2, -3),
                        (0b001000, -1, 3),
                        (0b000010, -1, -3),
                        (0b010000, 2, 3),
                    )

                    for mask, row_off, col_off in offsets:
                        if value & mask:
                            input_grid[row + row_off][col + col_off] = mask

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

                    # input_grid[row - 1][col - 3] = 0b000010  # SE
                    # input_grid[row + 2][col + 3] = 0b010000  # NW
                    #
                    # for x in range(0, 12, 3):
                    #     row, col = 1 + x, round(width / 2) + 1
                    #     input_grid[row][col] = 1
                    #     for (row_off, col_off) in settings.HONEYCOMB[col % 2]:
                    #         input_grid[row + row_off][col + col_off] = 3

            colors = [None] * 64
            for key, val in yaml.safe_load((settings.BASE_PATH / "lgca" / "config" / "colors.yaml").open())[
                "fhpi"].items():
                val = val.lstrip("#")
                colors[int(key, 2)] = (int(val[:2], 16), int(val[2:4], 16), int(val[4:], 16))

            automaton = FhpOne(grid=input_grid)

            HexagonalGrid(
                title=f"LGCA {model_name}",
                automaton=automaton,
                tile_size=tile_size,
                colors=tuple(colors),
                max_iteration=steps,
                run=run,
                fps=fps,
            ).mainloop()

        case "HPP":

            col_palette = """
                0000:#000000

                0001:#444444
                0010:#444444
                0100:#444444
                1000:#444444

                0011:#888888
                0110:#888888
                0101:#888888
                1010:#888888
                1001:#888888
                1100:#888888

                0111:#CCCCCC
                1011:#CCCCCC
                1101:#CCCCCC
                1110:#CCCCCC

                1111:#FFFFFF
            """

            colors = [0] * (2 ** 7 + 16)

            for row in col_palette.strip().split("\n"):
                dat = row.strip()
                if not dat:
                    continue

                binary, hexa = row.strip().split(":")

                if not hexa:
                    continue

                hexa = hexa.lstrip("#")
                color = (int(hexa[:2], 16), int(hexa[2:4], 16), int(hexa[4:], 16))
                binary_num = int(binary, 2)
                colors[binary_num] = color
                obst_bin_num = binary_num | 0b1000_0000
                colors[obst_bin_num] = (
                    0xAA,
                    color[0],
                    color[0],
                )

            tile_size = 2
            fps = -1
            input_grid = [[0 for _ in range(width)] for _ in range(height)]

            rand_choice = secrets.choice
            rand_uniform = secrets.SystemRandom().random

            match pattern:
                case "wiki":
                    width, height, tile_size, fps = 300, 200, 2, -1
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    solid_square(input_grid, height // 2, 15)
                case "alt":
                    width, height, tile_size, fps = 400, 400, 1, -1
                    input_grid = [[rand_choice(range(16)) for _ in range(width)] for _ in range(height)]

                    for row in range(height - 37 - 90, height - 37):
                        for col in range(37, 37 + 100):
                            input_grid[row][col] = 0
                    frame(grid=input_grid, value=0b1000_0000, size=1)
                case "random":
                    width, height, tile_size, fps = 600, 400, 2, -1
                    input_grid = [[rand_choice(range(16)) for _ in range(width)] for _ in range(height)]

                    frame(grid=input_grid, value=0b1000_0000)
                case "single":
                    width, height, tile_size, fps = 13, 13, 64, 3
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    input_grid[height // 2][width // 2 + 0] = value
                case "obstacle":
                    width, height, tile_size, fps = 400, 300, 2, -1
                    input_grid = [
                        [
                            rand_choice(range(16)) if col < width // 2 and rand_uniform() < 0.3 else 0
                            for col in range(width)
                        ]
                        for _ in range(height)
                    ]

                    frame(grid=input_grid, value=0b1000_0000, size=tile_size)
                    solid_rectangle(
                        grid=input_grid,
                        value=0b1000_0000,
                        height=height // 3,
                        width=4,
                        left_offset=width // 8 + 2,
                    )

                case "test":
                    width, height, tile_size, fps = 13, 13, 64, 3

                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    if value & 0b0001:
                        input_grid[1][width // 2] = 1
                    if value & 0b0010:
                        input_grid[height // 2][1] = 2
                    if value & 0b0100:
                        input_grid[height - 2][width // 2] = 4
                    if value & 0b1000:
                        input_grid[height // 2][width - 2] = 8

                    input_grid[height // 2][width // 2 + 0] = 0b1000_0000

                    frame(grid=input_grid, value=0b1000_0000, size=1)

            automaton = Hpp(grid=input_grid)

            SquareGrid(
                title=f"LGCA {model_name}",
                automaton=automaton,
                tile_size=tile_size,
                colors=tuple(colors),
                max_iteration=steps,
                run=run,
                fps=fps,
            ).mainloop()

        case _:
            raise click.ClickException(f"{model_name=} is not supported yet.")
