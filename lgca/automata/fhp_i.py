from lgca import settings
from lgca.automata import Lgca


class FhpI(Lgca):
    name: str = "FHP I"
    masks: tuple[int, int, int, int, int, int] = (
        0b001000,
        0b010000,
        0b100000,
        0b000001,
        0b000010,
        0b000100,
    )

    def get_neighborhood(self, col):
        return settings.HONEYCOMB[col % 2]
