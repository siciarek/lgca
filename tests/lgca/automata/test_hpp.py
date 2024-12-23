from lgca.automata import Hpp, Lgca
from tests.helpers.utils import get_test_data


def test_general():
    width = 17
    height = 17
    steps = 5

    input_grid = [[0 for _ in range(width)] for _ in range(height)]
    input_grid[height // 2][width // 2] = 0b001001

    automaton: Lgca = Hpp(grid=input_grid)

    for _ in range(steps):
        next(automaton)


def test_next():
    step_count = 6
    input_dat, expected_dat = get_test_data(folder="hpp", step_count=step_count)

    for idx, input_grid in input_dat.items():
        automaton: Lgca = Hpp(grid=input_grid)
        for _ in range(step_count):
            next(automaton)
        assert automaton.grid == expected_dat[idx]
