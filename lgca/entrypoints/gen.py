import numpy as np
from pathlib import Path
import click
from PIL import Image
from lgca.automata import (
    Hpp,
)
from lgca.utils.common import decode_pattern_file, get_color_map
from lgca.utils.table_generator import BIT_COUNT


@click.command()
@click.option("-s", "--steps", default=0, show_default=True, help="Number of steps.")
@click.option(
    "-n", "--model-name", type=click.Choice(["HPP", "hpp"]), show_default=True, default="hpp", help="Model name."
)
@click.option(
    "-p",
    "--pattern",
    default="",
    type=str,
    show_default=False,
    help="Select initial state pattern.",
)
def main(steps: int, model_name: str, pattern: str):
    """Generate image of LGCA."""

    pattern_file = Path(pattern)
    if not pattern_file.is_file():
        raise click.FileError(pattern_file.as_posix(), "pattern not found.")

    step_tmpl = f"STEP: {{step:0{len(str(steps))}}}"
    file_tmpl = f"{pattern_file.stem}-{{model_name}}-{{step:0{len(str(steps))}}}.png"

    input_grid, tile_size, mode, fps, obstacle_color = decode_pattern_file(
        pattern_file=pattern_file,
        model_name=model_name,
    )
    color_map = get_color_map(bit_count=BIT_COUNT[model_name], obstacle_color=obstacle_color)

    if model_name == "hpp":
        automaton = Hpp(
            grid=input_grid,
            mode=mode,
        )
    else:
        raise click.ClickException(f"Model {model_name} is not supported yet.")

    while steps:
        next(automaton)
        print(step_tmpl.format(step=automaton.step), end="\r")
        steps -= 1

    bitmap_array: list = []
    for row in input_grid:
        bitmap_array.append([color_map[cell] for cell in row])

    img: Image = Image.fromarray(np.array(np.uint8(bitmap_array)))
    img = img.resize(size=[elem * tile_size for elem in img.size], resample=Image.Resampling.NEAREST)
    img.save(file_tmpl.format(model_name=model_name, step=automaton.step))
