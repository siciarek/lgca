import pygame
from . import BaseGrid
from lgca.utils.hexagon import Hex, Layout, Point, layout_flat, polygon_corners
from math import sqrt, ceil, floor


class HexagonalGrid(BaseGrid):

    def set_up_window(self) -> tuple[pygame.Surface, pygame.Surface]:
        height, width = len(self.automaton.grid), len(self.automaton.grid[0])
        self.screen: pygame.Surface = pygame.Surface((width, height))
        self.window: pygame.Surface = pygame.display.set_mode(size=(width * self.tile_size, height * self.tile_size))

        width_margin = -self.tile_size // 2
        size = (
            ceil(width / 2) * (self.tile_size)
            + floor(width / 2) * (self.tile_size // 2)
            + self.tile_size * (sqrt(3) / 2)
            + width_margin,
            (height + 1) * self.tile_size * (sqrt(3) / 2) - self.tile_size // 3,
        )

        s = self.tile_size // 2
        self.layout = Layout(layout_flat, Point(s, s), Point(s, s))
        self.window: pygame.Surface = pygame.display.set_mode(size=size)

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
