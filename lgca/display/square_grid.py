import pygame
from copy import deepcopy


class SquareGrid:

    def __init__(
        self,
        automaton,
        title: str = "Square Grid",
        tile_size: int = 1,
        run: bool = False,
        fps: int = 60,
        max_iteration: int = -1,
        colors: tuple = ("#000000", "#ffffff"),
    ):
        height, width = len(automaton.grid), len(automaton.grid[0])
        self.screen: pygame.Surface = pygame.Surface((width, height))
        self.window: pygame.Surface = pygame.display.set_mode(size=(width * tile_size, height * tile_size))

        self.title = title
        self.animate: bool = run
        self.automaton = automaton
        self.initial_grid_state = deepcopy(self.automaton.grid)
        self.fps = fps
        self.max_iteration = max_iteration
        self.colors = colors

    def __next__(self):
        if 0 < self.max_iteration < self.automaton.step:
            return

        self.draw_grid(self.automaton.grid)

        if self.animate:
            next(self.automaton)

    def mainloop(self):
        pygame.init()
        self.run()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
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

            clock.tick(self.fps)

    def draw_grid(self, grid: list) -> None:

        # Convert automaton grid to bitmap.
        self.pixel_array = pygame.PixelArray(self.screen)
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                color = self.colors[val]
                self.pixel_array[x, y] = color
        self.pixel_array.close()

        # Adjust bitmap to screen size.
        self.window.blit(pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0))

        # Update title and refresh the screen.
        pygame.display.set_caption(f"{self.title} ({self.automaton.step})")
        pygame.display.flip()
        pygame.display.update()
