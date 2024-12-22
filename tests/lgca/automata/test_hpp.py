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
