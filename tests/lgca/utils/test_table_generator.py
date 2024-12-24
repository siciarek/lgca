import re
import pytest
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
