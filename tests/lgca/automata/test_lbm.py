import pytest
from lgca.automata import Lgca, Lbm


@pytest.mark.parametrize("mode", (None, Lgca.MODE_TORUS, Lgca.MODE_DIE))
def test_general(mode):
    width = 17
    height = 17
    steps = 5

    input_grid = [[0 for _ in range(width)] for _ in range(height)]
    input_grid[height // 2][width // 2] = 0b001001

    automaton: Lbm = Lbm(grid=input_grid) if mode is None else Lbm(grid=input_grid, mode=mode)

    for _ in range(steps):
        next(automaton)
