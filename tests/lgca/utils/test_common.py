import pytest
from lgca.utils.common import (
    get_color_palette,
    get_color_map,
    parse_integer_value,
    decode_pattern_file,
)
from lgca.utils.table_generator import BIT_COUNT
from lgca import settings

parse_integer_value_data_provider = (
    ("0b0101", 5),
    ("0o0101", 65),
    ("0x0101", 257),
    ("0101", 101),
)


@pytest.mark.parametrize("value, expected", parse_integer_value_data_provider)
def test_parse_integer_value(value: str, expected: int):
    assert parse_integer_value(value=value) == expected, (value, expected)


def test_get_color_palette():
    for bit_count in range(2, 8 + 1):
        color_palette = get_color_palette(bit_count=bit_count)
        assert isinstance(color_palette, list)


def test_get_color_map_smoke_test():
    for _, bit_count in BIT_COUNT.items():
        color_map = get_color_map(
            bit_count=bit_count,
        )
        reversed_color_map = get_color_map(
            bit_count=bit_count,
            reverse=True,
        )

        assert isinstance(color_map, tuple)
        assert isinstance(reversed_color_map, tuple)


def test_decode_pattern_file():
    pattern_file = settings.BASE_PATH / "lgca" / "data" / "patterns" / "hpp" / "collision.json"
    model_name = "hpp"

    input_grid, *_ = decode_pattern_file(pattern_file=pattern_file, model_name=model_name)
    assert isinstance(input_grid, list)

    pattern_file = settings.BASE_PATH / "lgca" / "data" / "patterns" / "hpp" / "invalid-name.json"
    model_name = "hpp"
    match = pattern_file.as_posix()
    with pytest.raises(FileNotFoundError, match=match):
        decode_pattern_file(pattern_file=pattern_file, model_name=model_name)

    pattern_file = settings.BASE_PATH / "lgca" / "data" / "patterns" / "hpp" / "collision.json"
    model_name = "hppx"
    match = f"Model {model_name!r} is not supported by pattern {pattern_file.as_posix()!r}"
    with pytest.raises(ValueError, match=match):
        decode_pattern_file(pattern_file=pattern_file, model_name=model_name)
