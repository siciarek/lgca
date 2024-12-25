from collections import defaultdict
import yaml
from lgca import settings

BIT_COUNT: dict = {
    "hpp": 4,
    "fhp_i": 6,
    "fhp_ii": 7,
    "fhp_iii": 7,
}


def get_collisions(name: str | None = None) -> dict:
    collisions = yaml.safe_load((settings.BASE_PATH / "lgca" / "config" / "collisions.yaml").open())
    if name is None:
        return collisions
    if name not in collisions:
        raise AttributeError(f"Name {name!r} is not supported, only {list(collisions.keys())} are valid.")

    return collisions[name]


def generate_lookup_table(name: str) -> dict:
    if name not in BIT_COUNT:
        raise AttributeError(f"Name {name!r} is not supported, only {list(BIT_COUNT.keys())} are valid.")

    collisions: dict = get_collisions(name)
    bits: int = BIT_COUNT[name]

    temp_table: defaultdict = defaultdict(dict)
    lookup_table: dict = {}

    for i in range(2**bits):
        template = "{value:0" + str(bits) + "b}"
        key = template.format(value=i)
        temp_table[i.bit_count()][key] = collisions.get(key, key)

    for _, values in temp_table.items():
        for key, val in values.items():
            lookup_table[key] = val

    return lookup_table
