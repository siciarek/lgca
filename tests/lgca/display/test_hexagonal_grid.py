import random
from lgca.automata import FhpThree
from lgca.display import HexagonalGrid


def test_general():
    width = 300
    height = 200

    input_grid = [[random.choice(range(16)) for _ in range(width)] for _ in range(height)]
    automaton = FhpThree(grid=input_grid)

    disp = HexagonalGrid(
        title=automaton.name,
        automaton=automaton,
    )

    assert isinstance(disp, HexagonalGrid)
