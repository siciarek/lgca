import pygame
from . import BaseGrid


class SquareGrid(BaseGrid):

    def set_up_window(self) -> None:
        height, width = len(self.automaton.grid), len(self.automaton.grid[0])
        self.screen: pygame.Surface = pygame.Surface((width, height))
        self.window: pygame.Surface = pygame.display.set_mode(size=(width * self.tile_size, height * self.tile_size))

    def draw_grid(self) -> None:

        # Convert automaton grid to bitmap.
        pixel_array: pygame.PixelArray = pygame.PixelArray(self.screen)
        for y, row in enumerate(self.automaton.grid):
            for x, val in enumerate(row):
                color = self.colors[val]
                pixel_array[x, y] = color
        pixel_array.close()

        # Adjust bitmap to screen size.
        self.window.blit(pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0))

        # Update title and refresh the screen.
        pygame.display.set_caption(f"{self.title} ({self.automaton.step})")
        pygame.display.flip()
        pygame.display.update()
