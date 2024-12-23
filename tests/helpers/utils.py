from pathlib import Path
from collections import defaultdict


def get_test_grid_from_file(file: Path):
    assert file.is_file()

    grid = defaultdict(list)

    with file.open() as fp:
        curr_idx = 0

        for line in fp:
            line = line.strip()
            if not line:
                curr_idx += 1
                continue
            line = line.replace(".", "0")
            row = [int(i) for i in list(line)]
            grid[curr_idx].append(row)

    return grid


def get_test_data(folder: str, step_count: int = None):
    test_data_dir = Path(__file__).parent.parent / "data" / folder
    input_dat_file = test_data_dir / "input.dat"
    expected_dat_file = test_data_dir / (f"expected.{step_count}.dat" if step_count else "expected.dat")

    input_dat = get_test_grid_from_file(file=input_dat_file)
    expected_dat = get_test_grid_from_file(file=expected_dat_file)

    return input_dat, expected_dat
