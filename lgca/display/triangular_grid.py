import pygame
from copy import deepcopy


class TriangularGrid:

    def __init__(
        self,
        automaton,
        title: str = "Triangular Grid",
        tile_size: int = 8,
        run: bool = False,
        fps: int = 60,
        max_iteration: int = -1,
        colors: tuple = ("#000000", "#ffffff"),
        grid_size: int = 0,
        background: str = "#000000",
    ):
        self.tile_size: int = tile_size
        height = len(automaton.grid) * (self.tile_size * 2) + 4
        width = len(automaton.grid[0]) * (self.tile_size + 1) + 4
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.animate: bool = run
        self.iteration: int = 0
        self.automaton = automaton
        self.initial_grid_state = deepcopy(self.automaton.grid)
        self.set_window_title(title)
        self.fps = fps
        self.max_iteration = max_iteration
        self.colors = colors
        self.grid_size = grid_size
        self.background = background if background else self.colors[0]

    def mainloop(self):
        pygame.init()
        self.run()

    def set_window_title(self, title):
        self.name: str = title
        self.title: str = self.name.replace("-", " ")
        pygame.display.set_caption(f"{self.title} ({self.automaton.step})")

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_SPACE:
                            self.animate = not self.animate
                        case pygame.K_ESCAPE:
                            self.automaton.grid = deepcopy(self.initial_grid_state)
                            self.automaton.step = 0
                        case pygame.K_RIGHT:
                            if not self.animate:
                                self.iterate()
            self.make_a_step()

            pygame.display.flip()
            pygame.display.update()
            clock.tick(self.fps)

    def iterate(self):
        self.automaton.grid = self.automaton.update_grid()

    def make_a_step(self):
        if 0 < self.max_iteration < self.automaton.step:
            return

        self.screen.fill(self.background)
        self.draw_grid(self.automaton.grid)
        pygame.display.set_caption(f"{self.title} ({self.automaton.step})")

        if self.animate:
            self.iterate()

    def draw_triangle(self, surface, color, position, size, mode):
        x, y = position
        points = []

        if mode:
            # white
            points.append((x - size, y))
            points.append((x - size // 2, y - size))
            points.append((x, y))
        else:
            # red
            points.append((x, y - size))
            points.append((x - size // 2, y))
            points.append((x - size, y - size))

        pygame.draw.polygon(surface=surface, color=color, points=points, width=0)

    def draw_grid(self, grid: list) -> None:

        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                size = self.tile_size
                color = self.colors[val]

                self.draw_triangle(
                    surface=self.screen,
                    color=color,
                    size=size,
                    position=(
                        x * size // 2 + size + 2 * x,
                        y * size + size + 2 * y,
                    ),
                    mode=(x + y % 2) % 2,
                )
