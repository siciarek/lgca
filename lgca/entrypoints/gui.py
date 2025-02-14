import secrets
import random
import re
import json
from pathlib import Path
from typing import Callable

import click

from lgca.automata import (
    Lgca,
    Hpp,
    FhpI,
    FhpII,
    FhpIII,
    Lbm,
)
from cellular_automata_grids.grids import (
    SquareGrid,
    HexagonalGrid,
    TerminalSquareGrid,
)
from lgca.utils.add_shape import (
    frame,
    solid_rectangle,
    arbitrary_single_point,
    solid_circle,
)
from lgca.utils.table_generator import BIT_COUNT
from lgca.utils.common import (
    parse_integer_value,
    get_color_map,
    decode_pattern_file,
)
from lgca import settings

CLASSES = {
    "hpp": (Hpp, TerminalSquareGrid),
    "fhp_i": (FhpI, HexagonalGrid),
    "fhp_ii": (FhpII, HexagonalGrid),
    "fhp_iii": (FhpIII, HexagonalGrid),
    "lbm": (Lbm, SquareGrid),
}


def generate_test(model_name: str, extra_params: dict, size: tuple[int, int], value: int, dist: int = 4):
    width, height = size
    input_grid = [[0 for _ in range(width)] for _ in range(height)]
    row, col = height // 2, width // 2

    x = dist - 2

    offsets = []

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


def generate_obstacle(model_name: str, width, height, density: float = 0.3):
    if model_name == "lbm":
        width, height, tile_size, fps, mode = 400, 100, 2, -1, Lgca.MODE_TORUS
        input_grid = [[0 for _ in range(width)] for _ in range(height)]

        solid_circle(grid=input_grid, size=26, col_offset=-width // 4, value=Lgca.OBSTACLE_BIT)

        return input_grid, width, height, tile_size, fps, mode

    width, height, tile_size, fps, mode = width, height, 2, -1, Lgca.MODE_TORUS

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


def decode_json_callback(ctx, param, value):  # pylint: disable=unused-argument
    return json.loads(value) if value is not None else None


@click.command()
@click.option(
    "-e", "--select-every", default=1, show_default=True, help="Select only frames after specified number of steps."
)
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
            "LBM",
            "hpp",
            "fhp_i",
            "fhp_ii",
            "fhp_iii",
            "lbm",
        ]
    ),
    show_default=True,
    default="HPP",
    help="Model name.",
)
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
@click.option("-w", "--width", default=400, show_default=True, help="Lattice window width.")
@click.option("-h", "--height", default=300, show_default=True, help="Lattice window height.")
def main(
    width: int,
    height: int,
    tile_size: int,
    model_name: str,
    steps: int,
    select_every: int,
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

    [X] LBM
    """

    reverse_color_map = False
    obstacle_color_map = json.loads((settings.BASE_PATH / "lgca" / "config" / "colors.json").read_text())
    obstacle_color = obstacle_color_map.get(obstacle_color, obstacle_color)

    if not re.match(r"#[\dA-Fa-f]{6}", obstacle_color):
        raise click.ClickException(f"Invalid color name: {obstacle_color!r}")

    model_name = model_name.lower()
    decoded_value: int = parse_integer_value(value=value)
    fps: int = 10

    rand_choice: Callable = random.choice
    random.seed(42)

    if not deterministic:
        rand_choice = secrets.choice

    input_grid: list[list] = [
        [rand_choice(range(2 ** BIT_COUNT[model_name])) if model_name not in ("lbm",) else 0 for _ in range(width)]
        for _ in range(height)
    ]

    if pattern == "test":
        width, height, tile_size, fps = 17, 17, 54, 4
        input_grid = generate_test(
            model_name=model_name, extra_params=extra_params, size=(width, height), value=decoded_value
        )
    elif pattern == "single":
        width, height, tile_size, fps = 17, 17, 54, 7
        input_grid = [[0 for row in range(width)] for row in range(height)]
        frame(grid=input_grid, value=Lgca.OBSTACLE_BIT, size=2)
        arbitrary_single_point(grid=input_grid, row=-3, col=10, value=value)
    elif pattern == "obstacle":
        input_grid, width, height, tile_size, fps, mode = generate_obstacle(
            model_name=model_name, width=width, height=height
        )

    if model_name == "hpp" and pattern == "test":
        width, height, tile_size, fps = 400, 400, 1, -1
        small = width // 10
        reverse_color_map = False
        input_grid = [
            [rand_choice(range(1, 2 ** BIT_COUNT[model_name])) for row in range(width)] for row in range(height)
        ]
        value = 0  # 2 ** BIT_COUNT[model_name] - 1
        solid_rectangle(
            grid=input_grid, width=small, height=small, value=value, offset={"left": -2 * small, "top": 2 * small}
        )


    click.secho(
        f"{model_name=} {width=}, {height=}, {pattern=} value={decoded_value} value-bin={decoded_value:07b} {extra_params=}",
        fg="yellow",
    )

    if pattern not in {"random", "obstacle", "test", "single"}:
        input_grid, tile_size, mode, fps, obstacle_color = decode_pattern_file(
            pattern_file=Path(pattern),
            model_name=model_name,
        )

    colors = (
        ([(i, i * 2 % 0xFF, i) for i in range(0x100)])
        if model_name == "lbm"
        else get_color_map(bit_count=BIT_COUNT[model_name], obstacle_color=obstacle_color, reverse=reverse_color_map)
    )

    automaton_class, grid_class = CLASSES[model_name]
    automaton = automaton_class(
        grid=input_grid,
        mode=mode,
    )
    grid_class(
        title=f"{Lgca.name} {automaton.name}",
        automaton=automaton,
        tile_size=tile_size,
        colors=tuple(colors),
        max_iteration=steps,
        run=run,
        fps=fps,
        select_every=select_every,
    ).mainloop()
