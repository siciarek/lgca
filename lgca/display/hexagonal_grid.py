import pygame
from lgca.utils.hexagon import Hex, Layout, Point, layout_flat, polygon_corners
from copy import deepcopy
from math import sqrt, ceil, floor


class HexagonalGrid:
    def __init__(
        self,
        automaton,
        title: str = "Hexagonal Grid",
        tile_size: int = 1,
        run: bool = False,
        fps: int = 60,
        max_iteration: int = -1,
        colors: tuple = ("#000000", "#FFFFFF"),
        background: str | tuple[int] = "#000000",
    ):
        height, width = len(automaton.grid), len(automaton.grid[0])
        width_margin = -tile_size // 2
        size = (
            ceil(width / 2) * (tile_size)
            + floor(width / 2) * (tile_size // 2)
            + tile_size * (sqrt(3) / 2)
            + width_margin,
            (height + 1) * tile_size * (sqrt(3) / 2) - tile_size // 3,
        )

        print("SIZE:", size)

        pygame.init()
        self.tile_size = tile_size
        self.window: pygame.Surface = pygame.display.set_mode(size=size)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.title = title
        self.animate: bool = run
        self.automaton = automaton
        self.initial_grid_state = deepcopy(self.automaton.grid)
        self.fps = fps
        self.max_iteration = max_iteration
        self.colors = colors

        s = self.tile_size // 2
        self.layout = Layout(layout_flat, Point(s, s), Point(s, s))
        self.background = background

    def __next__(self):
        if 0 < self.max_iteration < self.automaton.step:
            return

        self.draw_grid()

        if self.animate:
            next(self.automaton)

    def mainloop(self):
        self.run()

    def run(self):
        running = True

        while running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    running = False

                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_SPACE:
                            self.animate = not self.animate
                        case pygame.K_s:
                            self.automaton.grid = deepcopy(self.initial_grid_state)
                            self.automaton.step = 0
                        case pygame.K_RIGHT:
                            if not self.animate:
                                next(self.automaton)
            next(self)

        pygame.quit()

    def draw_grid(self) -> None:
        self.window.fill(self.background)

        for row in range(self.automaton.height):
            for col in range(self.automaton.width):
                value = self.automaton.grid[row][col]
                if value == 0:
                    continue
                self.draw_hexagon(col=col, row=row, color=self.colors[value])

        # Update title and refresh the screen.
        pygame.display.set_caption(f"{self.title} ({self.automaton.step})")
        pygame.display.update()

    def draw_hexagon(self, row, col, color):
        q, s = col, -(row + col % 2) - col // 2
        r = -(q + s)
        corners = polygon_corners(layout=self.layout, h=Hex(q=q, r=r, s=s))
        pygame.draw.polygon(
            surface=self.window,
            color=color,
            points=[(point.x, point.y) for point in corners],
        )
