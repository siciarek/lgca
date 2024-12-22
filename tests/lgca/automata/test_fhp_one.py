from lgca.automata import FhpOne, Lgca


def test_general():
    width = 9
    height = 9
    steps = 5

    input_grid = [[0 for _ in range(width)] for _ in range(height)]
    input_grid[height // 2][width // 2] = 0b100100

    automaton: Lgca = FhpOne(grid=input_grid)

    for _ in range(steps):
        next(automaton)
