from lgca.automata import FhpII, Lgca
from tests.helpers import get_test_data


def test_general():
    width = 19
    height = 19
    steps = 15

    input_grid = [[0 for _ in range(width)] for _ in range(height)]
    input_grid[height // 2][width // 2] = 0b100100

    automaton: Lgca = FhpII(grid=input_grid)

    for _ in range(steps):
        next(automaton)


def test_next():
    step_count = 6
    input_dat, expected_dat = get_test_data(folder="fhp_ii", step_count=step_count)

    for idx, input_grid in input_dat.items():
        automaton: Lgca = FhpII(grid=input_grid)
        for _ in range(step_count):
            next(automaton)
        assert automaton.grid == expected_dat[idx]
