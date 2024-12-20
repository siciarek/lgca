import secrets
import click
from lgca.automata import Hpp
from lgca.display import SquareGrid
from lgca.utils.initial_shape import solid_square, frame, solid_rectangle


@click.command()
@click.option("-c", "--cell", type=click.IntRange(0, 15), default=15, help="Cell content binary definition.")
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
def main(width: int, height: int, model_name: str, steps: int, run: bool, pattern: str, cell: int):
    """
    Lattice Gas Cellular Automata
    [X] HPP
    [ ] FHP I
    [ ] FHP II
    [ ] FHP III
    """

    match model_name.upper():
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

            colors = [0] * (2**7 + 16)

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
                    width, height = 300, 200

                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    solid_square(input_grid, height // 2, 15)
                case "alt":
                    height = width = 400
                    tile_size = 1

                    input_grid = [[rand_choice(range(16)) for _ in range(width)] for _ in range(height)]

                    for row in range(height - 37 - 90, height - 37):
                        for col in range(37, 37 + 100):
                            input_grid[row][col] = 0

                    frame(grid=input_grid, value=0b1000_0000, size=1)
                case "random":
                    fps = -1
                    width = 600
                    height = 400
                    tile_size = 2
                    input_grid = [
                        [rand_choice(range(16)) if width // 4 < col < width - width // 4 else 0 for col in range(width)]
                        for _ in range(height)
                    ]

                    input_grid = [[rand_choice(range(16)) for _ in range(width)] for _ in range(height)]

                    frame(grid=input_grid, value=0b1000_0000)
                case "single":
                    fps = 3
                    tile_size = 64
                    width = 13
                    height = 13
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    input_grid[height // 2][width // 2 + 0] = cell
                case "obstacle":
                    fps = -1
                    tile_size = 2
                    width = 400
                    height = 300
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
                    fps = 3
                    tile_size = 64
                    width = 13
                    height = 13

                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    if cell & 0b0001:
                        input_grid[1][width // 2] = 1
                    if cell & 0b0010:
                        input_grid[height // 2][1] = 2
                    if cell & 0b0100:
                        input_grid[height - 2][width // 2] = 4
                    if cell & 0b1000:
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
