import random
from lgca.automata import Hpp
from lgca.display import SquareGrid


def test_general():
    width = 300
    height = 200

    input_grid = [[random.choice(range(16)) for _ in range(width)] for _ in range(height)]
    automaton = Hpp(grid=input_grid)

    disp = SquareGrid(
        title=automaton.name,
        automaton=automaton,
    )

    assert isinstance(disp, SquareGrid)
