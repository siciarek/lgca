from pathlib import Path
from collections import defaultdict
from lgca.automata import Hpp, Lgca


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
    input_dat, expected_dat = get_test_data(model="hpp", step_count=step_count)

    for idx, input_grid in input_dat.items():
        automaton: Lgca = Hpp(grid=input_grid)
        for _ in range(step_count):
            next(automaton)
        assert automaton.grid == expected_dat[idx]


def get_test_data(model: str, step_count: int):
    test_data_dir = Path(__file__).parent.parent.parent / "data" / model
    input_dat_file = test_data_dir / "input.dat"
    expected_dat_file = test_data_dir / f"expected.{step_count}.dat"

    assert input_dat_file.is_file()
    assert expected_dat_file.is_file()

    input_dat = defaultdict(list)
    expected_dat = defaultdict(list)

    with input_dat_file.open() as fp:
        curr_idx = 0

        for line in fp:
            line = line.strip()
            if not line:
                curr_idx += 1
                continue

            input_dat[curr_idx].append([int(i) for i in list(line)])

    with expected_dat_file.open() as fp:
        curr_idx = 0

        for line in fp:
            line = line.strip()
            if not line:
                curr_idx += 1
                continue

            expected_dat[curr_idx].append([int(i) for i in list(line)])

    return input_dat, expected_dat
