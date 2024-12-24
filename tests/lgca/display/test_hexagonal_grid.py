import random
from lgca import automata as a
from lgca.display import HexagonalGrid


def test_general():
    width = 300
    height = 200

    input_grid = [[random.choice(range(16)) for _ in range(width)] for _ in range(height)]

    for cls in [a.FhpI, a.FhpII, a.FhpIII]:
        automaton = cls(grid=input_grid)

        disp = HexagonalGrid(
            title=automaton.name,
            automaton=automaton,
        )

        assert isinstance(disp, HexagonalGrid)
