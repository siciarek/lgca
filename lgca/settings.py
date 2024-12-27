from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
LGCA_CONFIGURATION_PATH = BASE_PATH / "lgca" / "config"

VON_NEUMANN_NEIGHBORHOOD = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (0, -1),
    "W": (1, 0),
}

HONEYCOMB = (
    (  # col % 2 == 0
        (-1, 1),
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, -1),
        (-1, 0),
    ),
    (  # col % 2 == 1
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, 0),
    ),
)
