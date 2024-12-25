import secrets
import random
import json
from pathlib import Path
from typing import Callable
from functools import partial
from collections import defaultdict
import click
from lgca.automata import (
    Lgca,
    Hpp,
    FhpI,
    FhpII,
    FhpIII,
)
from lgca.display import (
    SquareGrid,
    HexagonalGrid,
)
from lgca.utils.add_shape import (
    solid_square,
    frame,
    solid_rectangle,
    solid_circle,
)
from lgca.utils.table_generator import BIT_COUNT


def parse_value(value: str) -> int:
    if "0b" in value:
        return int(value.replace("0b", ""), 2)

    if "0o" in value:
        return int(value.replace("0o", ""), 8)

    if "0x" in value:
        return int(value.replace("0x", ""), 16)

    return int(value, 10)


def get_color_palette(num: int):
    palette, step, color = [], round(0xFF / num), 0xFF

    while len(palette) < num + 1:
        palette.append(f"#{color:02X}{color:02X}{color:02X}")
        color -= step

    if palette[-1] != "#000000":
        palette[-1] = "#000000"

    return palette[::-1]


def get_color_map(num, reverse: bool = False, obstacle_color: str = "#AA0000"):
    color_palette = get_color_palette(num)

    if reverse:
        color_palette.reverse()

    temp_map = defaultdict(dict)
    color_map = [0] * 256

    for i in range(2**num):
        template = f"{{value:0{num}b}}"
        key = template.format(value=i)
        bit_count = i.bit_count()
        temp_map[bit_count][key] = color_palette[bit_count]

    oc: str = obstacle_color.lstrip("#")
    obstacle_color = (int(oc[:2], 0x10), int(oc[2:4], 0x10), int(oc[4:], 0x10))

    for _, values in temp_map.items():
        for key, val in values.items():
            int_key = int(key, 2)
            val = val.lstrip("#")
            color_map[int_key] = (
                int(val[:2], 0x10),
                int(val[2:4], 0x10),
                int(val[4:], 0x10),
            )
            if not int_key & Lgca.REST_PARTICLE_BIT:
                color_map[(int_key | Lgca.OBSTACLE_BIT)] = tuple(
                    [w if w > 0 else int(val[:2], 0x10) for w in obstacle_color]
                )

    while color_map[-1] == 0:
        color_map.pop()

    return tuple(color_map)


def decode_json(ctx, param, value):
    return json.loads(value) if value is not None else None


@click.command()
@click.option("-v", "--value", type=str, default="0", show_default=True, help="Content value.")
@click.option("-t", "--tile-size", type=int, default=2, show_default=True, help="Grid tile size.")
@click.option(
    "-n",
    "--model-name",
    type=click.Choice(
        [
            "HPP",
            "FHP_I",
            "FHP_II",
            "FHP_III",
            "hpp",
            "fhp_i",
            "fhp_ii",
            "fhp_iii",
        ]
    ),
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
    default="obstacle",
    type=str,
    show_default=True,
    help="Select initial state pattern.",
)
@click.option(
    "-m",
    "--mode",
    default=Lgca.MODE_TORUS,
    type=click.Choice(["torus", "die"]),
    show_default=True,
    help="Automaton behavior when the particle reaches the edge.",
)
@click.option(
    "-x",
    "--extra-params",
    type=str,
    default={},
    callback=decode_json,
    help="Extra parameters provided to the application.",
)
def main(
    width: int,
    height: int,
    tile_size: int,
    model_name: str,
    steps: int,
    run: bool,
    pattern: str,
    value: str,
    deterministic: bool,
    mode: str,
    extra_params: dict,
):
    """
    Lattice Gas Cellular Automata
    [X] HPP
    [X] FHP I
    [X] FHP II
    [X] FHP III
    """

    value: int = parse_value(value=value)
    input_grid: list = [[0 for _ in range(width)] for _ in range(height)]
    fps: int = -1

    print(f"{value=} {value=:07b} {extra_params=}")

    if deterministic:
        rand_choice: Callable = random.choice
        rand_uniform: partial | Callable = partial(random.uniform, 0, 1)
        random.seed(42)
    else:
        rand_choice: Callable = secrets.choice
        rand_uniform: partial | Callable = secrets.SystemRandom().random

    model_name = model_name.lower()

    classes = {
        "hpp": (Hpp, SquareGrid),
        "fhp_i": (FhpI, HexagonalGrid),
        "fhp_ii": (FhpII, HexagonalGrid),
        "fhp_iii": (FhpIII, HexagonalGrid),
    }
    automaton_class, grid_class = classes[model_name]

    obstacle_color = "#880000"

    predefined_patterns = {"random", "alt", "single", "obstacle", "test"}

    if pattern in predefined_patterns:
        match model_name:
            case "fhp_iii":
                match pattern:
                    case "random":
                        width, height, tile_size, fps = 400, 300, 2, -1
                        input_grid = [[secrets.choice(range(128)) for _ in range(width)] for _ in range(height)]
                    case "obstacle":
                        width, height, tile_size, fps, mode = 400, 300, 2, -1, Lgca.MODE_TORUS

                        input_grid = [
                            [
                                rand_choice(range(127)) if rand_uniform() < 0.3 and col < width // 2 else 0
                                for col in range(width)
                            ]
                            for _ in range(height)
                        ]

                        solid_rectangle(
                            grid=input_grid,
                            value=Lgca.OBSTACLE_BIT,
                            height=height // 3,
                            width=4,
                            offset={"left": 50, "top": 0},
                        )
                        width, height, tile_size, fps = 400, 300, 2, -1
                        # input_grid = [
                        #     [rand_choice(range(128)) if col < width // 2 and rand_uniform() < 0.3 else 0 for col in
                        #      range(width)]
                        #     for _ in range(height)
                        # ]

                        frame(grid=input_grid, value=Lgca.OBSTACLE_BIT, size=tile_size)

                        # solid_circle(grid=input_grid, value=0, size=height // 5)
                        # solid_square(grid=input_grid, value=127, size=height // 12)

                        # solid_circle(
                        #     grid=input_grid,
                        #     size=1 + height // 4,
                        #     value=Lgca.OBSTACLE_BIT,
                        #     col_offset=80,
                        # )
                        # solid_rectangle(
                        #     grid=input_grid,
                        #     value=Lgca.OBSTACLE_BIT,
                        #     height=height // 3,
                        #     width=4,
                        #     offset={"left": width // 8 + 2, "top": 0},
                        # )
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

            case "fhp_ii":
                match pattern:
                    case "random":
                        width, height, tile_size, fps = 400, 300, 2, -1
                        input_grid = [[secrets.choice(range(63)) for _ in range(width)] for _ in range(height)]
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
                    case "obstacle-bis":
                        width, height, tile_size, fps, mode = 400, 300, 2, -1, Lgca.MODE_DIE

                        input_grid = [
                            [rand_choice(range(127)) if rand_uniform() < 0.08 else 0 for col in range(width)]
                            for _ in range(height)
                        ]

                        solid_circle(grid=input_grid, value=0, size=height // 5)
                        solid_square(grid=input_grid, value=127, size=height // 12)

                        solid_rectangle(
                            grid=input_grid,
                            value=Lgca.OBSTACLE_BIT,
                            height=height // 3,
                            width=4,
                            offset={"left": 100, "top": 0},
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

            case "fhp_i":
                match pattern:
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

                        offsets = [
                            (0b000100, -dist, 0),
                            (0b100000, dist, 0),
                            (0b000001, x, -dist),
                            (0b001000, -(dist - x), dist),
                            (0b000010, -(dist - x), -dist),
                            (0b010000, x, dist),
                        ]

                        input_grid[row][col] = Lgca.OBSTACLE_BIT

                        for mask, row_off, col_off in offsets:
                            if value & mask:
                                input_grid[row + row_off][col + col_off] = mask

                        frame(grid=input_grid, value=Lgca.OBSTACLE_BIT)

            case "hpp":
                match pattern:
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
                        width, height, tile_size, fps = 17, 17, 54, 4

                        input_grid = [[0 for _ in range(width)] for _ in range(height)]
                        row, col = height // 2, width // 2
                        dist = 4
                        offsets = [
                            (0b0001, -dist, 0),
                            (0b0010, 0, -dist),
                            (0b0100, dist, 0),
                            (0b1000, 0, dist),
                        ]

                        if value == 0:
                            value = 0xF

                        for mask, row_off, col_off in offsets:
                            if value & mask:
                                input_grid[row + row_off][col + col_off] = mask

                        if extra_params.get("center", True):
                            input_grid[row][col] = Lgca.OBSTACLE_BIT

                        frame(grid=input_grid, value=Lgca.OBSTACLE_BIT, size=1)
    else:
        pattern_file = Path(pattern)
        if not pattern_file.is_file():
            raise click.FileError(pattern_file.as_posix(), "pattern not available.")

        data = json.load(pattern_file.open())
        models = data.get("models", ["hhp", "fhp_i", "fhp_ii", "fhp_iii"])

        if model_name not in models:
            raise click.ClickException(f"Model {model_name!r} is not supported by pattern {pattern_file.as_posix()!r}")

        tile_size = data.get("tile_size", 2)
        obstacle_color = data.get("obstacle_color", "#FF0000")
        mode = data.get("mode", Lgca.MODE_TORUS)
        fps = data.get("fps", -1)
        input_grid = data["data"]

    automaton = automaton_class(grid=input_grid, mode=mode)
    colors = get_color_map(num=BIT_COUNT[model_name], obstacle_color=obstacle_color)
    grid_class(
        title=f"LGCA {automaton.name}",
        automaton=automaton,
        tile_size=tile_size,
        colors=colors,
        max_iteration=steps,
        run=run,
        fps=fps,
    ).mainloop()
