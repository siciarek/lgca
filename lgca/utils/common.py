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


def parse_integer_value(value: str) -> int:
    for base, pref in {2: "0b", 8: "0o", 16: "0x"}.items():
        if pref in value:
            return int(value.replace(pref, ""), base)

    return int(value, 10)


def get_color_palette(bit_count: int):
    palette, step, color = [], round(0xFF / bit_count), 0xFF

    while len(palette) < bit_count + 1:
        palette.append(f"#{color:02X}{color:02X}{color:02X}")
        color -= step

    if palette[-1] != "#000000":
        palette[-1] = "#000000"

    return palette[::-1]


def get_color_map(bit_count, reverse: bool = False, obstacle_color: str = "#AA0000"):
    color_palette = get_color_palette(bit_count)

    if reverse:
        color_palette.reverse()

    temp_map = defaultdict(dict)
    color_map = [0] * 256

    for i in range(2**bit_count):
        tmpl = f"{{value:0{bit_count}b}}"
        key = tmpl.format(value=i)
        bit_count = i.bit_count()
        temp_map[bit_count][key] = color_palette[bit_count]

    obstacle_color = decode_color(color=obstacle_color)

    for _, values in temp_map.items():
        for key, val in values.items():
            int_key, rgb = int(key, 2), decode_color(color=val)
            color_map[int_key] = rgb

            if not int_key & Lgca.REST_PARTICLE_BIT:
                obstacle_key = int_key | Lgca.OBSTACLE_BIT
                color_map[obstacle_key] = tuple([c if c > 0 else rgb[0] for c in obstacle_color])

    while color_map[-1] == 0:
        color_map.pop()

    return tuple(color_map)
