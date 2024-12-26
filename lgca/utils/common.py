import json
from pathlib import Path
from collections import defaultdict
from lgca.automata import Lgca


def decode_color(color: str):
    color = color.lstrip("#")
    return (
        int(color[:2], 0x10),
        int(color[2:4], 0x10),
        int(color[4:], 0x10),
    )


def decode_pattern_file(pattern_file: Path, model_name: str):
    if not pattern_file.is_file():
        raise FileNotFoundError(pattern_file.as_posix())

    data = json.load(pattern_file.open())
    models = data.get("models", ["hhp", "fhp_i", "fhp_ii", "fhp_iii"])

    if model_name not in models:
        raise ValueError(f"Model {model_name!r} is not supported by pattern {pattern_file.as_posix()!r}")

    tile_size = data.get("tile_size", 2)
    obstacle_color = data.get("obstacle_color", "#FF0000")
    mode = data.get("mode", Lgca.MODE_TORUS)
    fps = data.get("fps", -1)
    input_grid = data["data"]

    return input_grid, tile_size, mode, fps, obstacle_color


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
            rgb = val.lstrip("#")

            color_map[int_key] = (
                int(rgb[:2], 0x10),
                int(rgb[2:4], 0x10),
                int(rgb[4:], 0x10),
            )

            if not int_key & Lgca.REST_PARTICLE_BIT:
                obstacle_key = int_key | Lgca.OBSTACLE_BIT
                color_map[obstacle_key] = tuple([w if w > 0 else int(rgb[:2], 0x10) for w in obstacle_color])

    while color_map[-1] == 0:
        color_map.pop()

    return tuple(color_map)
