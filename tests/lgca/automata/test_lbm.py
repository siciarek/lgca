import pytest
from lgca.automata import Lgca, Lbm


@pytest.mark.parametrize("mode", (None, Lgca.MODE_TORUS, Lgca.MODE_DIE))
def test_general(mode):
    width = 19
    height = 19
    steps = 10

    grid = [[0 for _ in range(width)] for _ in range(height)]
    grid[height // 2][width // 2] = 0b001001

    automaton: Lbm = Lbm(grid=grid) if mode is None else Lbm(grid=grid, mode=mode)

    for _ in range(steps):
        next(automaton)
