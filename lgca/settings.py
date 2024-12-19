from pathlib import Path

BASE_PATH = Path(__file__).parent.parent

VON_NEUMANN_NEIGHBORHOOD = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (0, -1),
    "W": (1, 0),
}

HONEYCOMB = {
    0: (  # col % 2 == 0
        (-1, 1),
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, -1),
        (-1, 0),
    ),
    1: (  # col % 2 == 1
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, 0),
    ),
}
