import pygame
from . import BaseGrid


class TriangularGrid(BaseGrid):

    def set_up_window(self) -> None:
        height = len(self.automaton.grid) * (self.tile_size * 2) + 4
        width = len(self.automaton.grid[0]) * (self.tile_size + 1) + 4

        self.screen: pygame.Surface = pygame.display.set_mode((width, height))

    def draw_grid(self) -> None:

        for y, row in enumerate(self.automaton.grid):
            for x, val in enumerate(row):
                size = self.tile_size
                color = self.colors[val]

                self.draw_triangle(
                    color=color,
                    size=size,
                    position=(
                        x * size // 2 + size + 2 * x,
                        y * size + size + 2 * y,
                    ),
                    mode=(x + y % 2) % 2,
                )

    def draw_triangle(self, color, position, size, mode):
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

        pygame.draw.polygon(surface=self.screen, color=color, points=points, width=0)
