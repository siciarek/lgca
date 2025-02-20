from lgca import settings
from lgca.automata import Lgca
from lgca.automata.lgca_faster import LgcaFaster as Lgca


class Hpp(Lgca):
    name: str = "HPP"
    masks: tuple[int, int, int, int] = (
        0b0001,
        0b1000,
        0b0010,
        0b0100,
    )
    neighborhood: tuple = (
        settings.VON_NEUMANN_NEIGHBORHOOD.values(),
        settings.VON_NEUMANN_NEIGHBORHOOD.values(),
    )
