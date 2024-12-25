import numpy as np
from pathlib import Path
from PIL import Image
from lgca.automata import (
    Hpp,
)
from lgca.utils.common import decode_pattern_file, get_color_palette
from lgca.utils.table_generator import BIT_COUNT


def display(grid: list):
    result: list[str] = []
    for row in grid:
        result.append("".join(["." if i == 0 else str(i) for i in row]))

    print("\n".join(result))


def decode_color(color: str):
    color = color.lstrip("#")
    return (
        int(color[:2], 0x10),
        int(color[2:4], 0x10),
        int(color[4:], 0x10),
    )


def main():
    pattern = "lgca/data/patterns/hpp/wiki.json"
    model_name = "hpp"
    steps = 0

    color_palette = get_color_palette(num=BIT_COUNT[model_name])
    bitmap = []

    input_grid, tile_size, mode, fps, obstacle_color = decode_pattern_file(
        pattern_file=Path(pattern),
        model_name=model_name,
    )

    if model_name == "hpp":
        automaton = Hpp(
            grid=input_grid,
            mode=mode,
        )

    while steps:
        next(automaton)

    for row in input_grid:
        bitmap.append([list(decode_color(color_palette[cell.bit_count()])) for cell in row])

    img = Image.fromarray(np.array(bitmap))

    print(color_palette)
    display(bitmap)
    print(img)
