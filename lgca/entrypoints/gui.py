import secrets
import random
from functools import partial
import click
import yaml
from lgca.automata import (
    Lgca,
    Hpp,
    FhpOne,
    FhpTwo,
    FhpThree,
)
from lgca.display import SquareGrid, HexagonalGrid
from lgca.utils.add_shape import solid_square, frame, solid_rectangle
from lgca import settings


def generate_color_palette(num: int):
    palette, step, color = [], round(0xFF / num), 0xFF
    while color >= 0:
        palette.append(f"#{color:02X}{color:02X}{color:02X}")
        color -= step
    if palette[-1] != "#000000":
        palette[-1] = "#000000"
    return palette[::-1]


def set_up_colors(binary, hexa, colors):
    if not hexa:
        return

    if isinstance(hexa, str):
        hexa = hexa.lstrip("#")
        color = (int(hexa[:2], 16), int(hexa[2:4], 16), int(hexa[4:], 16))
        binary_num = int(binary, 2)
        colors[binary_num] = color
    else:
        binary_num = binary
        color = hexa

    while len(colors) <= 0xFF:
        colors += [0]

    obst_bin_num = binary_num | Lgca.OBSTACLE_BIT

    colors[obst_bin_num] = (
        0xAA,
        color[0],
        color[0],
    )


@click.command()
@click.option("-v", "--value", type=str, default="0", show_default=True, help="Content value.")
@click.option(
    "-n",
    "--model-name",
    type=click.Choice(["HPP", "FHPI", "FHPII", "FHPIII", "hpp", "fhpi", "fhpii", "fhpiii"]),
    show_default=True,
    default="HPP",
    help="Model name.",
)
@click.option("-w", "--width", default=300, show_default=True, help="Lattice window width.")
@click.option("-h", "--height", default=200, show_default=True, help="Lattice window height.")
@click.option("-s", "--steps", default=-1, show_default=True, help="Number of steps.")
@click.option("-r", "--run", is_flag=True, default=False, show_default=True, help="Run immediately.")
@click.option(
    "-d",
    "--deterministic",
    is_flag=True,
    default=True,
    show_default=True,
    help="Generate the same randomized result for the same params.",
)
@click.option(
    "-p",
    "--pattern",
    default="wiki",
    type=click.Choice(["wiki", "random", "alt", "single", "obstacle", "test"]),
    show_default=True,
    help="Select initial state pattern.",
)
def main(
    width: int, height: int, model_name: str, steps: int, run: bool, pattern: str, value: str, deterministic: bool
):
    """
    Lattice Gas Cellular Automata
    [X] HPP
    [X] FHP I
    [X] FHP II
    [ ] FHP III
    """

    if "0b" in value:
        value = int(value.replace("0b", ""), 2)
    elif "0o" in value:
        value = int(value.replace("0o", ""), 8)
    elif "0x" in value:
        value = int(value.replace("0x", ""), 16)
    else:
        value = int(value, 10)

    print(f"{value=} {value=:07b}")

    if deterministic:
        rand_choice = random.choice
        rand_uniform = partial(random.uniform, 0, 1)
        random.seed(42)
    else:
        rand_choice = secrets.choice
        rand_uniform = secrets.SystemRandom().random

    match model_name.upper():
        case "FHPIII":
            match pattern:
                case "wiki":
                    width, height, tile_size, fps = 300, 200, 2, -1
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    solid_square(input_grid, height // 2, 0b111111)
                case "random":
                    width, height, tile_size, fps = 400, 300, 2, -1
                    input_grid = [[secrets.choice(range(128)) for _ in range(width)] for _ in range(height)]
                case "obstacle":
                    width, height, tile_size, fps = 400, 300, 2, -1
                    input_grid = [
                        [
                            rand_choice(range(16)) if col < width // 2 and rand_uniform() < 0.3 else 0
                            for col in range(width)
                        ]
                        for _ in range(height)
                    ]

                    frame(grid=input_grid, value=Lgca.OBSTACLE_BIT, size=tile_size)
                    solid_rectangle(
                        grid=input_grid,
                        value=Lgca.OBSTACLE_BIT,
                        height=height // 3,
                        width=4,
                        offset={"left": width // 8 + 2, "top": 0},
                    )
                case "single":
                    width, height, tile_size, fps = 17, 18, 64, 4
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    row, col = height // 2, width // 2

                    input_grid[row][col] = value
                case "test":
                    width, height, tile_size, fps = 19, 19, 60, 4
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    row, col = height // 2, width // 2

                    dist = 3
                    x = dist - 1

                    offsets = (
                        (0b1000000, 0, 0),
                        (0b0000100, -dist, 0),
                        (0b0100000, dist, 0),
                        (0b0000001, x, -dist),
                        (0b0001000, -(dist - x), dist),
                        (0b0000010, -(dist - x), -dist),
                        (0b0010000, x, dist),
                    )

                    # input_grid[row][col] = 0b1000_0000

                    # HONEYCOMB
                    # for (row_off, col_off) in settings.HONEYCOMB[col % 2]:
                    #     input_grid[row + row_off][col + col_off] = 0b1000_0000

                    frame(grid=input_grid, value=0b1000_0000)

                    for mask, row_off, col_off in offsets:
                        if value & mask:
                            input_grid[row + row_off][col + col_off] = mask

            color_temp = {}
            for i in range(0b111_1111 + 1):
                if i.bit_count() not in color_temp:
                    color_temp[i.bit_count()] = []
                color_temp[i.bit_count()].append(i)

            palette = generate_color_palette(len(color_temp))

            xcolors = {}
            for bits, values in color_temp.items():
                for val in values:
                    xcolors[f"{val:07b}"] = palette[bits]

            colors = [None] * 128
            for key, val in xcolors.items():
                val = val.lstrip("#")
                colors[int(key, 2)] = (int(val[:2], 16), int(val[2:4], 16), int(val[4:], 16))
                set_up_colors(int(key, 2), colors[int(key, 2)], colors)

            automaton = FhpThree(grid=input_grid)
            title = f"LGCA {automaton.name}"
            HexagonalGrid(
                title=title,
                automaton=automaton,
                tile_size=tile_size,
                colors=tuple(colors),
                max_iteration=steps,
                run=run,
                fps=fps,
                # background="#FFFFAA",
            ).mainloop()

        case "FHPII":
            match pattern:
                case "wiki":
                    width, height, tile_size, fps = 300, 200, 2, -1
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    solid_square(input_grid, height // 2, 0b111111)
                case "random":
                    width, height, tile_size, fps = 400, 300, 2, -1
                    input_grid = [[secrets.choice(range(128)) for _ in range(width)] for _ in range(height)]
                case "obstacle":
                    width, height, tile_size, fps = 400, 300, 2, -1
                    input_grid = [
                        [
                            rand_choice(range(16)) if col < width // 2 and rand_uniform() < 0.3 else 0
                            for col in range(width)
                        ]
                        for _ in range(height)
                    ]

                    frame(grid=input_grid, value=Lgca.OBSTACLE_BIT, size=tile_size)
                    solid_rectangle(
                        grid=input_grid,
                        value=Lgca.OBSTACLE_BIT,
                        height=height // 3,
                        width=4,
                        offset={"left": width // 8 + 2, "top": 0},
                    )
                case "single":
                    width, height, tile_size, fps = 17, 18, 64, 4
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    row, col = height // 2, width // 2

                    input_grid[row][col] = value
                case "test":
                    width, height, tile_size, fps = 19, 19, 60, 4
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    row, col = height // 2, width // 2

                    dist = 3
                    x = dist - 1

                    offsets = (
                        (0b1000000, 0, 0),
                        (0b000100, -dist, 0),
                        (0b100000, dist, 0),
                        (0b000001, x, -dist),
                        (0b001000, -(dist - x), dist),
                        (0b000010, -(dist - x), -dist),
                        (0b010000, x, dist),
                    )

                    # input_grid[row][col] = 0b1000_0000

                    # HONEYCOMB
                    # for (row_off, col_off) in settings.HONEYCOMB[col % 2]:
                    #     input_grid[row + row_off][col + col_off] = 0b1000_0000

                    frame(grid=input_grid, value=Lgca.OBSTACLE_BIT)

                    for mask, row_off, col_off in offsets:
                        if value & mask:
                            input_grid[row + row_off][col + col_off] = mask

            color_temp = {}
            for i in range(0b111_1111 + 1):
                if i.bit_count() not in color_temp:
                    color_temp[i.bit_count()] = []
                color_temp[i.bit_count()].append(i)

            palette = generate_color_palette(len(color_temp))

            xcolors = {}
            for bits, values in color_temp.items():
                for val in values:
                    xcolors[f"{val:07b}"] = palette[bits]

            colors = [None] * 128
            for key, val in xcolors.items():
                val = val.lstrip("#")
                colors[int(key, 2)] = (int(val[:2], 16), int(val[2:4], 16), int(val[4:], 16))
                set_up_colors(int(key, 2), colors[int(key, 2)], colors)

            automaton = FhpTwo(grid=input_grid)
            title = f"LGCA {automaton.name}"
            HexagonalGrid(
                title=title,
                automaton=automaton,
                tile_size=tile_size,
                colors=tuple(colors),
                max_iteration=steps,
                run=run,
                fps=fps,
                # background="#FFFFAA",
            ).mainloop()

        case "FHPI":
            match pattern:
                case "wiki":
                    width, height, tile_size, fps = 300, 200, 2, -1
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    solid_square(input_grid, height // 2, 0b111111)
                case "random":
                    width, height, tile_size, fps = 400, 300, 2, -1
                    input_grid = [[secrets.choice(range(64)) for _ in range(width)] for _ in range(height)]
                case "obstacle":
                    width, height, tile_size, fps = 400, 300, 2, -1
                    input_grid = [
                        [
                            rand_choice(range(16)) if col < width // 2 and rand_uniform() < 0.3 else 0
                            for col in range(width)
                        ]
                        for _ in range(height)
                    ]

                    frame(grid=input_grid, value=Lgca.OBSTACLE_BIT, size=tile_size)
                    solid_rectangle(
                        grid=input_grid,
                        value=Lgca.OBSTACLE_BIT,
                        height=height // 3,
                        width=4,
                        offset={"left": width // 8 + 2, "top": 0},
                    )
                case "single":
                    width, height, tile_size, fps = 17, 18, 64, 4
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    row, col = height // 2, width // 2

                    input_grid[row][col] = value
                case "test":
                    width, height, tile_size, fps = 19, 19, 60, 4
                    input_grid = [[0 for _ in range(width)] for _ in range(height)]
                    row, col = height // 2, width // 2

                    dist = 3
                    x = dist - 1

                    offsets = (
                        (0b000100, -dist, 0),
                        (0b100000, dist, 0),
                        (0b000001, x, -dist),
                        (0b001000, -(dist - x), dist),
                        (0b000010, -(dist - x), -dist),
                        (0b010000, x, dist),
                    )

                    input_grid[row][col] = Lgca.OBSTACLE_BIT

                    # HONEYCOMB
                    # for (row_off, col_off) in settings.HONEYCOMB[col % 2]:
                    #     input_grid[row + row_off][col + col_off] = 0b1000_0000

                    for mask, row_off, col_off in offsets:
                        if value & mask:
                            input_grid[row + row_off][col + col_off] = mask

                    frame(grid=input_grid, value=Lgca.OBSTACLE_BIT)

                    # for x in range(0, 12, 3):
                    #     row, col = 1 + x, round(width / 2) + 1
                    #     input_grid[row][col] = 1
                    #     for (row_off, col_off) in settings.HONEYCOMB[col % 2]:
                    #         input_grid[row + row_off][col + col_off] = 3

            colors = [None] * 64
            for key, val in yaml.safe_load((settings.BASE_PATH / "lgca" / "config" / "colors.yaml").open())[
                "fhp_6bits"
            ].items():
                val = val.lstrip("#")
                colors[int(key, 2)] = (int(val[:2], 16), int(val[2:4], 16), int(val[4:], 16))
                set_up_colors(int(key, 2), colors[int(key, 2)], colors)

            automaton = FhpOne(grid=input_grid)
            HexagonalGrid(
                title=f"LGCA {automaton.name}",
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

            colors = [0] * (2**7 + 16)

            for row in col_palette.strip().split("\n"):
                dat = row.strip()
                if not dat:
                    continue

                binary, hexa = row.strip().split(":")
                set_up_colors(binary=binary, hexa=hexa, colors=colors)

            tile_size = 2
            fps = -1
            input_grid = [[0 for _ in range(width)] for _ in range(height)]

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

                    frame(grid=input_grid, value=Lgca.OBSTACLE_BIT, size=tile_size)
                    solid_rectangle(
                        grid=input_grid,
                        value=Lgca.OBSTACLE_BIT,
                        height=height // 3,
                        width=4,
                        offset={"left": width // 8 + 2, "top": 0},
                    )

                case "test":
                    width, height, tile_size, fps = 19, 19, 54, 4

                    input_grid = [[0 for _ in range(width)] for _ in range(height)]

                    value = int(value)

                    if value & 0b0001:
                        input_grid[1][width // 2] = 1
                    if value & 0b0010:
                        input_grid[height // 2][1] = 2
                    if value & 0b0100:
                        input_grid[height - 2][width // 2] = 4
                    if value & 0b1000:
                        input_grid[height // 2][width - 2] = 8

                    input_grid[height // 2][width // 2 + 0] = Lgca.OBSTACLE_BIT

                    frame(grid=input_grid, value=Lgca.OBSTACLE_BIT, size=1)

            automaton = Hpp(grid=input_grid)
            SquareGrid(
                title=f"LGCA {automaton.name}",
                automaton=automaton,
                tile_size=tile_size,
                colors=tuple(colors),
                max_iteration=steps,
                run=run,
                fps=fps,
            ).mainloop()

        case _:
            raise click.ClickException(f"{model_name=} is not supported yet.")
