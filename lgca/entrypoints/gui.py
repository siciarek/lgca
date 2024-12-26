import secrets
import random
import json
from pathlib import Path
from typing import Callable
from functools import partial

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
from lgca.utils.common import (
    parse_integer_value,
    get_color_map,
    decode_pattern_file,
)


def generate_test(model_name: str, extra_params: dict, height: int, value: int, width: int, dist: int = 4):
    input_grid = [[0 for _ in range(width)] for _ in range(height)]
    row, col = height // 2, width // 2

    x = dist - 2

    if model_name in ("fhp_ii", "fhp_iii"):
        offsets = [
            (0b0000100, -dist, 0),
            (0b0100000, dist, 0),
            (0b0000001, x, -dist),
            (0b0001000, -(dist - x), dist),
            (0b0000010, -(dist - x), -dist),
            (0b0010000, x, dist),
            (Lgca.REST_PARTICLE_BIT, 0, 0),
        ]
    elif model_name == "fhp_i":
        offsets = [
            (0b0000100, -dist, 0),
            (0b0100000, dist, 0),
            (0b0000001, x, -dist),
            (0b0001000, -(dist - x), dist),
            (0b0000010, -(dist - x), -dist),
            (0b0010000, x, dist),
        ]
    elif model_name == "hpp":
        offsets = [
            (0b0001, -dist, 0),
            (0b0010, 0, -dist),
            (0b0100, dist, 0),
            (0b1000, 0, dist),
        ]

    for mask, row_off, col_off in offsets:
        if value & mask:
            input_grid[row + row_off][col + col_off] = mask

    frame(grid=input_grid, value=Lgca.OBSTACLE_BIT)

    if extra_params.get("center", False):
        input_grid[row][col] = Lgca.OBSTACLE_BIT

    return input_grid


def generate_obstacle(model_name: str, density: float = 0.3):
    width, height, tile_size, fps, mode = 400, 300, 2, -1, Lgca.MODE_TORUS

    input_grid = [
        [
            (
                secrets.choice(range(2 ** BIT_COUNT[model_name]))
                if secrets.SystemRandom().random() < density and col < width // 2
                else 0
            )
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

    return input_grid, width, height, tile_size, fps, mode


def decode_json_callback(ctx, param, value):
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
    type=click.Choice([Lgca.MODE_TORUS, Lgca.MODE_DIE]),
    show_default=True,
    help="Automaton behavior when the particle reaches the edge.",
)
@click.option(
    "-o",
    "--obstacle-color",
    default="#440044",
    type=str,
    show_default=True,
    help="Obstacle color.",
)
@click.option(
    "-x",
    "--extra-params",
    type=str,
    default={},
    callback=decode_json_callback,
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
    obstacle_color: str,
    extra_params: dict,
):
    """
    Lattice Gas Cellular Automata
    [X] HPP
    [X] FHP I
    [X] FHP II
    [X] FHP III
    """

    model_name: str = model_name.lower()
    value: int = parse_integer_value(value=value)
    fps: int = -1

    if deterministic:
        rand_choice: Callable = random.choice
        rand_uniform: partial | Callable = partial(random.uniform, 0, 1)
        random.seed(42)
    else:
        rand_choice: Callable = secrets.choice
        rand_uniform: partial | Callable = secrets.SystemRandom().random

    input_grid: list[list] = [
        [rand_choice(range(2 ** BIT_COUNT[model_name])) for _ in range(width)] for _ in range(height)
    ]

    if pattern == "test":
        width, height, tile_size, fps = 17, 17, 54, 4
        input_grid = generate_test(
            model_name=model_name, extra_params=extra_params, width=width, height=height, value=value
        )
    elif pattern == "obstacle":
        input_grid, width, height, tile_size, fps, mode = generate_obstacle(model_name=model_name)

    print(f"{model_name=} {pattern=} {value=} {value=:07b} {extra_params=}")

    classes = {
        "hpp": (Hpp, SquareGrid),
        "fhp_i": (FhpI, HexagonalGrid),
        "fhp_ii": (FhpII, HexagonalGrid),
        "fhp_iii": (FhpIII, HexagonalGrid),
    }

    if pattern in {"random", "obstacle", "test"}:
        match model_name:
            case "fhp_ii":
                match pattern:
                    case "obstacle-bis":
                        width, height, tile_size, fps, mode = 400, 300, 2, -1, Lgca.MODE_DIE

                        input_grid = [
                            [rand_choice(range(2 ** BIT_COUNT[model_name])) if rand_uniform() < 0.08 else 0 for col in range(width)]
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
    else:
        input_grid, tile_size, mode, fps, obstacle_color = decode_pattern_file(
            pattern_file=Path(pattern),
            model_name=model_name,
        )

    automaton_class, grid_class = classes[model_name]
    automaton = automaton_class(grid=input_grid, mode=mode)
    colors = get_color_map(bit_count=BIT_COUNT[model_name], obstacle_color=obstacle_color)
    grid_class(
        title=f"{Lgca.name} {automaton.name}",
        automaton=automaton,
        tile_size=tile_size,
        colors=colors,
        max_iteration=steps,
        run=run,
        fps=fps,
    ).mainloop()
