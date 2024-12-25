import re
import pytest
import csv
import yaml
from lgca import settings
from lgca.utils.table_generator import BIT_COUNT, generate_lookup_table, get_collisions

models = (
    "hpp",
    "fhp_i",
    "fhp_ii",
    "fhp_iii",
)


@pytest.mark.parametrize("name", models)
def test_generate_lookup_table(name: str):
    expected = yaml.safe_load((settings.BASE_PATH / "lgca" / "config" / f"{name}.yaml").open())["particle"]

    lookup_table = generate_lookup_table(name=name)
    assert isinstance(lookup_table, dict)
    assert lookup_table == expected


def test_validate_fhp_iii_lookup_table(name="fhp_iii"):
    """Validation against the lookup table form Buick PHD dissertation."""
    expected = yaml.safe_load((settings.BASE_PATH / "lgca" / "config" / f"{name}.yaml").open())["particle"]

    lookup_table = generate_lookup_table(name=name)
    assert isinstance(lookup_table, dict)
    assert lookup_table == expected

    buick_table_file = settings.BASE_PATH / "tests" / "data" / "buick.phd.lookup.table.csv"
    assert buick_table_file.is_file()

    first = True
    with buick_table_file.open() as fp:
        for row in csv.reader(fp):
            if first:
                first = False
                continue
            values = list(map(int, row))
            for map_values in [values[:3], values[3:]]:
                in_state, *out_state = map_values
                out_state.sort()
                out_state_bin = sorted([f"{i:07b}" for i in out_state])

                if out_state_bin[0] == out_state_bin[-1]:
                    out_state_bin = out_state_bin[0]

                in_state_bin = f"{in_state:07b}"

                assert in_state_bin in lookup_table, {in_state: out_state}
                assert lookup_table[in_state_bin] == out_state_bin or set(lookup_table[in_state_bin]), set(
                    out_state_bin
                )


def test_generate_lookup_table_exception():
    name = "invalid_name"
    match = re.escape(f"Name '{name}' is not supported, only {list(BIT_COUNT.keys())} are valid.")

    with pytest.raises(AttributeError, match=match) as exc_info:
        generate_lookup_table(name=name)

    assert isinstance(exc_info.value, AttributeError)


def test_get_collisions():
    name = "invalid_name"
    match = re.escape(f"Name '{name}' is not supported, only {list(BIT_COUNT.keys())} are valid.")

    actual = get_collisions()
    assert isinstance(actual, dict)

    for model in models:
        actual = get_collisions(name=model)
        assert isinstance(actual, dict)

    with pytest.raises(AttributeError, match=match) as exc_info:
        get_collisions(name=name)

    assert isinstance(exc_info.value, AttributeError)
